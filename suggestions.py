SUGGESTIONS = {
    "Maths": "Revise algebra basics and practice problems",
    "Physics": "Focus on formulas and numerical problems",
    "CS": "Practice loops, conditions, and basic programs",
    "English": "Improve grammar and reading comprehension"
}

def get_suggestions(gaps, risk):
    advice = []

    for subject in gaps:
        advice.append(SUGGESTIONS.get(subject, ""))

    if risk == "Medium":
        advice.append("Follow a weekly revision schedule")

    if risk == "High":
        advice.append("Immediate mentoring and extra practice needed")

    return advice
