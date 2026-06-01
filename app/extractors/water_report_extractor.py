import re


def extract_water_report_data(text):

    data = {}

    company = re.search(
        r"Company Name:\s*(.*)",
        text
    )

    sample_type = re.search(
        r"Sample Type:\s*(.*)",
        text
    )

    collection_date = re.search(
        r"Collection Date:\s*(.*)",
        text
    )

    analysis_date = re.search(
        r"Analysis Date:\s*(.*)",
        text
    )

    ph = re.search(
        r"pH\s+(\d+\.?\d*)",
        text
    )

    tds = re.search(
        r"TDS\s+(\d+\.?\d*)",
        text
    )

    cod = re.search(
        r"COD\s+(\d+\.?\d*)",
        text
    )

    bod = re.search(
        r"BOD\s+(\d+\.?\d*)",
        text
    )

    status = re.search(
        r"Overall Status:\s*(.*)",
        text
    )

    remarks = re.search(
        r"Remarks:\s*(.*?)(?:Dr\.|Chief|$)",
        text,
        re.DOTALL
    )

    data["company_name"] = company.group(1).strip() if company else None
    data["sample_type"] = sample_type.group(1).strip() if sample_type else None
    data["collection_date"] = collection_date.group(1).strip() if collection_date else None
    data["analysis_date"] = analysis_date.group(1).strip() if analysis_date else None

    data["ph"] = float(ph.group(1)) if ph else None
    data["tds"] = float(tds.group(1)) if tds else None
    data["cod"] = float(cod.group(1)) if cod else None
    data["bod"] = float(bod.group(1)) if bod else None

    data["overall_status"] = status.group(1).strip() if status else None
    data["remarks"] = remarks.group(1).strip() if remarks else None

    return data