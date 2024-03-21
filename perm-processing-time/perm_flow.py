"""
Script to web crawl perm processing time
"""
import json
from prefect import flow
from prefect.client.schemas.schedules import construct_schedule
from info_email import inform_processing_time

# Define the schedule
cron_schedule = construct_schedule(cron="0 9 * * 1,4", timezone="America/Los_Angeles")  # At 09:00 am on Monday and Thursday, US west time

# Define function to get account and password
def read_email_config(file_path="email_pwd.json"):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data["send_email"], data["send_email_pwd"]

sender_email, sender_pwd = read_email_config()

@flow(log_prints=True)
def daily_inform_processing_time_flow(
    sender_email: str,
    sender_pwd: str,
    receiving_email: str
):
    inform_processing_time(sender_email, sender_pwd, receiving_email)

if __name__ == "__main__":
    daily_inform_processing_time_flow.from_source(
        source="https://github.com/Bill-Zhan/web-crawler.git",
        entrypoint="perm-processing-time/perm_flow.py:daily_inform_processing_time_flow",
    ).deploy(   
        name="daily-inform-perm-processing-time",
        work_pool_name="perm-time-crawler-pool",
        tags=["daily", "crawl"],
        parameters={
            "sender_email": sender_email,
            "sender_pwd": sender_pwd,
            "receiving_email": "billtsan1994@gmail.com"
        },
        schedule=cron_schedule,
    )
