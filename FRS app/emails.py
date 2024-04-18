import schedule
import time

def my_task():
    print("Executing my task")

# Schedule the task to run every day at 8:00 AM
schedule.every().day.at("20:33").do(my_task)

# Run the scheduler indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)
