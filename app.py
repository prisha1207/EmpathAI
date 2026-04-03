import re
from flask import Flask, request, render_template_string
from datetime import datetime, timedelta

app = Flask(__name__)

# -----------------------------
# In-memory schedule
# -----------------------------
scheduled_meetings = []

# -----------------------------
# Utility Functions
# -----------------------------

def extract_time(email):
    match = re.search(r'(\d{1,2}(:\d{2})?\s?(AM|PM))', email, re.IGNORECASE)
    if match:
        return match.group().upper()
    return "Not specified"

def detect_tone(email):
    email = email.lower()
    if "urgent" in email or "asap" in email:
        return "Urgent"
    elif "no rush" in email or "whenever" in email:
        return "Flexible"
    return "Normal"

def assign_priority(tone):
    if tone == "Urgent":
        return "High"
    elif tone == "Flexible":
        return "Low"
    return "Medium"

# -----------------------------
# Time Handling
# -----------------------------

def parse_time(time_str):
    try:
        return datetime.strptime(time_str, "%I:%M %p")
    except:
        return None

def is_overlapping(new_time):
    new_dt = parse_time(new_time)
    if not new_dt:
        return False

    for meeting in scheduled_meetings:
        existing_dt = parse_time(meeting)
        if existing_dt:
            # assume 1 hour duration
            if abs((new_dt - existing_dt).total_seconds()) < 3600:
                return True
    return False

def find_alternative(time_str):
    base = parse_time(time_str)
    if not base:
        return "Next Available Slot"

    for i in range(1, 5):
        new_time = (base + timedelta(hours=i)).strftime("%I:%M %p")
        if not is_overlapping(new_time):
            return new_time

    return "No nearby slot available"

# -----------------------------
# FIXED Natural Time Formatting
# -----------------------------

def format_with_day(time_str):
    now = datetime.now()

    try:
        meeting_time = datetime.strptime(time_str, "%I:%M %p")
    except:
        return time_str

    # attach today's date
    meeting_time = meeting_time.replace(
        year=now.year,
        month=now.month,
        day=now.day
    )

    # IMPORTANT FIX:
    # if time already passed OR equal → move to next day
    if meeting_time <= now:
        meeting_time += timedelta(days=1)

    day_name = meeting_time.strftime("%A")
    formatted_time = meeting_time.strftime("%I:%M %p").lstrip("0")

    if meeting_time.date() == now.date():
        return f"Today {formatted_time}"
    elif meeting_time.date() == (now + timedelta(days=1)).date():
        return f"Tomorrow {formatted_time}"
    else:
        return f"{day_name} {formatted_time}"

# -----------------------------
# Scheduling Logic
# -----------------------------

def schedule_meeting(time, priority):
    global scheduled_meetings

    # Better default times (avoids weird early morning outputs)
    if time == "Not specified":
        if priority == "High":
            time = "04:00 PM"
        elif priority == "Medium":
            time = "02:00 PM"
        else:
            time = "11:00 AM"

    # Handle overlap
    if is_overlapping(time):
        alt = find_alternative(time)
        scheduled_meetings.append(alt)
        final_time = alt
    else:
        scheduled_meetings.append(time)
        final_time = time

    return format_with_day(final_time)

# -----------------------------
# Reply Generator
# -----------------------------

def generate_reply(tone, scheduled_time):
    if tone == "Urgent":
        return f"Your urgent request has been prioritized. Meeting scheduled at {scheduled_time}."
    elif tone == "Flexible":
        return f"Your request is flexible. Scheduled at {scheduled_time}."
    else:
        return f"Meeting scheduled at {scheduled_time}."

# -----------------------------
# UI
# -----------------------------

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>EmpathAI Email Analyzer</title>
    <style>
        body {
            margin: 0;
            font-family: "Segoe UI", sans-serif;
            background: linear-gradient(135deg, #f5f5dc, #e6f4f1);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #2f3e46;
        }

        .container {
            width: 420px;
            padding: 30px;
            border-radius: 20px;
            background: #ffffffcc;
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }

        h2 {
            text-align: center;
            margin-bottom: 20px;
            font-weight: 600;
            color: #52796f;
        }

        input {
            width: 100%;
            padding: 14px;
            border-radius: 12px;
            border: 1px solid #cad2c5;
            background: #f8f9fa;
            font-size: 14px;
            outline: none;
            transition: 0.2s;
        }

        input:focus {
            border-color: #84a98c;
            box-shadow: 0 0 0 2px rgba(132,169,140,0.3);
        }

        button {
            width: 100%;
            margin-top: 16px;
            padding: 14px;
            border: none;
            border-radius: 12px;
            background: linear-gradient(135deg, #84a98c, #52796f);
            color: white;
            font-size: 15px;
            font-weight: 500;
            cursor: pointer;
            transition: 0.25s;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(82,121,111,0.3);
        }

        .result {
            margin-top: 22px;
            padding: 18px;
            border-radius: 14px;
            background: #f0efeb;
            border: 1px solid #dde5d9;
            white-space: pre-wrap;
            line-height: 1.6;
            font-size: 14px;
        }

        .urgent {
            color: #d62828;
            font-weight: 600;
        }

        .footer {
            text-align: center;
            margin-top: 15px;
            font-size: 11px;
            color: #6c757d;
        }
    </style>
</head>
<body>

<div class="container">
    <h2>🌿 EmpathAI Analyzer</h2>

    <form method="POST">
        <input type="text" name="email" placeholder="Type or paste your email..." required>
        <button type="submit">Analyze</button>
    </form>

    {% if result %}
    <div class="result {% if 'Urgent' in result %}urgent{% endif %}">
        {{ result }}
    </div>
    {% endif %}

    <div class="footer">
        calm. intelligent. organized.
    </div>
</div>

</body>
</html>
"""

# -----------------------------
# Route
# -----------------------------

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        email = request.form.get("email", "")

        time = extract_time(email)
        tone = detect_tone(email)
        priority = assign_priority(tone)
        scheduled_time = schedule_meeting(time, priority)
        reply = generate_reply(tone, scheduled_time)

        result = f"""
🕒 Time: {time}
😊 Tone: {tone}
⭐ Priority: {priority}
📅 Scheduled: {scheduled_time}

💬 Reply:
{reply}
"""

    return render_template_string(HTML, result=result)

# -----------------------------
# Run
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)
