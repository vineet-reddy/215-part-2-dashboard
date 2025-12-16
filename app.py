"""ClearSkin Dashboard: Dash app connected to Azure OLAP"""

from pathlib import Path
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

from db import make_engine, test_connection, read_sql_file

# Setup
BASE_DIR = Path(__file__).resolve().parent
SQL_DIR = BASE_DIR / "sql"

ENGINE = make_engine()
test_connection(ENGINE)

# Load data from OLAP
def load_data():
    appt_sql = read_sql_file(str(SQL_DIR / "appointments.sql"))
    inv_sql = read_sql_file(str(SQL_DIR / "invoices.sql"))
    
    df_appt = pd.read_sql(appt_sql, ENGINE)
    df_inv = pd.read_sql(inv_sql, ENGINE)
    
    df_appt["full_date"] = pd.to_datetime(df_appt["full_date"])
    df_inv["invoice_date"] = pd.to_datetime(df_inv["invoice_date"])
    
    return df_appt, df_inv

DF_APPT, DF_INV = load_data()
clinic_options = sorted(DF_APPT["clinic_name"].dropna().unique().tolist())

# Dash app
app = dash.Dash(__name__, title="ClearSkin Dashboard")

app.layout = html.Div([
    html.H1("ClearSkin Dashboard"),
    
    html.Label("Filter by Clinic:"),
    dcc.Dropdown(
        id="clinic_filter",
        options=[{"label": c, "value": c} for c in clinic_options],
        value=clinic_options,
        multi=True
    ),
    
    html.Br(),
    
    # KPIs
    html.Div(id='kpis'),
    
    html.Br(),
    
    # Charts - 3 in a row
    html.Div([
        dcc.Graph(id="fig1", style={"width": "33%", "display": "inline-block"}),
        dcc.Graph(id="fig2", style={"width": "33%", "display": "inline-block"}),
        dcc.Graph(id="fig3", style={"width": "33%", "display": "inline-block"}),
    ]),
])


@app.callback(
    [Output("kpis", "children"),
     Output("fig1", "figure"),
     Output("fig2", "figure"),
     Output("fig3", "figure")],
    [Input("clinic_filter", "value")]
)
def update(clinics):
    df_a = DF_APPT[DF_APPT["clinic_name"].isin(clinics)] if clinics else DF_APPT
    df_i = DF_INV[DF_INV["clinic_name"].isin(clinics)] if clinics else DF_INV
    
    # KPIs
    total_rev = df_i["total_charge"].sum()
    total_appts = len(df_a)
    completed = df_a["is_completed"].sum()
    cancelled = df_a["is_cancelled"].sum()
    
    kpis = html.Div([
        html.P(f"Total Revenue: ${total_rev:,.2f}"),
        html.P(f"Total Appointments: {total_appts}"),
        html.P(f"Completed: {completed} | Cancelled: {cancelled}")
    ])
    
    # Chart 1: Appointment Status by Clinic (simple bar)
    status_df = df_a.groupby(["clinic_name", "status"]).size().reset_index(name="count")
    fig1 = px.bar(status_df, x="clinic_name", y="count", color="status", barmode="group",
                  title="Appointment Status by Clinic")
    
    # Chart 2: Booking Channel (simple pie)
    channel_df = df_a.groupby("booking_channel").size().reset_index(name="count")
    fig2 = px.pie(channel_df, names="booking_channel", values="count",
                  title="Appointments by Booking Channel")
    
    # Chart 3: Revenue by Clinic - stacked by payer type
    rev_df = df_i.groupby("clinic_name")[["insurance_portion", "patient_portion"]].sum().reset_index()
    rev_df = rev_df.melt(id_vars="clinic_name", var_name="payer", value_name="amount")
    fig3 = px.bar(rev_df, x="clinic_name", y="amount", color="payer", barmode="stack",
                  title="Revenue by Clinic (Insurance vs Patient)")
    
    return kpis, fig1, fig2, fig3


if __name__ == "__main__":
    app.run_server(debug=True)
