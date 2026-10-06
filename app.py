from flask import Flask, render_template, request, redirect
from logic.performance_analysis import analyze_students
from logic.suggestions import get_suggestions
from logic.notification_engine import decide_notification
from logic.message_templates import email_message, sms_message
from logic.email_sender import send_email
from logic.sms_simulator import send_sms


import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# HOME
@app.route("/")
def home():
    return render_template("home.html")

# FACULTY VIEW
@app.route("/faculty", methods=["GET", "POST"])
def faculty():
    students = []
    error = None

    if request.method == "POST":
        file = request.files["file"]

        if not file.filename.endswith(".csv"):
            error = "Please upload a CSV file"
        else:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            data = analyze_students(file_path)

            for row in data:
                gaps = row["Gaps"].split(", ") if row["Gaps"] else []
                row["Suggestions"] = get_suggestions(gaps, row["Risk"])

            students = data

    return render_template("faculty.html", students=students, error=error)
# SEND MESSAGE FROM FACULTY (NEW)
@app.route("/send_message", methods=["POST"])
def send_message():
    student = request.form["student"]
    email = request.form.get("email")
    phone = request.form.get("phone")
    message = request.form["message"]
    risk = request.form.get("risk")

    subject = f"Academic Guidance ({risk} Risk)"

    # Send email (real)
    if email:
        send_email(email, subject, message)

    # Send SMS (simulated)
    if phone:
        send_sms(phone, f"{student}: {message}")

    return redirect("/faculty")

# STUDENT VIEW
@app.route("/student", methods=["GET", "POST"])
def student():
    student_data = None
    error = None

    if request.method == "POST":
        student_name = request.form["student_name"].strip()
        file_path = os.path.join(UPLOAD_FOLDER, os.listdir(UPLOAD_FOLDER)[0])

        data = analyze_students(file_path)

        for row in data:
            if str(row["Student"]).lower() == student_name.lower():
                gaps = row["Gaps"].split(", ") if row["Gaps"] else []

                # Existing suggestion logic
                row["Suggestions"] = [s for s in row["Suggestions"] if s.strip()]

            

                # 🔔 Notification decision
                notify, level = decide_notification(row["Risk"])

                if notify:
                    # Email notification
                    if "Email" in row and row["Email"]:
                        body = email_message(row["Student"], row["Risk"], gaps)
                        send_email(
                        row["Email"],
                        "Academic Risk Alert",
                        body
                        )

                    # SMS notification (simulated)
                    if "Phone" in row and row["Phone"]:
                        msg = sms_message(row["Student"], row["Risk"])
                        send_sms(row["Phone"], msg)

                student_data = row
                break   # ✅ break ONLY after student is found


        if not student_data:
            error = "Student not found"

    return render_template("student.html", student=student_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
