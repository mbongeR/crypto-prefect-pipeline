"""Demo pipeline using Prefect for data extraction with retry logic."""
from prefect import flow, task
import random
import time

@task(retries=1, retry_delay_seconds=1)
def extract_data(source):
    print(f'Extracting from {source}...')
    time.sleep(1)
    if random.random() < 0.5:
        raise ValueError('Simulated network glitch!')
    return f'{source}_data'

@flow(name='My Demo Pipeline', log_prints=True)
def my_demo_flow():
    print('Starting pipeline...')
    for source in ['API_1', 'API_2', 'DB_1']:
        try:
            extract_data(source)
        except Exception:
            pass 
    print('Pipeline finished.')

if __name__ == '__main__':
    # This serves the flow so the Prefect UI can trigger it!
    my_demo_flow.serve(
        name="minutely-demo-deployment",
        cron="* * * * *", 
        tags=["demo"]
    )