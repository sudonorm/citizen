import os
import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.proxy import Proxy, ProxyType
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from string import ascii_lowercase
from typing import List, Dict
import argparse
import re
import datetime
import time
import random
import winsound
import sys
import psutil
import glob

from PyQt6.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog
)

from citizen_ui import Ui_AppointmentFinder

QUIT_AFTER = 24 * 60 * 60

class Window(QMainWindow, Ui_AppointmentFinder):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.cboDays.addItems(["30", "60", "90"])
        self.connectSignalsSlots()
        self.user_agents_slim = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.1",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/117.0",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:109.0) Gecko/20100101 Firefox/117.0",
            "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0",
            "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        ]
        
    def connectSignalsSlots(self):
        # self.cmdGetPath.clicked.connect(self.dir_pop_up)
        # self.cmdGetCode.clicked.connect(self.get_values)
        self.cmdGetCode.clicked.connect(self.get_appointment)
        self.cmdExit.clicked.connect(QApplication.instance().quit)
        
    def dir_pop_up(self):
        folder = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
        folder = folder + "//chromedriver.exe"
        self.entryPath.setText(folder)

    def get_values(self):

        print(self.entryEmail.text())
        print(self.entryFirstName.text())
        print(self.entryLastName.text())
            
    def get_appointment(self):
        
        start_time = time.time()
        # print(self.entryEmail.text())
        # print(self.entryFirstName.text())
        # print(self.entryLastName.text())
        # print(self.cboDays.currentText())
        
        option = webdriver.ChromeOptions()
        # option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument('--incognito')
        option.add_argument('--disable-infobars')
        option.add_argument("--disable-notifications")
        #option.add_argument('disable-infobars')
        option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        
        try:
            for process in (process for process in psutil.process_iter() if process.name()=="chromedriver.exe"):
                try:
                    process.kill()
                except:
                    pass
        except:
            pass

        install_pth = rf'{ChromeDriverManager().install()}'

        files = glob.glob(f'{install_pth.split("chromedriver")[0]}{"chromedriver"}{os.sep}{"*"}')
        for f in files:
            import shutil
            shutil.rmtree(f)
        
        install_pth = rf'{ChromeDriverManager().install()}'
        
        driver = webdriver.Chrome(service=ChromeService(install_pth), options=option)
        
        driver.implicitly_wait(10)

        url = "https://serviceportal.hamburg.de/HamburgGateway/FVP/FV/Bezirke/DigiTermin/Behoerde/Auswahl?mandantId=5"

        print("reading url...")
        driver.get(url)

        time.sleep(random.randint(3, 7))
        checkBox = driver.find_element(by=By.CLASS_NAME, value="custom-control-label").click()
        time.sleep(random.randint(3, 7))
        second_checkbox = driver.find_element(by=By.ID, value="DsgvoAcceptance_label").click()
        time.sleep(random.randint(3, 7))
        accept = driver.find_element(by=By.ID, value="buttonNext").click()
        time.sleep(random.randint(3, 7))
        driver.find_element(by=By.ID, value="Vorname").send_keys(self.entryFirstName.text())
        driver.find_element(by=By.ID, value="Nachname").send_keys(self.entryLastName.text())
        driver.find_element(by=By.ID, value="EMail").send_keys(self.entryEmail.text())
        # 
        time.sleep(random.randint(3, 7))
        driver.find_element(by=By.ID, value="buttonNext").click()
        time.sleep(random.randint(3, 7))
        driver.find_element(by=By.ID, value="DienstleistungGruppen_0__Dienstleistungen_0__Anzahl").send_keys(1)
        time.sleep(random.randint(3, 7))
        driver.find_element(by=By.ID, value="buttonNext").click()

        print("started...")
        base = datetime.datetime.today()
        numdays = int(self.cboDays.currentText())
        
        date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
        date_list = [".".join(y for y in str(x).split(" ")[0].split("-")[::-1]) for x in date_list]

        datePicker = driver.find_element(by=By.ID, value="GewuenschterTermin_VonTag")

        while time.time() - start_time != QUIT_AFTER:
            for dt in date_list:
                datePicker.clear()
                datePicker.send_keys(dt)

                all_input_elements = driver.find_elements(by=By.TAG_NAME, value="input")
                for a in all_input_elements:
                    if a.get_attribute('type').lower().strip() == "submit":
                        try:
                            a.click()
                        except:
                            pass
                
                sourceCode = driver.page_source
                soup = bs(sourceCode, 'html.parser')
                
                if "Bitte wählen Sie das zuständige Amt aus:" in str(soup):
                    print("dates available")
                    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                    winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
                    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                    winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
                    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                    
                    appointments = driver.find_element(by=By.ID, value="amSchnellsten").find_element(by=By.CLASS_NAME, value="card-body")
                    appointments = driver.find_elements(by=By.CLASS_NAME, value="ignore-cancel-dialog")
                    appointments[0].click()
                    
                    driver.find_element(by=By.CSS_SELECTOR, value='#buttonNext > span.halflings.halflings-menu-right.sc-icon-right').click()
                    
                    if self.checkBoxCode.isChecked():
                        driver.find_element(by=By.CSS_SELECTOR, value='#btnTerminBuchen').click() ## book appointment
                
                time.sleep(random.randint(3, 7))

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())