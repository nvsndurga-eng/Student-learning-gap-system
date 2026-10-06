def decide_notification(risk):
    if risk == "High":
        return True, "HIGH"
    elif risk == "Medium":
        return True, "MEDIUM"
    else:
        return False, None
