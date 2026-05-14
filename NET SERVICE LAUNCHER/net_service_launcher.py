import tkinter as tk
import subprocess
import threading
import json

with open("services.json", "r") as f:
    services = json.load(f)

root = tk.Tk()
root.title("Net Service Launcher")
root.geometry("600x400")

status_labels = {}

log_box = tk.Text(root, height=18, width=72)
log_box.config(bg="#d1d1d1")
log_box.grid(row=100, column=0, columnspan=4, pady=10, padx=10)

log_iter = 1

def log(msg: str):
    global log_iter
    log_box.insert(tk.END, f"{log_iter}. {msg}\n")
    log_box.see(tk.END)
    log_iter += 1

def log_async(msg: str):
    root.after(0, lambda: log(msg))

def get_state(service: str):
    result = subprocess.run(
        ["sc", "query", service],
        capture_output=True,
        text=True,
        errors="replace")

    if result.returncode != 0: return False
    return "RUNNING" in result.stdout

def execute(service: str, action: str):
    cmd = ["net", "start", service] if action == "start" else ["net", "stop", service]
    result = subprocess.run(cmd, capture_output=True)

    output = (result.stdout.decode(errors="replace") + result.stderr.decode(errors="replace"))

    return output

def refresh_status():
    for _, service in services.items():
        state = get_state(service)
        status_labels[service].config(
            text="Running" if state else "Stopped",
            fg="#44c53f" if state else "#c53232",
            font=("Arial", 9, "bold"))

    root.after(2000, refresh_status)

def run_service(service, action):
    output = execute(service, action)
    if output: log_async(output)

    root.after(0, refresh_status)

def handle_execute(service, action):
    threading.Thread(
        target=run_service,
        args=(service, action),
        daemon=True
    ).start()

for row, (display_name, service_name) in enumerate(services.items()):
    tk.Label(root, text=display_name, width=20).grid(row=row, column=0)

    tk.Button(
        root,
        text="Start",
        command=lambda s=service_name: handle_execute(s, "start")
    ).grid(row=row, column=1)

    tk.Button(
        root,
        text="Stop",
        command=lambda s=service_name: handle_execute(s, "stop")
    ).grid(row=row, column=2)

    status_labels[service_name] = tk.Label(root, text="Unknown")
    status_labels[service_name].grid(row=row, column=3)

refresh_status()
root.mainloop()