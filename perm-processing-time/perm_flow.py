"""
Script to web crawl perm processing time
"""
from prefect import flow
from prefect.client.schemas.schedules import construct_schedule
from info_email import inform_processing_time

# Define the schedule
cron_schedule = construct_schedule(cron="0 9 * * 1,4", timezone="America/Los_Angeles")  # At 09:00 am on Monday and Thursday, US west time

@flow(log_prints=True)
def daily_inform_processing_time_flow(receiving_email: str):
    inform_processing_time(receiving_email)

if __name__ == "__main__":
    daily_inform_processing_time_flow.serve(
        name="daily-inform-perm-processing-time",
        tags=["daily", "crawl"],
        parameters={"receiving_email": "billtsan1994@gmail.com"},
        schedule=cron_schedule,
    )
