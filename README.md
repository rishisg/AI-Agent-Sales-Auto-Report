# AI Agent for Automated Report Generation 🚀

## 1📌 Overview
The **AI Agent for Automated Report Generation** is a powerful automation tool designed to **eliminate manual reporting work** by dynamically generating reports from databases and CSV files. Users can provide **natural language prompts**, and the system intelligently **processes the request**, retrieves relevant data, and generates structured reports. It also supports **scheduled automatic reports** and **email delivery**, ensuring a smooth workflow.

---

## ✅ Client Requirements & Solution
### **Client's Requirements**
1️⃣ **Extract data from databases or spreadsheets** to generate reports  
2️⃣ **Allow users to provide prompts or filters** for dynamic report creation  
3️⃣ **Automate report generation (via scheduling)**  
4️⃣ **Send reports via email after generation**  
5️⃣ **Ensure an intuitive and fast user interface**  
6️⃣ **Provide relevant data visualizations when necessary**  

### **Solution Implemented**
✔ **Database & File Handling** – Fetches structured data from MySQL and CSV files  
✔ **AI-Powered Query Processing** – Uses **OpenAI GPT** to convert prompts into SQL queries  
✔ **Automated Scheduling** – Uses **APScheduler** for scheduled report automation  
✔ **Email Delivery System** – Sends **CSV reports & visualization images** via SMTP  
✔ **Streamlit Web UI** – Provides an **interactive, user-friendly interface**  
✔ **Data Visualization** – Generates **charts using Matplotlib & Seaborn**  

---

## 📌 Features
✅ **Natural Language Prompt-Based Reports** – AI understands and generates reports automatically  
✅ **Manual Report Generation** – Users can select predefined report types  
✅ **Database & CSV File Integration** – Fetch reports from **structured databases or uploaded CSV files**  
✅ **Automated Report Scheduling** – Set up scheduled reports with **APSheduler**  
✅ **Email Automation** – Sends **CSV reports & visualization images via email**  
✅ **Data Visualization** – Generates **charts for relevant reports**  

---

## 🛠️ Tech Stack
- **Python** – Core development language  
- **Streamlit** – Web UI framework  
- **OpenAI GPT** – AI-powered query processing  
- **MySQL & Pandas** – Database & CSV handling  
- **APScheduler** – Report automation & scheduling  
- **SMTP** – Email reports automatically  
- **Matplotlib & Seaborn** – Data visualization  

---

## 📥 Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-repo/ai-report-agent.git
cd ai-report-agent


2️⃣ Install Dependencies
pip install -r requirements.txt


3️⃣ Set Up .env File (Environment Variables)
Create a .env file with:
DB_HOST=your-database-host
DB_USER=your-database-user
DB_PASS=your-database-password
DB_NAME=report_db
EMAIL_SENDER=your-email@example.com
EMAIL_PASSWORD=your-email-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
OPENAI_API_KEY=your-openai-api-key


4️⃣ Run the Application
streamlit run app.py


📊 Usage Guide
Generating a Manual Report
Open the web app (localhost:8501)

Select Database or CSV as the data source

Choose the report type (Summary, By Product, Sales Trends, Top Products)

Click "Generate Report"

Report is displayed on the screen and sent via email

Generating an AI-Prompt Report
Enter a natural language request (e.g., "Show total sales grouped by region")

Click "Generate Report from Prompt"

AI processes the query and retrieves the report

Report appears on the screen and is emailed

Automating Scheduled Reports
Set a report interval (minutes)

Click "Start Scheduler"

Reports are auto-generated based on interval settings

Click "Stop Scheduler" to disable automation

📷 Screenshots
Web UI Dashboard

Sample Report Output

Generated Chart

🔧 Troubleshooting & Debugging
Email Not Sending?
✔️ Check SMTP settings in .env ✔️ Verify email sender authentication

Scheduler Not Running?
✔️ Make sure APSheduler is installed ✔️ Restart Streamlit after setting an interval

AI Prompt Not Working?
✔️ Verify OpenAI API Key ✔️ Check if SQL query generation is correct

🚀 Future Enhancements
✅ Multi-Database Support – Extend compatibility for PostgreSQL, SQLite, etc. ✅ PDF & Excel Exports – Generate reports in PDF & Excel formats ✅ Enhanced UI – Interactive dashboard for easier selection & filtering ✅ User Authentication – Secure login system for different access levels

📞 Contact & Support
💡 Need Help? Reach Out! 📧 Email: support@example.com 🌐 GitHub: Repo Link

🚀 Enjoy automated reporting with AI efficiency! 🔥