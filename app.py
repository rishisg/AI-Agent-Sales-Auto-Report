import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from database import Database
from email_service import EmailService
from prompt_parser import parse_prompt
import logging
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

# Load environment variables
load_dotenv()

# Initialize services
db = Database()
email = EmailService()

recipient_email = os.getenv("EMAIL_RECEIVER")  # ✅ Load recipient email dynamically from .env

# ✅ Ensure the scheduler is initialized correctly
if "scheduler" not in st.session_state:
    st.session_state.scheduler = BackgroundScheduler()

def scheduled_task():
    """Automated task to fetch reports and send emails"""
    print("⏳ Scheduled task is running...")
    user_prompt = "Show total sales for each product from the database."  
    report_data = db.generate_report(user_prompt, "Database")
    
    if report_data is not None and not report_data.empty:
        email.send_report(report_data, "Scheduled Sales Report", recipient_email)
    else:
        print("❌ No data found for scheduled report.")

# UI Setup
st.set_page_config(page_title="📊 Sales Report Automator", page_icon="🤖", layout="wide")
st.title("🤖 Sales Report Automation Agent")

# Sidebar for System Status
st.sidebar.subheader("System Status")
st.sidebar.write(f"⏱️ Interval: {st.session_state.get('ui_interval', 5)} mins")
st.sidebar.write(f"📋 Scheduler: {st.session_state.get('scheduler_status', 'Stopped')}")
st.sidebar.write(f"📝 Report Type: {st.session_state.get('ui_report_type', 'summary')}")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Select Data Source")
    data_source = st.radio("Choose Data Source:", ("Database", "CSV"), key="data_source_radio")

    uploaded_file = None
    if data_source == "CSV":
        st.subheader("Upload CSV File")
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    st.subheader("Manual Report Generation")
    selected_report_type = st.selectbox("Select Report Type", ("summary", "by_product", "sales_trends", "top_products"), key="ui_report_type")

    if st.button("Generate Report"):
        report_data = db.generate_report(selected_report_type, data_source.lower(), uploaded_file)
        if report_data is not None and not report_data.empty:
            st.subheader(f"Generated {selected_report_type.capitalize()} Report:")
            st.dataframe(report_data)

            # ✅ Save Chart as Image for Email Attachment
            chart_filename = None

            if selected_report_type == "by_product":
                chart_filename = "sales_by_product.png"
                fig, ax = plt.subplots()
                sns.barplot(x=report_data["product"], y=report_data["total_sales"], ax=ax)
                ax.set_xlabel("Product")
                ax.set_ylabel("Total Sales")
                ax.set_title("Total Sales by Product")
                fig.savefig(chart_filename)  # ✅ Save chart as image
                st.pyplot(fig)

            elif selected_report_type == "sales_trends":
                chart_filename = "sales_trend.png"
                fig, ax = plt.subplots()
                sns.lineplot(x=report_data["date"], y=report_data["total_sales"], ax=ax)
                ax.set_xlabel("Date")
                ax.set_ylabel("Total Sales")
                ax.set_title("Daily Sales Trends")
                fig.savefig(chart_filename)  # ✅ Save chart as image
                st.pyplot(fig)

            elif selected_report_type == "top_products":
                chart_filename = "top_products.png"
                fig, ax = plt.subplots()
                sns.barplot(x=report_data["product"], y=report_data["total_sales"], ax=ax)
                ax.set_xlabel("Product")
                ax.set_ylabel("Total Sales")
                ax.set_title("Top Products by Sales")
                fig.savefig(chart_filename)  # ✅ Save chart as image
                st.pyplot(fig)

            # ✅ Send report & visualization via email
            email_subject = f"{selected_report_type.capitalize()} Report"
            email_sent = email.send_report(report_data, email_subject, recipient_email, chart_filename)
            if email_sent:
                st.success(f"Report and visualization sent to {recipient_email} successfully!")
            else:
                st.error("Failed to send the report and visualization via email.")
        else:
            st.error(f"No data found for report type '{selected_report_type}'.")

    st.subheader("Natural Language Prompt")
    user_prompt = st.text_area("Enter request (e.g., 'Show total sales grouped by region.')", key="user_prompt")

    if st.button("Generate Report from Prompt"):
        report_type = parse_prompt(user_prompt)
        report_data = db.generate_report(report_type, data_source.lower())
        if report_data is not None and not report_data.empty:
            st.subheader(f"Generated {report_type.capitalize()} Report:")
            st.dataframe(report_data)

            # ✅ Save Chart as Image for Email Attachment
            chart_filename = None

            if "sales" in report_data.columns and "date" in report_data.columns:
                chart_filename = "sales_trend_prompt.png"
                fig, ax = plt.subplots()
                sns.lineplot(x=report_data["date"], y=report_data["sales"], ax=ax)
                ax.set_xlabel("Date")
                ax.set_ylabel("Total Sales")
                ax.set_title("Daily Sales Trends")
                fig.savefig(chart_filename)  # ✅ Save chart as image
                st.pyplot(fig)

            elif "product" in report_data.columns and "total_sales" in report_data.columns:
                chart_filename = "sales_by_product_prompt.png"
                fig, ax = plt.subplots()
                sns.barplot(x=report_data["product"], y=report_data["total_sales"], ax=ax)
                ax.set_xlabel("Product")
                ax.set_ylabel("Total Sales")
                ax.set_title("Total Sales by Product")
                fig.savefig(chart_filename)  # ✅ Save chart as image
                st.pyplot(fig)

            # ✅ Send report & visualization via email with fixed subject formatting
            email_subject = "Generated Report"
            email_sent = email.send_report(report_data, email_subject, recipient_email, chart_filename)
            if email_sent:
                st.success(f"Report and visualization sent to {recipient_email} successfully!")
            else:
                st.error("Failed to send the report and visualization via email.")
        else:
            st.error(f"No data found for report type '{report_type}'.")

with col2:
    st.subheader("Scheduler Control")
    interval = st.number_input("Interval (minutes)", min_value=1, value=st.session_state.get("ui_interval", 5))

    if st.button("Start Scheduler"):
        if not st.session_state.scheduler.running:
            st.session_state.scheduler.add_job(scheduled_task, 'interval', minutes=interval)
            st.session_state.scheduler.start()
            st.session_state["scheduler_status"] = "Running"
            st.sidebar.write("📋 Scheduler: Running")
            print("✅ Scheduler started!")
        else:
            print("⚠️ Scheduler is already running.")

    if st.button("Stop Scheduler"):
        if st.session_state.scheduler.running:
            st.session_state.scheduler.remove_all_jobs()  # ✅ Ensures all jobs are removed
            st.session_state.scheduler.shutdown(wait=False)  # ✅ Immediately stops the scheduler
            st.session_state["scheduler_status"] = "Stopped"
            st.sidebar.write("📋 Scheduler: Stopped")
            print("❌ Scheduler stopped successfully!")
        else:
            print("⚠️ Scheduler is not running, no need to stop it.")
