import time
from datetime import datetime

def action():
    print("A new minute has started!")

def main():
    # Get the current minute
    last_minute = datetime.now().minute

    while True:
        # Wait for a short time to avoid high CPU usage
        time.sleep(1)

        # Get the current minute
        current_minute = datetime.now().minute

        # Check if the minute has changed
        if current_minute != last_minute:
            action()  # Trigger the action
            last_minute = current_minute  # Update the last minute

main()