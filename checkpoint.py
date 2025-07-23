import os

CHECKPOINT_FILE = "checkpoint.txt"

def save_checkpoint(index):
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(str(index))

def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            return int(f.read())
    return 0
