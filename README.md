\# Smart Environmental Compliance Management System



\## About the Project



Smart Environmental Compliance Management System is a web-based application developed to help industries manage their environmental compliance reports in one place. Companies can register, add their company and CTO details, and upload Water and Air laboratory reports as PDF files. The system extracts the required values from the uploaded reports, checks them against the permissible limits, calculates a compliance score, and displays the results through a dashboard. Previous reports are stored so that companies can view their compliance history and track their performance over different reporting periods.



\## Features



\- User Registration and Login

\- OTP Verification

\- Company Details Management

\- Industry and Production Details

\- CTO Details Management

\- Water Report Upload

\- Air Report Upload

\- PDF Text Extraction

\- Automatic Environmental Data Extraction

\- Water Compliance Analysis

\- Air Compliance Analysis

\- Compliance Score Calculation

\- Compliance Alerts

\- Dashboard with Compliance Summary

\- Previous Report History

\- Compliance Trend Graph

\- Environmental Compliance Report Generation



\## Water Report Analysis



The system extracts important parameters from Water Quality laboratory reports such as:



\- pH

\- TDS

\- COD

\- BOD

\- TSS

\- Chloride

\- Sulphate

\- Oil \& Grease



The extracted values are compared with their permissible limits and the system identifies parameters that are within or above the limit.



\## Air Report Analysis



The system extracts parameters from Industrial Air Quality reports such as:



\- PM2.5

\- PM10

\- SO2

\- NOx

\- CO



These values are checked against their respective permissible limits and a compliance score is calculated.



\## How the System Works



```text

User Registration

&#x20;      ↓

Login / OTP Verification

&#x20;      ↓

Add Company \& CTO Details

&#x20;      ↓

Upload Water / Air Report

&#x20;      ↓

Extract Text from PDF

&#x20;      ↓

Extract Environmental Values

&#x20;      ↓

Check Permissible Limits

&#x20;      ↓

Calculate Compliance Score

&#x20;      ↓

Save Report Data

&#x20;      ↓

Dashboard

&#x20;      ↓

View Previous Reports

&#x20;      ↓

View Compliance Trends

&#x20;      ↓

Generate Compliance Report

Technology Stack
Backend
Python
FastAPI
SQLAlchemy
PyMySQL
Uvicorn
Database
MySQL
MySQL Workbench
Frontend
HTML
CSS
JavaScript
Jinja2
Other Tools
Git & GitHub
Postman
Swagger UI
Project Structure
backend/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── pdf_utils.py
│   ├── compliance_engine.py
│   │
│   ├── extractors/
│   │   ├── water_report_extractor.py
│   │   └── air_report_extractor.py
│   │
│   └── routes/
│       ├── document_routes.py
│       ├── dashboard_routes.py
│       └── report_routes.py
│
├── templates/
│   └── compliance_report.html
│
├── uploads/
├── reports/
├── requirements.txt
└── README.md
Database

MySQL is used to store user, company, document, and compliance report information.

Main tables include:

users
otp_verifications
documents
extracted_reports
compliance_reports

Each uploaded document is connected with the respective user/company.

API

Some of the main APIs are:

POST /api/documents/upload
GET  /api/documents/all
GET  /api/documents/extract/{document_id}
GET  /api/documents/analyze/{document_id}
GET  /api/documents/summary
GET  /api/dashboard/compliance-trends
GET  /api/reports/preview
Running the Project

Create a virtual environment:

python -m venv .venv

Activate it:

.venv\Scripts\activate

Install the required packages:

pip install -r requirements.txt

Create the MySQL database:

CREATE DATABASE compliance_db;

Configure the database connection in the .env file.

Run the backend:

uvicorn app.main:app --reload

Open Swagger API documentation:

http://127.0.0.1:8000/docs
Future Improvements
Improve AI-based document understanding
Add Waste Report processing
Add ESG reporting
Add more environmental parameters
Improve compliance report PDF design
Add automated compliance notifications
Connect real-time environmental sensors
Complete automated regulatory report submission
Project Purpose

The main idea of this project is to reduce the manual work involved in checking environmental laboratory reports and help industries monitor their compliance through a single platform.
