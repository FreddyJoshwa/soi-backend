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
    # CLEAN TEXT
    # =========================

    clean_text = text.replace("\n", " ")

    # =========================
    # COMPANY NAME
    # =========================

    company = re.search(

        r"Company\s*Name[:\s]+(.*?)(?:Sample|Collection|Date)",

        clean_text,

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

        r"Sample\s*Type[:\s]+(.*?)(?:Collection|Analysis|Date)",

        clean_text,

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

        r"Collection\s*Date[:\s]+([A-Za-z0-9\s:-]+)",

        clean_text,

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

        r"Analysis\s*Date[:\s]+([A-Za-z0-9\s:-]+)",

        clean_text,

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

        r"pH.*?(\d+(?:\.\d+)?)",

        clean_text,

        re.IGNORECASE
    )

    if ph:

        value = float(ph.group(1))

        if 0 <= value <= 14:

            data["ph"] = value

    # =========================
    # TDS
    # =========================

    tds = re.search(

        r"TDS.*?(\d+(?:\.\d+)?)\s*(?:mg/L|mg|ppm)?",

        clean_text,

        re.IGNORECASE
    )

    if tds:

        value = float(tds.group(1))

        if value > 10:

            data["tds"] = value

    # =========================
    # COD
    # =========================

    cod = re.search(

        r"COD.*?(\d+(?:\.\d+)?)\s*(?:mg/L|mg)?",

        clean_text,

        re.IGNORECASE
    )

    if cod:

        value = float(cod.group(1))

        if value > 1:

            data["cod"] = value

    # =========================
    # BOD
    # =========================

    bod = re.search(

        r"BOD.*?(\d+(?:\.\d+)?)\s*(?:mg/L|mg)?",

        clean_text,

        re.IGNORECASE
    )

    if bod:

        value = float(bod.group(1))

        if value > 1:

            data["bod"] = value

    # =========================
    # STATUS
    # =========================

    if "NON-COMPLIANT" in clean_text.upper():

        data["overall_status"] = (
            "NON-COMPLIANT"
        )

    elif "COMPLIANT" in clean_text.upper():

        data["overall_status"] = (
            "COMPLIANT"
        )

    # =========================
    # REMARKS
    # =========================

    remarks = re.search(

        r"(?:Remarks|Observation).*?(.*?)(?:Authorized|Signature|Dr\.|$)",

        clean_text,

        re.IGNORECASE | re.DOTALL
    )

    if remarks:

        data["remarks"] = (
            remarks.group(1).strip()[:500]
        )

    return data