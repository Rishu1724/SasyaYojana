"""
Script to schedule periodic model retraining.
This script can be run as a cron job or scheduled task.
"""

import schedule
import time
import subprocess
import sys
import os
from datetime import datetime

def run_retraining():
    """Run the model retraining script."""
    print(f"[{datetime.now()}] Starting model retraining...")
    
    try:
        # Run the retraining script
        result = subprocess.run([
            sys.executable, 
            os.path.join(os.path.dirname(__file__), 'retrain_model.py'),
            '--days', '30'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[{datetime.now()}] Model retraining completed successfully")
            print(result.stdout)
        else:
            print(f"[{datetime.now()}] Model retraining failed")
            print(result.stderr)
    except Exception as e:
        print(f"[{datetime.now()}] Error running retraining script: {e}")

def schedule_retraining():
    """Schedule model retraining."""
    # Schedule monthly retraining (runs on the 1st of every month at 2:00 AM)
    schedule.every().month.do(run_retraining)
    
    # Alternatively, you can schedule:
    # Weekly: schedule.every().week.do(run_retraining)
    # Daily: schedule.every().day.do(run_retraining)
    # Hourly: schedule.every().hour.do(run_retraining)
    
    print("Model retraining scheduled:")
    print("- Monthly on the 1st at 2:00 AM")
    print("Scheduler started. Press Ctrl+C to stop.")
    
    # Run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    try:
        schedule_retraining()
    except KeyboardInterrupt:
        print("\nScheduler stopped.")
    except Exception as e:
        print(f"Scheduler error: {e}")