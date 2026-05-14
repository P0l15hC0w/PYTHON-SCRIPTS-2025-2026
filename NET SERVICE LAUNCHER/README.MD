# Net Service Launcher

#### A small windows utility for playing with the status of services from a simple Tkinter GUI.

## Overview
- `start.vbs` - a helper script that launches `net_service_launcher.py` with requred privileges.
- `net_service_launcher.py` - the main python application.
- `services.json` - configuration file for the services played with.

## Requirements
- Windows
- Python installed and available either in the `PATH` environment variable or inside the project root folder.
- Access to run service control commands (`net start`, `net stop`, `sc query`).
- A json file record corresponding to a `net service`.

## How to start the app
Run `start.vbs` to launch the app with the right privileges. The VBScript uses `ShellExecute` with `runas`, so it requests elevation and starts `python.exe` with `net_service_launcher.py`.

If Python is not in **`PATH`**, place `python.exe` in the same folder as the project and the script will still work.

## How the app works

`net_service_launcher.py` creates a Tkinter window with one row for each service defined in `services.json`.

`services.json` maps friendly display names to actual Windows service names. basically serving them both for the backend and ux on a clean plate. 

#### A basic example of what xampp services look like inside of the file:
```json
{
    "Display name": "service_name",

    // actual use
    "MySQL Xampp": "mysql",
    "Apache Xampp": "apache2.4",
    "FileZilla Xampp": "filezillaserver"
}
```

The app backend uses `sc query` to check whether if each service is running and updates the status labels every 2 seconds.

## Pipeline and threading

When a user clicks Start or Stop, the app launches the service command in a separate thread. This is important because `net start` and `net stop` can take time to complete, and running them in the main thread would freeze the Tkinter interface.

The fresh thread executes the command, logs the output, triggering a status refresh whilst. This keeps the GUI responsive while service control commands run in the background.

## summary
- The app relies on `services.json` for the service list, so updating that file changes the buttons and labels shown in the GUI, with their corresponding actions.
- The status refresh loop is periodic and runs mostly independently from button events.
- The `start.vbs` file is the recommended entry point because it ensures both the elevated privileges which are requested at launch, as of no cli and gui at once.