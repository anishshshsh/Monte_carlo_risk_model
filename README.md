# **Investment Banking Risk Modeling Tool with Monte Carlo Simulation**

This project implements a **Monte Carlo simulation** for **risk scoring and visualization** in an investment banking context.
It allows you to:

* Load and score risk data
* Simulate uncertainties using Monte Carlo methods
* Visualize results via heatmaps and top-risk charts
* Export processed data for further analysis

---

## **Project Structure**

```
.
├── data/
│   └── risks.csv               # Input risk data
├── outputs/
│   ├── risks_scored.csv        # Scored and categorized risks
│   ├── risk_heatmap.png        # Heatmap visualization
│   └── top_risks.png           # Top risks bar chart
├── src/
│   ├── monte_carlo.py          # Monte Carlo simulation logic
│   ├── risk_model.py           # Risk scoring logic
│   ├── visualizations.py       # Visualization functions
│   └── report.py               # PDF report generation
├── streamlit_app.py            # Streamlit UI entry point
├── requirements.txt            # Dependencies
├── README.md                   # Project documentation
└── main.py                     # CLI entry point (optional)
```

---

## **Getting Started**

### 1️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

### 2️⃣ Run the Streamlit App

```sh
streamlit run streamlit_app.py
```

---

## **Data Format**

The **input file** should be `data/risks.csv` with columns such as:

* `Risk Name` — Identifier for the risk
* `Base Exposure` — Initial exposure amount
* `Probability` — Likelihood of occurrence (0–1)
* `Impact` — Severity of the impact

Example:

```csv
Risk Name,Base Exposure,Probability,Impact
Credit Risk,5000000,0.2,0.8
Market Risk,3000000,0.3,0.6
Operational Risk,2000000,0.1,0.4
```

---

## **Outputs**

* **`outputs/risks_scored.csv`** — Processed file with calculated scores.
* **`outputs/risk_heatmap.png`** — Heatmap of risk categories.
* **`outputs/top_risks.png`** — Bar chart of the top risks.

## **Core Features**

* **Monte Carlo Simulation**: Estimates potential risk impact by running multiple randomized trials.
* **Risk Scoring**: Scores risks based on probability and impact.
* **Interactive Dashboard**: Streamlit app for exploring results.
* **Exportable Reports**: Saves charts and scored data.

---

## **Monte Carlo Simulation Overview**

Monte Carlo simulation runs thousands of trials, each randomly varying risk parameters within their defined ranges.
The results are aggregated to estimate **average exposure** and **possible loss distribution**.

General formula for simulation:

$$
{Simulated Exposure} = {Base Exposure} * { 1 + Random Factor}
$$

Where the random factor is drawn from a probability distribution (e.g., normal, uniform).

---
## How It Works

1. **Data Input**: Load risk data from a CSV file.
2. **Risk Scoring**: Calculate risk scores based on predefined criteria.
3. **Monte Carlo Simulation**: Run simulations to model potential risk scenarios.
4. **Visualization**: Generate heatmaps and charts to visualize results.
5. **Reporting**: Export findings to CSV and PDF formats.

---
## License
This project is open-source under the MIT License.

---