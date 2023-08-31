import os
import json
import time


VALID_STATES = ["IDLE", "WAIT", "IN_PROGRESS", "DONE"]
VALID_EVENTS = ["READY_TO_WAIT", "STARTING", "COMPLETE"]

def update_state(current_state, event):
    if event == "READY_TO_WAIT" and current_state == "IDLE":
        return "WAIT"
    elif event == "STARTING" and current_state == "IDLE":
        return "IN_PROGRESS"
    elif event == "STARTING" and current_state == "IN_PROGRESS":
        return "DONE"
    elif event == "COMPLETE" and current_state == "IDLE":
        return "DONE"
    return current_state

def main():
    current_state = "IDLE"
    
    while current_state != "DONE":
        try:
            with open("events.json", "r") as events_file:
                events_data = json.load(events_file)
                event = events_data.get("event")
                
                if event in VALID_EVENTS:
                    new_state = update_state(current_state, event)
                    if new_state != current_state:
                        current_state = new_state
                        with open("state.txt", "w") as state_file:
                            state_file.write(current_state)
                            print(f"State updated: {current_state}")
                    else:
                        print(f"No state change: {current_state}")
                else:
                    print(f"Invalid event: {event}")
                    break
                
                time.sleep(1) 
            
        except FileNotFoundError:
            print("events.json not found. please create json file...")
            time.sleep(1)

if __name__ == "__main__":
    main()
