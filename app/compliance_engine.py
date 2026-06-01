def calculate_compliance_score(data):

    score = 100
    alerts = []

    if data.get("cod") and data["cod"] > 250:
        score -= 10
        alerts.append("COD Above Limit")

    if data.get("bod") and data["bod"] > 30:
        score -= 10
        alerts.append("BOD Above Limit")

    if data.get("ph"):
        if data["ph"] < 6.5 or data["ph"] > 8.5:
            score -= 10
            alerts.append("pH Out Of Range")

    return {
        "score": max(score, 0),
        "alerts": alerts
    }