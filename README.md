# 🏢 AI-Powered Predictive Analytics & Dynamic RAG System for NGOs

An advanced, end-to-end local data engine built to optimize financial and operational workflows for non-profit organizations and NGOs. This dynamic solution bridges the gap between raw data entry, business intelligence, and responsive conversational AI.

---

## 🚀 Key Features

- **📥 Dual-Input Dynamic Data Management:** A 100% stable **Python + Streamlit** web interface enabling dual CRUD operations. Users can seamlessly insert/update donor profiles and beneficiary family needs into an isolated **SQLite** database locally in fractions of a second.
- **📊 Business Intelligence & Predictive Analytics (Power BI Simulation):** Implements automated multi-criteria sorting to evaluate **Churn Risk Analytics**. It isolates high-risk donors (dormant > 6 months, engagement rate < 40%) to proactively mitigate upcoming cash-flow deficits.
- **👥 Beneficiary & Aid Matrix Monitoring:** Integrated live data frames parsing total covered families, total supported members, and automated **Plotly** chart updates mapping geographical distribution and cash requirement ratios.
- **💬 Tab 4: The Advanced AI Chatbot:** A keyphrase-based dynamic search engine that dynamically binds donor contributions to beneficiary demands, automatically computing the organization's **Financial Coverage Ratio** and outputting actionable strategic management suggestions.

---

## 🛠️ Built with the Professional Local Stack

- **Frontend:** Streamlit Web UI (Configured with RTL Arabic interface support)
- **Database:** SQLite3 Relational Database Engine
- **Data Wrangling:** Pandas DataFrames
- **Data Visualization:** Plotly Express & Plotly Graph Objects

---

## 📂 Architecture & Mapped Files

```text
📁 charity_central_project/
│
├── 📁 venv/                 # Isolated Python virtual environment
├── 📄 rag_bot.py            # Main full-stack application script 
├── 📄 charity_central.db    # Dynamic local SQLite relational database 
└── 📄 README.md             # Systems documentation file
```

---

## 💻 Technical Setup & Installation

To run this platform completely offline and independent of external server restrictions, execute the following commands in your local workspace terminal:

### 1. Initialize and Activate the Isolated Workspace
```bash
cd charity_central_project
python -m venv venv
# For Windows
venv\Scripts\activate
# For Mac/Linux
source venv/bin/activate
```

### 2. Install Core Dependencies
```bash
pip install streamlit pandas plotly
```

### 3. Run the Production Server
```bash
streamlit run rag_bot.py
```
Once initialized, the platform will automatically boot an adaptive viewport inside your default browser at `http://localhost:8501`.

---

## 🧠 Business Logic Framework (Sample Interview Prompts)

- **Financial Coverage Ratio Mapping:**
$$\text{Coverage Ratio} = \left( \frac{\sum \text{Total Received Inflow}}{\sum \text{Total Required Outflow}} \right) \times 100$$
If the generated value slips under 100%, Tab 4 automatically flags a system warning calculates the localized deficit, and suggests target re-engagement channels.

---

## 🎯 Career & Contact Information
I am actively open to career opportunities as a **Data Analyst / Reporting Officer / Power BI Developer**. 

- **Name:** [Your Full Name]
- **Email:** [Your Email Address]
- **LinkedIn:** [Your Profile Link]
