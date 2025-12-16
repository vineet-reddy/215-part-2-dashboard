# ClearSkin Dash OLAP Dashboard (Azure Postgres)

## What this is
A Dash dashboard that connects to Azure PostgreSQL and loads OLAP data (schema: `olap`) on startup.
Includes filters + KPIs + 4 charts.

## Quick Start (Easiest Way)

1.  **Configure Environment**:
    -   Create a `.env` file in this directory.
    -   Add your database password: `PGPASSWORD=your_actual_password_here`.
    -   (See `.env.example` or ask admin if you need other connection details).

2.  **Run the Script**:
    -   Open your terminal in this directory.
    -   Run: `sh run_dashboard.sh`
    -   This script automatically creates a virtual environment, installs dependencies, and launches the dashboard.

3.  **View Dashboard**:
    -   Open your browser to `http://127.0.0.1:8050`.

---

## Manual Setup (If you prefer)

1.  **Prerequisites**:
    -   Python 3.10+ installed.
    -   Access to the Azure PostgreSQL database.

2.  **Environment Setup**:
    ```bash
    # Create virtual environment
    python3 -m venv venv

    # Activate virtual environment
    # Mac/Linux:
    source venv/bin/activate
    # Windows:
    # venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Secrets**:
    -   Ensure `.env` exists with `PGHOST`, `PGUSER`, `PGDATABASE`, and `PGPASSWORD`.

5.  **Run Application**:
    ```bash
    python app.py
    ```

## Screenshots for submission
- Take screenshots showing filters (date/clinic/channel/specialty/payer) and how charts/KPIs change.
