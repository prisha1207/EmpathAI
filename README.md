# EmpathAI — Human-Aware Email Assistant
> Intelligent • Context-Aware • Automated Scheduling

EmpathAI is a Flask-based web application that reads an email, 
understands its emotional tone and urgency, automatically schedules 
a meeting, and generates a smart reply — all without any manual effort.

---
## 🚀 Features

- 📧 **Email Parsing** — Extracts meeting time from raw email text
- 😊 **Sentiment & Tone Detection** — Detects if an email is Urgent, Normal, or Flexible
- ⭐ **Priority Assignment** — High / Medium / Low based on tone
- 📅 **Smart Scheduling** — Avoids conflicts, finds the next free slot automatically
- 💬 **Smart Reply Generation** — Writes a context-aware confirmation reply
- 🌐 **Web Interface** — Clean, minimal Flask UI

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| NLP / Pattern Matching | Python `re` module |
| Sentiment Detection | Keyword-based logic |
| Time Handling | Python `datetime`, `timedelta` |
| Frontend | HTML, CSS (inline with Flask) |

---

## ⚙️ How to Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/EmpathAI.git
cd EmpathAI
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
python app.py
```

### 4. Open in browser
link: http://127.0.0.1:5000/

## 📸 Demo

![EmpathAI Screenshot](screenshots/demo.png)

---

## 🔄 How It Works
User types email
↓
extract_time()    →  Finds "3 PM"
detect_tone()     →  Detects "Urgent"
assign_priority() →  Returns "High"
schedule_meeting() → Books slot, avoids conflicts
generate_reply()  →  Writes smart confirmation
↓
Result displayed on screen

---

## 👥 Team CodeSlayers
- Harshita Jain
- Aarya Pargaonkar
- Prisha Banerjee
- Purva Kawathe

---

## 📄 License
This project was built as part of an academic prototype submission.
