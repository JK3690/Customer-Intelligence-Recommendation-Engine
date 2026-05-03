# Customer Intelligence & Recommendation Engine

## Overview

A decision-focused system that analyzes customer purchase behavior, segments users, ranks them by value, and generates **actionable, explainable recommendations**.

Unlike basic analytics projects, this system prioritizes **business decisions**.

---

## Key Capabilities

* Customer segmentation based on behavioral patterns
* Quantile-based value scoring
* Priority ranking using weighted scoring
* Action recommendation engine (segment + priority aware)
* Human-readable insights with reasoning
* CLI support for querying individual customers
* Exportable results for downstream use

---

## How It Works

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

## Example Output

Customer ID: 663

Segment: High Value Customer

Priority: Priority 1

Insight: Customer has a score of 4.10, placing them in Priority 1, and is a High Value Customer with High Score value and High frequency. 

Recommended action: VIP Treatment.

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

Output includes:

* segment
* priority
* recommended action
* explanation

---

## Project Structure

```text
project/
├── data/
│   └── shopping_trends.csv
├── outputs/
│   └── customer_insights.csv
├── source
│   └── main.py
├── README.md
├── requirements.txt
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Tech Stack

* Python
* Pandas
* Plotly

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
* Dashboard / web interface
* Real-time data integration

---

## Author
Jeevika Kapoor

Interested in building data-driven systems that translate raw data into actionable decisions.