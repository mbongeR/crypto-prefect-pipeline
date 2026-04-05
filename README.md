# 📈 Live Crypto Market Tracker (Orchestrated with Prefect)

A robust, self-monitoring data pipeline built in Python that fetches live cryptocurrency prices, analyzes market ratios, and alerts administrators upon failure. This project was built to explore data orchestration, scheduling, and error handling using **Prefect**.

## 🛠️ Tech Stack
* **Language:** Python
* **Orchestration:** Prefect 2.x
* **Data Source:** CoinGecko API
* **Libraries:** `httpx`, `asyncio`, `prefect-email`

## 🚀 Key Features
* **Scheduled Data Ingestion:** Automatically fetches live prices for Bitcoin, Ethereum, Solana, Cardano, Ripple, and Polkadot at regular intervals.
* **Resilient Execution:** Implements `@task` level retries (2 retries, 5-second delay) to handle temporary network blips or API rate limits.
* **Automated Failure Alerting:** Uses Prefect State Hooks (`on_failure`) and Secure Blocks to automatically trigger an email alert if the pipeline crashes, ensuring zero silent failures.
* **Decoupled Architecture:** The deployment pulls code directly from this GitHub repository, allowing any authorized Prefect Worker to execute the pipeline regardless of the local environment.

## ⚙️ How It Works
1. **Fetch Task:** Hits the CoinGecko API in a single efficient HTTP request.
2. **Analysis Task:** Parses the JSON response, formats the prices, and calculates the live BTC/ETH purchasing ratio.
3. **Orchestration Flow:** Manages the execution state. If a critical error occurs, it intercepts the `Failed` state and executes the `send_failure_alert` hook to notify the admin via SMTP.

## 🧑‍💻 Running It Locally

**1. Clone the repository**
```bash
git clone [https://github.com/mbongeR/crypto-prefect-pipeline.git](https://github.com/mbongeR/crypto-prefect-pipeline.git)
cd crypto-prefect-pipeline 
pip install -r requirements.txt
prefect server start
prefect worker start --pool "my-local-pool"
python market_tracker.py
