import re


def extract_air_report_data(text):

    data = {

        "company_name": None,
        "monitoring_date": None,

        "pm25": None,
        "pm10": None,

        "so2": None,
        "nox": None,
        "co": None,

        "overall_status": None,
        "remarks": None
    }

    # =========================
    # CLEAN TEXT
    # =========================

    text = text.replace("\n", " ")

    # =========================
    # COMPANY NAME
    # =========================

    company = re.search(

        r"Company\s*Name[:\s]+(.*?)(?:Monitoring|Sample|Date)",

        text,

        re.IGNORECASE
    )

    if company:

        data["company_name"] = (
            company.group(1).strip()
        )

    # =========================
    # MONITORING DATE
    # =========================

    monitoring_date = re.search(

        r"Monitoring\s*Date[:\s]+([A-Za-z0-9\s:-]+)",

        text,

        re.IGNORECASE
    )

    if monitoring_date:

        data["monitoring_date"] = (
            monitoring_date.group(1).strip()
        )

    # =========================
    # PM2.5
    # =========================

    pm25 = re.search(

        r"PM2\.?5.*?(\d+(?:\.\d+)?)\s*(?:µg|ug|mg)",

        text,

        re.IGNORECASE
    )

    if pm25:

        data["pm25"] = float(
            pm25.group(1)
        )

    # =========================
    # PM10
    # =========================

    pm10 = re.search(

        r"PM10.*?(\d+(?:\.\d+)?)\s*(?:µg|ug|mg)",

        text,

        re.IGNORECASE
    )

    if pm10:

        data["pm10"] = float(
            pm10.group(1)
        )

    # =========================
    # SO2
    # =========================

    so2 = re.search(

        r"SO2.*?(\d+(?:\.\d+)?)\s*(?:mg|µg|ug)",

        text,

        re.IGNORECASE
    )

    if so2:

        data["so2"] = float(
            so2.group(1)
        )

    # =========================
    # NOX
    # =========================

    nox = re.search(

        r"NOx.*?(\d+(?:\.\d+)?)\s*(?:mg|µg|ug)",

        text,

        re.IGNORECASE
    )

    if nox:

        data["nox"] = float(
            nox.group(1)
        )

    # =========================
    # CO
    # =========================

    co = re.search(

        r"CO.*?(\d+(?:\.\d+)?)\s*(?:mg|µg|ug)",

        text,

        re.IGNORECASE
    )

    if co:

        data["co"] = float(
            co.group(1)
        )

    # =========================
    # STATUS
    # =========================

    if "NON-COMPLIANT" in text.upper():

        data["overall_status"] = (
            "NON-COMPLIANT"
        )

    elif "COMPLIANT" in text.upper():

        data["overall_status"] = (
            "COMPLIANT"
        )

    # =========================
    # REMARKS
    # =========================

    remarks = re.search(

        r"(?:Remarks|Observations).*?(.*?)(?:Authorized|Signature|$)",

        text,

        re.IGNORECASE | re.DOTALL
    )

    if remarks:

        data["remarks"] = (
            remarks.group(1).strip()[:500]
        )

    return data