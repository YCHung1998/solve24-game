# services/persistence.py
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
COUNTER_FILE = os.path.join(DATA_DIR, "game_count.txt")

def load_and_increment_counter(session_state):
    """讀取並增加遊玩次數"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if "has_counted" not in session_state:
        count = 0
        if os.path.exists(COUNTER_FILE):
            try:
                with open(COUNTER_FILE, "r") as f:
                    content = f.read().strip()
                    if content.isdigit():
                        count = int(content)
            except:
                pass

        count += 1
        session_state["has_counted"] = True

        try:
            with open(COUNTER_FILE, "w") as f:
                f.write(str(count))
        except:
            pass
        return count
    else:
        if os.path.exists(COUNTER_FILE):
            try:
                with open(COUNTER_FILE, "r") as f:
                    return int(f.read().strip())
            except:
                return 0
        return 0
