import subprocess
import time

def run_saga_script():
    saga_script_path = "c:/git/scrapy/promart/bat_run.py"  # Absolute path to saga_s.py

    while True:
        print("PROMART SE INICI...")
        process = subprocess.Popen(["python", saga_script_path])  # Start saga_s.py as a subprocess

        while True:
            if process.poll() is not None:  # Check if the subprocess has completed
                print("PROMART SE ESTA REINICIANDO...")
                break  # Break the loop to restart the script
            time.sleep(5)  # Wait for 5 seconds before checking again

if __name__ == "__main__":
    run_saga_script()
