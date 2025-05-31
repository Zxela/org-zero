# scripts/run_pm.py
from agents.pm.agent import ProjectManagerAgent

if __name__ == "__main__":
    print("👷 PM Agent running...")
    pm = ProjectManagerAgent()

    import time
    while True:
        time.sleep(1)  # Keep process alive to listen
