# Let's talk citizenship...

<strong>Do note that the code in this repo is for educational purposes only. The author is not liable for any damages that might occur by using the code in this repo.</strong>

All solutions always start with a problem, and for me this was getting an appointment for the citizenship talk some years ago. Being employed full time and having to refresh a page continously all day long to secure an appointment which is super scarce was a no-no, so, in true over-engineering fashion, I automated this. The code has been cleaned up and will run on Windows. It has not been tested on MacOS, but it can surely be adapted

A repo which contains the code for securing a first-talk appointment for citizenship (Einbürgerung-Erstberatungsgespräch) in Hamburg.

# Requirements

- Install Chrome
- Create a virtual environment
- Install all the packages in the requirements.txt (pip install -r requirements.txt)

# Build Instructions
The app is a Selenium application and uses PyQt. The ui file for the simple user interface is included in `ui`. This can be modified using PyQt designer.

To recreate the `citizen_ui.py` script, which is needed by the application, from the `citizen.ui` file, run the below command from a terminal in which your virtual environment is running:

    pyuic6 -o `<path to desired output folder>`\citizen.py `<path to ui folder>`\ui\citizen.ui


To rebuild the the .exe file in the dist folder, run the below (after replacing the `< >` appropriately)

    pyinstaller get_passport_appointment.py --name citizenship_first_talk_appointment --paths=`<path to virtual environment folder>`\venv\Lib\site-packages --add-data "`<path to virtual environment folder>`\venv\Lib\site-packages\PyQt6;PyQt6" --add-data "`<path to citizen_ui python file>`\citizen_ui.py;citizen_ui.py" --onefile

# OS Usage
- If you are on Windows, the exe file in the `dist` folder can be used or you can run the `get_passport_appointment.py` script

# Usage
- Select the number of days in the future you want to search
- Indicate if you want to the appointment to be booked automatically or not (the default is that the appointment will be booked, so you can just run this and let it do its thing). This should be turned off if you are not flexible with the day, as it will book the first available slot
- Enter your email
- Enter your firstname
- Enter your lastname
- Click the `Check for appointment` button
- Go do some other stuff :)

When an appointment is found, it will make some windows sounds, and will either stop there or book the appointment, if you ask it to book.

Happy hunting :)


