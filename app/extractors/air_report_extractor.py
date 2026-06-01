import re

def extract_air_report_data(text):

    data = {}

    company = re.search(
        r"Company Name\s+(.*)",
        text
    )

    monitoring_date = re.search(
        r"Monitoring Date\s+(.*?)\n",
        text
    )

    pm_values = re.findall(
        r"PM.*?(\d+(?:\.\d+)?)\s*μg",
        text,
        re.DOTALL
    )

    so2 = re.search(
        r"Sulphur Dioxide\)\s*(\d+(?:\.\d+)?)",
        text
    )

    nox = re.search(
        r"Oxides of Nitrogen\)\s*(\d+(?:\.\d+)?)",
        text
    )

    co = re.search(
        r"Carbon Monoxide\)\s*(\d+(?:\.\d+)?)",
        text
    )

    status = re.search(
        r"STATUS\s+([A-Z\-]+)",
        text
    )

    remarks = re.search(
        r"REMARKS / OBSERVATIONS\s+(.*?)ECOAIR LAB",
        text,
        re.DOTALL
    )

    data["company_name"] = (
        company.group(1).strip()
        if company else None
    )

    data["monitoring_date"] = (
        monitoring_date.group(1).strip()
        if monitoring_date else None
    )

    data["pm25"] = (
        float(pm_values[0])
        if len(pm_values) > 0 else None
    )

    data["pm10"] = (
        float(pm_values[1])
        if len(pm_values) > 1 else None
    )

    data["so2"] = (
        float(so2.group(1))
        if so2 else None
    )

    data["nox"] = (
        float(nox.group(1))
        if nox else None
    )

    data["co"] = (
        float(co.group(1))
        if co else None
    )

    data["overall_status"] = (
        status.group(1).strip()
        if status else None
    )

    data["remarks"] = (
        remarks.group(1).strip()
        if remarks else None
    )

    return data