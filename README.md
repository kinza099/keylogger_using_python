# ⌨ KeyScope — Live Keylogger Dashboard

> A beautiful, real-time keystroke analytics dashboard built with Flask and a dark-themed web UI.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1.3-black?style=flat-square&logo=flask)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)

---

## ✨ Features

- **Live Keystroke Feed** — Real-time log of every key press with timestamps
- **Timeline Chart** — Bar chart showing keystroke activity over the last 60 seconds
- **Character Frequency Histogram** — See which keys you press the most
- **Special Keys Tracker** — Separate analysis for Backspace, Enter, Space, and more
- **Keyboard Heatmap** — Visual keyboard where frequently pressed keys glow brighter
- **Session Stats** — Total keys, unique keys, words typed, keys/min, and session time
- **Export to JSON** — Download your full session data in one click
- **Server-Sent Events (SSE)** — No page refresh needed; everything updates live

---

## 🖥 Preview

```
⌨ KeyScope is running → http://127.0.0.1:5000
```

Dark-themed dashboard featuring:
- Violet/cyan color palette
- Scanline overlay effect
- Monospace (JetBrains Mono) typography
- Fully responsive grid layout

---

## 📸 Screenshots

### Dashboard Overview
![Dashboard Overview](https://github.com/user-attachments/assets/46796db4-9ce4-4f77-afb8-8b46a68ea132)

### Live Feed & Key Frequency
![Live Feed](https://github.com/user-attachments/assets/2ac352e3-10f1-40a0-a658-08f48a7e39f3)

### Keyboard Heatmap
![Keyboard Heatmap](https://github.com/user-attachments/assets/62d0a43d-7b54-48ff-9c3d-5ac7d20a6d27)

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/keyscope.git
cd keyscope
```

### 2. Install dependencies

```bash
pip install flask pynput
```

### 3. Set up the folder structure

```
keyscope/
├── app.py
└── templates/
    └── index.html
```

> **Note:** Make sure `index.html` is placed inside the `templates/` folder so Flask can serve it correctly.

---

## 🚀 Usage

```bash
python app.py
```

Then open your browser and navigate to:

```
http://127.0.0.1:5000
```

### Dashboard Controls

| Button | Action |
|--------|--------|
| ▶ Start | Begin recording keystrokes |
| ■ Stop | Pause the recording |
| ↺ Reset | Clear all session data |
| ↓ Export | Download session as JSON |

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serves the dashboard UI |
| `/api/start` | POST | Start keystroke recording |
| `/api/stop` | POST | Stop keystroke recording |
| `/api/reset` | POST | Reset all state and data |
| `/api/stats` | GET | Returns live stats as JSON |
| `/api/export` | GET | Download full session export |
| `/stream` | GET | SSE stream for live events |

---

## 📊 Exported JSON Format

```json
{
  "exported_at": "2025-01-01 12:00:00",
  "session_start": "2025-01-01 11:45:00",
  "total_keystrokes": 342,
  "words_typed": 68,
  "char_frequency": { "a": 45, "e": 38 },
  "special_frequency": { "backspace": 12, "space": 71 },
  "log": [
    { "ts": "11:45:01.234", "key": "H", "kind": "char", "n": 1 }
  ]
}
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3, Flask |
| Keyboard Hook | `pynput` |
| Live Updates | Server-Sent Events (SSE) |
| Charts | Chart.js 4.4 |
| Fonts | JetBrains Mono, Inter (Google Fonts) |
| Frontend | Vanilla HTML / CSS / JS |

---

## ⚠️ Important Notes

- **For personal use only.** Installing this tool on someone else's computer without their knowledge or consent is **illegal** and unethical.
- This project is intended for **educational and personal productivity** purposes — for example, analyzing your own typing speed and habits.
- On **macOS**, you will need to grant Accessibility permissions on first run (`System Settings → Privacy & Security → Accessibility`).
- On **Linux**, root or sudo privileges may be required to capture keyboard events.

---

## 📁 Project Structure

```
keyscope/
├── app.py              # Flask backend + keylogger engine
├── templates/
│   └── index.html      # Full dashboard UI (single file)
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 📝 requirements.txt

```
flask
pynput
```

To generate automatically:

```bash
pip freeze > requirements.txt
```

---

## 🤝 Contributing

Pull requests are welcome! If you find a bug or want to suggest a feature, feel free to open an issue.

---

## 📜 License

MIT License — free to use, modify, and distribute.

---

<div align="center">
  Made with ❤️ &nbsp;|&nbsp; KeyScope v1.0
</div>
