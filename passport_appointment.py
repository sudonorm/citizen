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
import sys
import psutil
import glob
from sys import platform as plt_form
from random import choice

QUIT_AFTER = 24 * 60 * 60


class PassportAppointment:
    def __init__(self):
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

    def say(self, msg="Appointment found!", voice="Victoria"):
        # os.system(f"say -v {voice} {msg}")
        os.system(f"say {msg}")

    def get_appointment(
        self,
        *,
        entryFirstName: str,
        entryLastName: str,
        entryEmail: str,
        use_web_manager: bool = True,
        install_pth: str = None,
        cboDays: int = 30,
        book_appointment: bool = True,
    ):

        start_time = time.time()

        option = webdriver.ChromeOptions()
        # option.add_argument('--headless')
        option.add_argument("--no-sandbox")
        option.add_argument("--disable-dev-shm-usage")
        option.add_argument("--incognito")
        option.add_argument("--disable-infobars")
        option.add_argument("--disable-notifications")
        # option.add_argument('disable-infobars')
        option.add_experimental_option(
            "excludeSwitches", ["enable-automation", "enable-logging"]
        )
        selected_user_agent = choice(self.user_agents_slim)
        option.add_argument(f"user-agent= {selected_user_agent}")

        try:
            if plt_form in ["win32", "cygwin"]:
                for process in (
                    process
                    for process in psutil.process_iter()
                    if process.name() == "chromedriver.exe"
                ):
                    try:
                        process.kill()
                    except:
                        pass
            else:
                for process in (
                    process
                    for process in psutil.process_iter()
                    if process.name() == "chromedriver"
                ):
                    try:
                        process.kill()
                    except:
                        pass
        except:
            pass

        if use_web_manager:
            install_pth = rf"{ChromeDriverManager().install()}"

            files = glob.glob(
                f'{install_pth.split("chromedriver")[0]}{"chromedriver"}{os.sep}{"*"}'
            )
            for f in files:
                import shutil

                shutil.rmtree(f)

            install_pth = rf"{ChromeDriverManager().install()}"

            driver = webdriver.Chrome(
                service=ChromeService(install_pth), options=option
            )
        else:
            driver = webdriver.Chrome(
                service=ChromeService(install_pth), options=option
            )

        driver.implicitly_wait(10)

        url = "https://serviceportal.hamburg.de/HamburgGateway/FVP/FV/Bezirke/DigiTermin/Behoerde/Auswahl?mandantId=5"

        print("reading url...")
        driver.get(url)

        time.sleep(random.randint(3, 7))
        checkBox = driver.find_element(
            by=By.CLASS_NAME, value="custom-control-label"
        ).click()
        time.sleep(random.randint(3, 7))
        second_checkbox = driver.find_element(
            by=By.ID, value="DsgvoAcceptance_label"
        ).click()
        time.sleep(random.randint(3, 7))
        accept = driver.find_element(by=By.ID, value="buttonNext").click()
        time.sleep(random.randint(3, 7))
        driver.find_element(by=By.ID, value="Vorname").send_keys(entryFirstName)
        driver.find_element(by=By.ID, value="Nachname").send_keys(entryLastName)
        driver.find_element(by=By.ID, value="EMail").send_keys(entryEmail)
        #
        time.sleep(random.randint(3, 7))
        driver.find_element(by=By.ID, value="buttonNext").click()
        time.sleep(random.randint(3, 7))
        driver.find_element(
            by=By.ID, value="DienstleistungGruppen_0__Dienstleistungen_0__Anzahl"
        ).send_keys(1)
        time.sleep(random.randint(3, 7))
        driver.find_element(by=By.ID, value="buttonNext").click()

        print("started...")
        base = datetime.datetime.today()
        numdays = int(cboDays)

        date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
        date_list = [
            ".".join(y for y in str(x).split(" ")[0].split("-")[::-1])
            for x in date_list
        ]

        datePicker = driver.find_element(by=By.ID, value="GewuenschterTermin_VonTag")

        while time.time() - start_time != QUIT_AFTER:
            for dt in date_list:
                datePicker.clear()
                datePicker.send_keys(dt)

                all_input_elements = driver.find_elements(by=By.TAG_NAME, value="input")
                for a in all_input_elements:
                    if a.get_attribute("type").lower().strip() == "submit":
                        try:
                            a.click()
                        except:
                            pass

                sourceCode = driver.page_source
                soup = bs(sourceCode, "html.parser")

                if "Bitte wählen Sie das zuständige Amt aus:" in str(soup):

                    if plt_form in ["win32", "cygwin"]:
                        import winsound

                        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                        winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
                        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                        winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
                        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                    elif plt_form in ["darwin"]:

                        self.say(msg="Great! Finally found an appointment!")

                    appointments = driver.find_element(
                        by=By.ID, value="amSchnellsten"
                    ).find_element(by=By.CLASS_NAME, value="card-body")
                    appointments = driver.find_elements(
                        by=By.CLASS_NAME, value="ignore-cancel-dialog"
                    )
                    appointments[0].click()

                    driver.find_element(
                        by=By.CSS_SELECTOR,
                        value="#buttonNext > span.halflings.halflings-menu-right.sc-icon-right",
                    ).click()

                    if book_appointment:

                        driver.find_element(
                            by=By.CSS_SELECTOR, value="#btnTerminBuchen"
                        ).click()  ## book appointment

                        if plt_form in ["darwin"]:

                            # Or say something more exciting
                            self.say(msg="The appointment was booked!")

                time.sleep(random.randint(3, 7))
