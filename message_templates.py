def email_message(student, risk, gaps):
    if risk == "High":
        return f"""
Dear {student},

You are currently at HIGH academic risk.
Weak areas: {', '.join(gaps)}

Immediate action is required.
Please consult your faculty mentor this week.

Regards,
Academic Support System
"""

    elif risk == "Medium":
        return f"""
Dear {student},

You are at MEDIUM academic risk.
Weak areas: {', '.join(gaps)}

Consistent revision can help prevent decline.

Regards,
Academic Support System
"""

def sms_message(student, risk):
    if risk == "High":
        return f"ALERT: {student}, you are at HIGH academic risk. Immediate action needed."
    elif risk == "Medium":
        return f"NOTICE: {student}, you are at MEDIUM academic risk. Revise weak subjects."
