import httpx
import asyncio
from prefect import flow, task
from datetime import datetime, timedelta

# NEW IMPORTS FOR CACHING AND VARIABLES
from prefect.tasks import task_input_hash
from prefect.variables import Variable

from prefect_email import EmailServerCredentials, email_send_message

def send_failure_alert(flow, flow_run, state):
    print("🚨 Flow crashed! Sending email alert...")
    email_creds = EmailServerCredentials.load("my-alert-email")
    
    # 🌟 VARIABLE: Get email dynamically from the UI
    target_email = Variable.get("alert_email", default="n0235229g@students.nust.ac.zw")
    
    asyncio.run(
        email_send_message.fn(
            email_server_credentials=email_creds,
            subject=f"🚨 Prefect Alert: {flow.name} Failed!",
            msg=f"Hey! Your flow run '{flow_run.name}' just crashed. Can you check the logs!",
            email_to=target_email  
        )
    )

# 🌟 CACHING: Added cache_key_fn and cache_expiration
@task(
    retries=2, 
    retry_delay_seconds=5,
    cache_key_fn=task_input_hash, 
    cache_expiration=timedelta(minutes=1)
)
def fetch_all_prices(asset_ids: list) -> dict:
    print(f"Fetching live prices for {len(asset_ids)} coins in ONE request...")
    ids_string = ",".join(asset_ids)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_string}&vs_currencies=usd"
    
    response = httpx.get(url)
    response.raise_for_status() 
    data = response.json()
    
    flattened_data = {coin: info['usd'] for coin, info in data.items()}
    return flattened_data

@task
def analyze_market(market_data: dict):
    print("\n--- 📊 LIVE MARKET REPORT ---")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    for coin, price in market_data.items():
        print(f"{coin.capitalize()}: ${price:,.4f}")
        
    if "bitcoin" in market_data and "ethereum" in market_data:
        ratio = market_data["bitcoin"] / market_data["ethereum"]
        print(f"\nMarket Ratio: 1 BTC can currently buy {ratio:.2f} ETH")
    print("-----------------------------\n")

@flow(name="Live Crypto Market Tracker", log_prints=True, on_failure=[send_failure_alert])
def market_tracker_flow():
    
    # 🌟 VARIABLE: Fetch the list of coins from the UI (with a fallback default)
    default_coins = ["bitcoin", "ethereum", "solana", "cardano", "ripple", "polkadot"]
    coins_to_track = Variable.get("crypto_coins", default=default_coins)
    
    market_prices = fetch_all_prices(coins_to_track)
    analyze_market(market_prices)

if __name__ == "__main__":
    market_tracker_flow.from_source(
        # IMPORTANT: Put your GitHub URL back here!
        source="https://github.com/mbongeR/crypto-prefect-pipeline.git", 
        entrypoint="market_tracker.py:market_tracker_flow" 
    ).deploy(
        name="crypto-tracker-deployment",
        work_pool_name="my-local-pool", 
        interval=timedelta(minutes=2)
    )