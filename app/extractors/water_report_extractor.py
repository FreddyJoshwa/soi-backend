import re


def extract_water_report_data(text):

    data = {

        "company_name": None,
        "sample_type": None,

        "collection_date": None,
        "analysis_date": None,

        "ph": None,
        "tds": None,
        "cod": None,
        "bod": None,

        "overall_status": None,
        "remarks": None
    }

    # =========================
    # COMPANY NAME
    # =========================

    company = re.search(
        r"Company Name\s*:\s*(.*)",
        text,
        re.IGNORECASE
    )

    if company:

        data["company_name"] = (
            company.group(1).strip()
        )

    # =========================
    # SAMPLE TYPE
    # =========================

    sample_type = re.search(
        r"Sample Type\s*:\s*(.*)",
        text,
        re.IGNORECASE
    )

    if sample_type:

        data["sample_type"] = (
            sample_type.group(1).strip()
        )

    # =========================
    # COLLECTION DATE
    # =========================

    collection_date = re.search(
        r"Collection Date\s*:\s*(.*)",
        text,
        re.IGNORECASE
    )

    if collection_date:

        data["collection_date"] = (
            collection_date.group(1).strip()
        )

    # =========================
    # ANALYSIS DATE
    # =========================

    analysis_date = re.search(
        r"Analysis Date\s*:\s*(.*)",
        text,
        re.IGNORECASE
    )

    if analysis_date:

        data["analysis_date"] = (
            analysis_date.group(1).strip()
        )

    # =========================
    # pH
    # =========================

    ph = re.search(
        r"pH\s*\(at.*?\)\s*-\s*(\d+\.\d+)",
        text,
        re.IGNORECASE
    )

    if ph:

        data["ph"] = float(
            ph.group(1)
        )

    # =========================
    # TDS
    # =========================

    tds = re.search(
        r"TDS\)\s*mg/L\s*(\d+)",
        text,
        re.IGNORECASE
    )

    if tds:

        data["tds"] = float(
            tds.group(1)
        )

    # =========================
    # COD
    # =========================

    cod = re.search(
        r"COD\)\s*mg/L\s*(\d+)",
        text,
        re.IGNORECASE
    )

    if cod:

        data["cod"] = float(
            cod.group(1)
        )

    # =========================
    # BOD
    # =========================

    bod = re.search(
        r"BOD\)\s*mg/L\s*(\d+)",
        text,
        re.IGNORECASE
    )

    if bod:

        data["bod"] = float(
            bod.group(1)
        )

    # =========================
    # STATUS
    # =========================

    status = re.search(
        r"Overall Compliance Status:\s*(\w+)",
        text,
        re.IGNORECASE
    )

    if status:

        data["overall_status"] = (
            status.group(1).strip()
        )

    # =========================
    # REMARKS
    # =========================

    remarks = re.search(
        r"Remarks:\s*(.*?)\[",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if remarks:

        data["remarks"] = (
            remarks.group(1).strip()
        )

    return data