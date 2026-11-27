
# Delivery Performance Dashboard

A data analytics project that analyzes delivery performance across different regions and delivery statuses. The dashboard helps identify delivery trends, compare regional performance, and monitor delivery outcomes using interactive visualizations.

## Project Overview

This project focuses on analyzing a delivery logistics dataset containing 25,000 delivery records.

The objective is to transform raw delivery data into meaningful insights through data cleaning, SQL analysis, and an interactive dashboard.

## Key Features

- Total delivery count and delivery status KPIs
- Regional performance analysis
- Delivery status distribution
- Interactive region filter
- Dynamic dashboard insights
- Responsive dashboard layout
- Backend API integration with PostgreSQL

## Technologies Used

### Data Analytics
- PostgreSQL
- SQL
- Data Cleaning
- Data Analysis

### Backend
- Python
- FastAPI
- psycopg2

### Frontend
- React
- Vite
- Recharts
- CSS

## Dataset

The project uses a delivery logistics dataset containing 25,000 records.

The dataset includes information such as:
- Delivery records
- Delivery partners
- Regions
- Delivery status
- Delivery-related attributes

## Data Quality Note

The original dataset contains invalid values in the delivery time and expected delivery time columns.

These columns were identified during data cleaning and were not used for time-based KPI calculations.

Therefore, this dashboard focuses on delivery volume, delivery status, and regional performance rather than delivery duration or on-time delivery rate.

## Dashboard Insights

The dashboard provides insights into:

- Total deliveries
- Delivered, delayed, and failed deliveries
- Regional delivery volume
- Delivery status distribution
- Region-wise performance comparison

## Project Structure

```text
Delivery Performance Dashboard/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   └── package.json
│
├── Data/
│   └── Cleaned/
│
├── sql/
│   ├── 01_create_database_tables.sql
│   └── 02_delivery_analysis_queries.sql
│
└── README.md
```

## How to Run the Project

### 1. Start the Backend

Open a terminal in the backend folder:

```bash
cd backend
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
python -m uvicorn main:app --reload
```

Backend URL:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

### 2. Start the Frontend

Open another terminal in the frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend URL:

http://localhost:5173

## Learning Outcomes

Through this project, I practiced:

- Cleaning and validating real-world data
- Working with PostgreSQL
- Writing SQL queries for analysis
- Building backend APIs using FastAPI
- Connecting a React frontend to a backend
- Creating interactive charts and KPIs
- Presenting data through a dashboard

## Author

Sanika Parate

B.Tech Computer Science

Aspiring Data Analyst
