Sora Prompt Maker (Desktop)

Files:
- sora_prompt_maker.py   -> The Tkinter app
- run.bat                -> Windows launcher (creates .venv, installs requirements, runs app)
- requirements.txt       -> Currently empty (tkinter is built-in); keep for future add-ons

How to use:
1) Install Python 3.10 or newer (https://www.python.org/downloads/). On Windows, CHECK "Add Python to PATH".
2) Put all three files in the same folder.
3) Double-click run.bat. It will:
   - Create .venv if missing
   - Install requirements from requirements.txt (if any)
   - Launch the UI

Troubleshooting:
- If Python isn’t found, install it or run from a terminal: py -3 run.bat
- If tkinter is missing on your distro, install the "tcl/tk" option for Python.
