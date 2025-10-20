# CloudWalk Operations Intelligence Analysis

**Technical Challenge - Operations Intelligence Analyst Position**

##  Project Overview

This project analyzes CloudWalk's payment processing transaction data (Q1 2025) to provide strategic insights on Total Payment Volume (TPV), transaction patterns, and business performance. The analysis includes KPI calculations, visualizations, and an AI-powered monitoring bot proposal.

**Analysis Period:** January 1 - March 31, 2025  
**Dataset:** 37,787 aggregated records | 146.5M transactions | R$ 19.4B TPV

---

##  Objectives

1. **Business KPIs Analysis**
   - Calculate and visualize TPV segmented by entity, product, and payment method
   - Analyze average ticket performance across segments
   
2. **Transactional Insights**
   - Understand how installment options impact transaction volume
   - Identify performance differences across price tiers
   
3. **Strategic Recommendations**
   - Provide actionable insights to support decision-making
   - Identify growth opportunities and operational improvements

4. **Automation Proposal**
   - Design AI-powered bot for daily TPV monitoring
   - Develop automated alert system for anomalies

---

##  Repository Structure

```
cloudwalk-operations-analysis/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── data/
│   └── operations_data.xlsx          # Original dataset
├── notebooks/
│   ├── 01_data_exploration.py        # Initial data analysis
│   ├── 02_kpi_analysis.py            # KPI calculations
│   └── 03_visualizations.py          # Chart generation
├── visualizations/
│   ├── images/                       # PNG charts
│   │   ├── 01_entity_analysis.png
│   │   ├── 02_product_tpv.png
│   │   ├── 03_payment_method.png
│   │   ├── 04_installments.png
│   │   ├── 05_weekday_analysis.png
│   │   ├── 06_price_tier.png
│   │   ├── 07_daily_trend.png
│   │   └── 08_entity_product_matrix.png
│   └── interactive/                  # Interactive HTML charts
│       ├── 01_tpv_by_entity.html
│       ├── 02_tpv_by_product.html
│       └── ... (10 total)
├── presentation/
│   └── CloudWalk_Operations_Analysis.pptx
└── docs/
    ├── ANALYSIS_REPORT.md            # Detailed findings
    └── AI_BOT_PROPOSAL.md            # Automation proposal

```

---

##  Key Findings

### **Executive Summary**
- **Total TPV:** R$ 19.44 Billion
- **Total Transactions:** 146.5 Million
- **Average Ticket:** R$ 132.72
- **Average Daily TPV:** R$ 216.0 Million

### **Entity Performance (PF vs PJ)**
| Entity | TPV | % Share | Avg Ticket |
|--------|-----|---------|------------|
| **PJ** | R$ 13.47B | 69.3% | R$ 108.95 |
| **PF** | R$ 5.97B | 30.7% | R$ 261.30 |

**Insight:** PF has 2.4x higher average ticket despite lower volume

### **Product Performance**
| Product | TPV | % Share | Avg Ticket |
|---------|-----|---------|------------|
| **POS** | R$ 8.24B | 42.4% | R$ 107.06 |
| **TAP** | R$ 6.25B | 32.2% | R$ 297.32 |
| **PIX** | R$ 2.48B | 12.7% | R$ 55.41 |
| **LINK** | R$ 2.43B | 12.5% | R$ 646.22 |
| **Bank Slip** | R$ 42.0M | 0.2% | R$ 741.79 |

**Insight:** TAP offers best balance of volume and value

### **Payment Method Distribution**
- **Credit Cards:** 74.2% of TPV (R$ 14.43B) - Avg ticket: R$ 318.46
- **Debit Cards:** 12.8% of TPV (R$ 2.49B) - Avg ticket: R$ 44.15
- **Uninformed:** 12.9% of TPV ( Data quality issue)

### **Installments Impact**
- **1x installment:** 44.9% of TPV but only R$ 64.70 avg ticket
- **10x installments:** 11.4% of TPV with R$ 2,243.26 avg ticket (35x higher!)
- **12x installments:** 8.3% of TPV with R$ 2,852.93 avg ticket (44x higher!)

**Critical Finding:** Strong positive correlation between installments and transaction value

### **Weekday Performance**
- **Weekdays:** 80% of TPV (R$ 15.55B)
- **Weekends:** 20% of TPV (R$ 3.90B)
- **Peak Day:** Thursday (R$ 3.31B)
- **Lowest Day:** Sunday (R$ 1.37B - 60% lower than peak)

---

##  Top Strategic Recommendations

### **1. Promote Long-Term Installments (10x, 12x)**
- **Impact:** +R$ 500M+ annually
- **Rationale:** Avg ticket 35-44x higher than single installment
- **Action:** Marketing campaign targeting PJ merchants

### **2. Expand TAP Product**
- **Impact:** +R$ 1B+ annually
- **Rationale:** Best balance of volume (32.2%) and avg ticket (R$ 297)
- **Action:** Aggressive merchant acquisition

### **3. Weekend Revenue Strategy**
- **Impact:** +R$ 800M+ annually
- **Rationale:** Sunday TPV is 60% lower than Thursday
- **Action:** Weekend promotions and merchant incentives

---

##  AI Bot Proposal

**Automated TPV Monitoring System**

### Features:
1. **Daily Morning Summary (8 AM BRT)**
   - TPV, transactions, and trend analysis
   - Growth comparisons vs previous day/week/month
   
2. **Real-Time Alerts**
   - Critical: TPV drops >20% in any segment
   - Warning: Declining trends (3+ days)
   - Opportunity: Surge detection
   
3. **Example Alert:**
```
CRITICAL ALERT - TPV SIGNIFICANT DROP

PJ Credit Card TPV down 28% vs yesterday
Current: R$ 82.3M | Expected: R$ 114.5M
Missing TPV: -R$ 32.2M

IMMEDIATE ACTIONS REQUIRED:
 Check system status and error logs
 Review top 50 merchants for unusual patterns
 Verify gateway connectivity
```

### Tech Stack:
- **Data Pipeline:** BigQuery/Postgres
- **Analysis:** Python + pandas
- **Anomaly Detection:** Statistical thresholds, Prophet forecasting
- **Delivery:** Slack API + Email
- **Dashboard:** Looker Studio

---

##  Tools & Technologies

- **Python 3.8+**
  - pandas (data manipulation)
  - plotly (interactive visualizations)
  - matplotlib/seaborn (static charts)
  - openpyxl (Excel processing)
  
- **Analysis Tools**
  - Jupyter Notebooks
  - Statistical analysis
  
- **Visualization**
  - Plotly (interactive HTML charts)
  - Matplotlib (static PNG images)
  - PowerPoint (presentation)

---

##  How to Run This Analysis

### **Prerequisites**
```bash
Python 3.8 or higher
pip (Python package manager)
```

### **Installation**

1. Clone this repository:
```bash
git clone https://github.com/yourusername/cloudwalk-operations-analysis.git
cd cloudwalk-operations-analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the analysis:
```bash
# Data exploration
python notebooks/01_data_exploration.py

# KPI calculations
python notebooks/02_kpi_analysis.py

# Generate visualizations
python notebooks/03_visualizations.py
```

### **Output**
- KPI summary printed to console
- PNG charts saved to `visualizations/images/`
- Interactive HTML charts saved to `visualizations/interactive/`

---

##  Methodology

### **Data Preparation**
- Dataset: 37,787 records covering 90 days
- No missing values detected
- Calculated metrics: TPV, Average Ticket, daily aggregations

### **Analysis Approach**
1. **Segmentation Analysis**
   - By entity (PF vs PJ)
   - By product (POS, TAP, PIX, LINK, Bank Slip)
   - By payment method (Credit, Debit, Uninformed)
   - By price tier (Normal, Aggressive, Intermediary, Domination)

2. **Time Series Analysis**
   - Daily trends
   - Weekly patterns
   - Day-of-week effects

3. **Behavioral Analysis**
   - Installment preferences
   - Anticipation method usage
   - Transaction patterns

### **Visualization Strategy**
- **Bar charts:** Comparative analysis
- **Line charts:** Trend analysis
- **Multi-panel dashboards:** Comprehensive views
- **Interactive HTML:** Deep-dive capabilities

---

##  Growth Projections

| Scenario | Initiatives | Annual TPV Increase | % Growth |
|----------|------------|-------------------|----------|
| **Conservative** | Priority 1 only | +R$ 1.8B | +9.3% |
| **Moderate** | Priority 1 + 2 | +R$ 3.2B | +16.5% |
| **Aggressive** | All priorities | +R$ 4.95B | +25.5% |

---

##  Key Business Questions Answered

 **Which product has highest TPV?** → POS (R$ 8.24B - 42.4%)  
 **Which has highest avg ticket?** → Bank Slip (R$ 741.79), then LINK (R$ 646.22)  
 **How do weekdays affect TPV?** → Weekdays = 80%, Weekend = 20%  
 **Which anticipation method per entity?** → PF: D0/Nitro (49.4%) | PJ: D1 (73.8%)  
 **Impact of installments?** → Strong correlation: more installments = higher value

---

##  Author

**[Your Name]**  
Operations Intelligence Analyst Candidate  
CloudWalk Technical Challenge - October 2025

---

##  License

This project was created for CloudWalk's technical challenge and contains proprietary business data. Not for public distribution.

---

##  Acknowledgments

- CloudWalk team for providing the dataset and challenge
- Python community for excellent data analysis libraries
- Plotly for powerful visualization capabilities

---

**Last Updated:** October 19, 2025
