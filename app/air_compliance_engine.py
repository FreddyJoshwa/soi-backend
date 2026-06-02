


def calculate_air_compliance_score(data):

    score = 100
    alerts = []

    if data.get("pm25") and data["pm25"] > 60:
        score -= 10
        alerts.append("PM2.5 Above Limit")

    if data.get("pm10") and data["pm10"] > 100:
        score -= 10
        alerts.append("PM10 Above Limit")

    if data.get("so2") and data["so2"] > 80:
        score -= 10
        alerts.append("SO2 Above Limit")

    if data.get("nox") and data["nox"] > 80:
        score -= 10
        alerts.append("NOx Above Limit")

    if data.get("co") and data["co"] > 2:
        score -= 10
        alerts.append("CO Above Limit")

    return {
        "score": max(score, 0),
        "alerts": alerts
    }