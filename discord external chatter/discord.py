import requests
import string
import json
import os

def menu():
    print('Choose an option:\n1 - Add an authenticator\n2 - Add a chat\n3 - Run the app\n(enter 1, 2 or 3)')
    while True:
        choice = input('> ').strip()
        if choice in ('1','2','3'):
            return choice
        else:
            print('Invalid choice. Enter 1, 2 or 3.')

def print_auth():
    print("\nAuthenticators:")
    enum = 1
    for key, token in authenticators.items():
        name = authvalues.get(token, "<no name>")
        print(f"{key}) {name} (token preview: {token[:6]}...{token[-6:]})")
        enum += 1
    print("")

def print_chats():
    print("\nChats:")
    enum = 1
    for key, chanid in options.items():
        desc = values.get(chanid, "<no desc>")
        print(f"{key}) {chanid} -- {desc}")
        enum += 1
    print("")

def choose_auth():
    if len(authenticators) == 0:
        print('There is no available tokens.')
        add_authenticator()
    else:
        print_auth()
        choice = input(f"Choose the authenticator (number): ").strip()
        auth = authenticators.get(choice)
        if not auth:
            print("Invalid authenticator selection.")
            return None, None
        print("Running from:", authvalues.get(auth), "\n")
        return auth, authvalues.get(auth)

def choose_chat():
    if len(options) == 0:
        print('There is no available chats.')
        add_chat()
    else:
        print_chats()
        choice = input(f"Choose the chat (number): ").strip()
        selection = options.get(choice)
        if not selection:
            print("Invalid chat selection.")
            return None, None
        print("You selected:", selection, "--", values.get(selection), "\n")
        return selection, values.get(selection)
def makeurl(id):
    return "https://discord.com/api/v9/channels/" + id + "/messages"

# ---- defining functions and variables
# ---------------------------------------

# ---------------------------------------
# ------- authorisation and chat tuples 
_default_dicts = {
    "authenticators": {

    },
    "authvalues": {

    },
    "options": {

    },
    "values": {

    }
}

_dicts_path = os.path.join(os.path.dirname(__file__), 'dicts.json')

def _load_dicts():
    if os.path.exists(_dicts_path):
        try:
            with open(_dicts_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for k in _default_dicts:
                if k not in data or not isinstance(data[k], dict):
                    data[k] = _default_dicts[k]
            return data
        except (json.JSONDecodeError, OSError):
            with open(_dicts_path, 'w', encoding='utf-8') as f:
                json.dump(_default_dicts, f, ensure_ascii=False, indent=4)
            return dict(_default_dicts)
    else:
        try:
            with open(_dicts_path, 'w', encoding='utf-8') as f:
                json.dump(_default_dicts, f, ensure_ascii=False, indent=4)
        except OSError:
            pass
        return dict(_default_dicts)

def save_dicts():
    data = {
        "authenticators": authenticators,
        "authvalues": authvalues,
        "options": options,
        "values": values
    }
    with open(_dicts_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

_loaded = _load_dicts()
authenticators = _loaded.get("authenticators", _default_dicts["authenticators"])
authvalues = _loaded.get("authvalues", _default_dicts["authvalues"])
options = _loaded.get("options", _default_dicts["options"])
values = _loaded.get("values", _default_dicts["values"])

def _next_numeric_key(d):
    nums = []
    for k in d.keys():
        try:
            nums.append(int(k))
        except Exception:
            pass
    return str(max(nums)+1 if nums else 1)

def add_authenticator():
    token = input("Enter authenticator token: ").strip()
    if not token:
        print("No token entered.")
        return
    name = input("Enter a name/label for this token: ").strip() or "<unnamed>"
    key = _next_numeric_key(authenticators)
    authenticators[key] = token
    authvalues[token] = name
    save_dicts()
    print(f"Added authenticator {key}: {name}")

def add_chat():
    chanid = input("Enter channel id: ").strip()
    if not chanid:
        print("No channel id entered.")
        return
    desc = input("Enter a description/label for this chat: ").strip() or "<unnamed>"
    key = _next_numeric_key(options)
    options[key] = chanid
    values[chanid] = desc
    save_dicts()
    print(f"Added chat {key}: {chanid} -- {desc}")

def run_app():
    auth, authname = choose_auth()
    if not auth:
        return
    chanid, chandesc = choose_chat()
    if not chanid:
        return
    url = makeurl(chanid)
    headers = {
        "Authorization": auth,
        "Content-Type": "application/json"
    }
    print("Enter messages to send. Type /quit to exit, /menu to return to menu.")
    while True:
        ladunek = input('input a message: ')
        if ladunek.strip() == "/quit":
            print("Exiting.")
            exit(0)
        if ladunek.strip() == "/menu":
            return
        payload = {"content": ladunek}
        try:
            res = requests.post(url, json=payload, headers=headers, timeout=10)
            print(f"Status: {res.status_code} - {res.text[:200]}")
        except Exception as e:
            print("Request failed:", e)

if __name__ == "__main__":
    while True:
        choice = menu()
        if choice == '1':
            add_authenticator()
        elif choice == '2':
            add_chat()
        elif choice == '3':
            run_app()
