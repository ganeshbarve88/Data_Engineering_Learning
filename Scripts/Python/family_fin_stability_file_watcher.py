import os
import time
import requests
from dotenv import load_dotenv
from threading import Timer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Load environment variables from the .env file
load_dotenv()

# Fetch configurations securely
AIRFLOW_URL = os.getenv("AIRFLOW_URL")
AIRFLOW_USER = os.getenv("AIRFLOW_USER")
AIRFLOW_PASSWORD = os.getenv("AIRFLOW_PASSWORD")

AIRFLOW_AUTH = (AIRFLOW_USER, AIRFLOW_PASSWORD)
WAIT_SECONDS = 60.0

class AirflowTriggerHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.timers = {}

    def on_modified(self, event):
        if event.is_directory:
            return
            
        filename = os.path.basename(event.src_path)
        if filename.endswith(".csv"):
            self.debounce_trigger(filename, event.src_path)

    def debounce_trigger(self, filename, filepath):
        if filename in self.timers:
            self.timers[filename].cancel()
            print(f"[{filename}] Modification detected. Resetting 60-second timer...")
        else:
            print(f"[{filename}] Modification detected. Starting 60-second countdown...")

        new_timer = Timer(WAIT_SECONDS, self.trigger_dag, args=[filename, filepath])
        new_timer.start()
        self.timers[filename] = new_timer

    def trigger_dag(self, filename, filepath):
        if filename in self.timers:
            del self.timers[filename]

        print(f"[{filename}] 60 seconds of silence elapsed. Triggering Airflow via Docker CLI...")
        
        # Create the configuration JSON string
        import json
        import subprocess
        conf_data = json.dumps({"filename": filename, "filepath": filepath})
        
        # Build the docker exec command
        command = [
            "docker", "exec", "airflow-airflow-scheduler-1",
            "airflow", "dags", "trigger",
            "--conf", conf_data,
            "csv_scd2_pipeline"
        ]
        
        try:
            # Execute the command directly on the host machine
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"[{filename}] Successfully triggered Airflow DAG.")
            else:
                # If Airflow throws an error, print it to the terminal
                error_msg = result.stderr.strip() or result.stdout.strip()
                print(f"[{filename}] Failed to trigger DAG: {error_msg}")
        except Exception as e:
            print(f"[{filename}] Subprocess execution failed: {e}")


if __name__ == "__main__":
    # Basic validation to ensure .env is loaded properly
    if not AIRFLOW_USER or not AIRFLOW_PASSWORD:
        print("Error: Airflow credentials not found. Please check your .env file.")
        exit(1)

    handler = AirflowTriggerHandler()
    observer = Observer()
    
    csv_directory = "G:/Not_Backed_Up/Barve_Ganesh_Family_Financial_Stability_Report" 
    observer.schedule(handler, path=csv_directory, recursive=False)
    observer.start()
    
    print(f"Watching {csv_directory} for CSV changes. Airflow trigger will delay for {WAIT_SECONDS}s...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("Shutting down watcher...")
    observer.join()