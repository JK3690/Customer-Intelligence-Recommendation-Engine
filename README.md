# Customer Intelligence & Recommendation Engine

## Overview

Transform customer data into prioritized segments, actionable recommendations, and explainable business insights.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

---
## Live Demo

Try the app:

https://customer-intelligence-recommendation-engine-jk3690.streamlit.app/

Deployed using Streamlit Community Cloud.

---
## Key Capabilities

* Customer segmentation based on behavioral patterns
* Quantile-based value scoring
* Priority ranking using weighted scoring
* Action recommendation engine (segment + priority aware)
* Human-readable insights with reasoning
* CLI support for querying individual customers
* Exportable results for downstream use
* Interactive dashboard (Streamlit)

---
## Screenshots / Output

<img width="1462" height="751" alt="Customer Analysis" src="https://github.com/user-attachments/assets/dd8ab11e-af8b-4e08-b7d2-d06646d8d334" />
<img width="2128" height="1175" alt="Bar Charts" src="https://github.com/user-attachments/assets/f099e737-88e9-465f-8dbf-86abce8fdaa6" />
<img width="2495" height="802" alt="Filtered Table" src="https://github.com/user-attachments/assets/481103f6-9f0c-4e5a-adcb-8daa574c638f" />

### Example Output

Customer ID: 663

Segment: High Value Customer

Priority: Priority 1

Insight: Customer has a score of 4.10, placing them in Priority 1, and is a High Value Customer with High Score value and High frequency. 

Recommended action: VIP Treatment.

---
## Run Locally

pip install -r requirements.txt

streamlit run source/app.py

---

## CLI Usage

Run the pipeline:

```bash
python source/main.py
```

Query a specific customer:

```bash
python source/main.py --customer_id 100
```
---

## Project Structure

```text
Customer Intelligence & Recommendation Engine/
├── data/
│   └── shopping_trends.csv
├── outputs/
│   └── customer_insights.csv
├── source
│   └── main.py
│   └── app.py
├── README.md
├── requirements.txt
```

---
## System Design / How It Works

The pipeline transforms raw transaction data into decisions:

```text
Raw Data → Feature Engineering → Scoring → Priority → Segmentation → Actions → Insights
```

### Core Logic

* **Value Score** = Purchase Amount × Previous Purchases

* **Final Score** = weighted combination of:

  * Spend score
  * Frequency score
  * Value score

* **Priority Levels**

  * Top 10% → Priority 1
  * Next 15% → Priority 2
  * Remaining → Priority 3

* **Decision Layer**

  * Combines segment + priority
  * Produces targeted business actions

---

## Why This Project

This project focuses on:

* decision-making
* prioritization
* explainability

It simulates how businesses:

* identify high-value customers
* allocate resources
* design targeted strategies

---

## Future Improvements

* API layer (Flask / FastAPI)
* LLM-based dynamic insight generation
* Real-time data integration

---

## Author
Jeevika Kapoor

Interested in building data-driven systems that translate raw data into actionable decisions.
