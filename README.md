# Clean Coalition Data Cleaner
tyler@clean-coalition.org

Application finds and fixes discrepencies in datetime data exported from UtilityAPI.

## Windows:

- Make sure python is installed
- Open data cleaner folder in Command Prompt (Right click file -> open in command prompt)
- Install dependancies, run:
``` 
pip3 install pandas
```
```
pip3 install Pillow
```
- Run script `python3 gui.py`

## How to run on MAC/LINUX:
- Open a terminal or command prompt.
- Navigate to the directory containing the Makefile, requirements.txt, and the Python script.
- Run `make install` to install the dependencies in a virtual environment.
- Run `make run` to run the Python script.


This assumes that the user has make, python3, and venv already installed on their system. If you don't have make, you can install it using their system package manager (e.g., apt, brew, yum, etc.). The steps for installing python3 and venv depend on a user's operating system.


Please note that the tkinter package may not come pre-installed with some minimal Python installations, especially on Linux. If a user encounters an issue with tkinter not being available, they might need to install it through their system's package manager. For example, on Ubuntu or Debian-based systems, they can run:

`sudo apt-get install python3-tk`

On other systems, the package name might be different. However, most standard Python installations on Windows and macOS should include tkinter by default.

### If the above doesn't work, manually install packages listed in requirements