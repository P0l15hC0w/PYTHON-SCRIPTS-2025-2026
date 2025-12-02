import subprocess
import sys
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_JSON = os.path.join(SCRIPT_DIR, "tools/default_tools.json")

DEFAULT_TOOLS = {
    "1": ["Calculator", "tools/calculator.py"]
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_tools():
    if not os.path.exists(TOOLS_JSON):
        # create file with defaults
        save_tools(DEFAULT_TOOLS)
        return dict(DEFAULT_TOOLS)
    try:
        with open(TOOLS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Ensure structure is key -> [name, filename]
        tools = {}
        for k, v in data.items():
            if isinstance(v, list) and len(v) >= 2:
                tools[str(k)] = [v[0], v[1]]
        return tools
    except Exception:
        # On error, fall back to defaults
        return dict(DEFAULT_TOOLS)

def save_tools(tools):
    try:
        with open(TOOLS_JSON, "w", encoding="utf-8") as f:
            json.dump(tools, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Failed to save tools.json: {e}")
        input("Press Enter to continue...")

def show_menu(tools):
    clear()
    print("=== Python Multitool Launcher ===\n")
    # show numeric keys sorted
    keys = sorted(tools.keys(), key=lambda x: int(x) if x.isdigit() else x)
    for key in keys:
        name, _ = tools[key]
        print(f"{key}. {name}")
    print("a. Add new tool")
    print("0. Exit\n")

def run_tool(choice, tools):
    if choice in tools:
        name, file = tools[choice]
        script_path = os.path.join(SCRIPT_DIR, file)

        if not os.path.exists(script_path):
            print(f"Error: '{file}' not found in {SCRIPT_DIR}.")
            input("Press Enter to continue...")
            return

        print(f"\nLaunching {name}...\n")
        subprocess.run([sys.executable, script_path])
        input("\nPress Enter to return to menu...")
    else:
        print("Invalid choice.")
        input("Press Enter to continue...")

def add_tool(tools):
    print("\n=== Add New Tool ===")
    name = input("Tool name: ").strip()
    if not name:
        print("Name cannot be empty.")
        input("Press Enter to continue...")
        return

    filename = "tools/"+input("Script file name (including the file extension) ").strip() #depends on what the name of the tools directory is named 
    if not filename:
        print("Filename cannot be empty.")
        input("Press Enter to continue...")
        return

    # compute next numeric key
    numeric_keys = [int(k) for k in tools.keys() if k.isdigit()]
    next_key = str(max(numeric_keys) + 1 if numeric_keys else 1)
    tools[next_key] = [name, filename]
    save_tools(tools)
    print(f"Added '{name}' as option {next_key} -> {filename}")

    script_path = os.path.join(SCRIPT_DIR, filename)
    if not os.path.exists(script_path):
        create = input(f"Script '{filename}' does not exist. Create empty file? [y/N]: ").strip().lower()
        if create == "y":
            try:
                os.makedirs(os.path.dirname(script_path), exist_ok=True)
                with open(script_path, "w", encoding="utf-8") as f:
                    f.write("#!/usr/bin/env python3\n\n")
                print(f"Created {script_path}")
            except Exception as e:
                print(f"Failed to create file: {e}")
    input("Press Enter to continue...")

def main():
    tools = load_tools()
    while True:
        show_menu(tools)
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        if choice.lower() == "a":
            add_tool(tools)
            # reload tools from disk to ensure consistency
            tools = load_tools()
            continue

        run_tool(choice, tools)

if __name__ == "__main__":
    main()

