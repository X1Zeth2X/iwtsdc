import pyautogui

from time import sleep
from datetime import datetime, timedelta
from selenium import webdriver
from subprocess import run

weekday = dict([
    (6, 'sun'),
    (0, 'mon'),
    (1, 'tue'),
    (2, 'wed'),
    (3, 'thu')
])

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('disable-infobars')

class Bot:
    # Initialize data
    def __init__(self, data: dict):
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.data = data

        # Bot settings.
        self.started = False
        self.current_time = datetime.today

        print('Bot initialized.')
        print('---------------\n')

    def start_recorder(self):
        try:
            run([self.data['record']['start']], shell=True, capture_output=False)
            return 0
        
        except Exception as e:
            print(e)
    
    # Join a session and subject
    def join_session(self, url: str):
        print(f"Joining session: {url}")

        self.driver.get(url)

        # Enter credentials
        name_form = self.driver.find_element_by_xpath('//*[@id="conference_nickname"]')
        name_form.send_keys(self.data['student']['name'])

        # Join
        enter_btn = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div/section[2]/form/div[1]/button')
        enter_btn.click()
    
    # Close previous handles (Window)
    def close_prev_handles(self):
        handles = self.driver.window_handles
        # Switch to original tab
        self.driver.switch_to_window(handles[0])

        # Close it
        self.driver.close()

        # Switch to latest
        self.driver.switch_to_window(handles[0])

    # Run
    def run(self):
        start = self.data['time']['start']
        stop = self.data['time']['stop']

        # Check if class ended
        if self.current_time().today().hour > stop[0]:
            print("Classes already finished!")
            return

        # Classes today
        today = self.current_time().weekday()
        classes = self.data['schedule'][weekday[today]]
        subjects = self.data['subjects']

        class_duration = self.data['time']['class_duration']

        # Stop if recorder fails to start.
        if self.start_recorder() != 0:
            return

        while True:
            print("Started! Running.")
            # Check if school hasn't started
            if not self.started:
                # Wait until first session starts
                time_now = self.current_time()
                time_start = time_now.replace(
                    hour=start[0],
                    minute=start[1]
                )

                wait_duration = time_now - time_start

                print("Classes hasn't started yet.")
                print(f"Wait for {wait_duration.total_seconds() / 60} minutes.")

                # sleep(wait_duration.total_seconds())

            # Check if class is free.
            # Record current class
            current_class = subjects['chemistry']
            self.join_session(current_class)

            pyautogui.hotkey(*self.data['record']['toggle'])
            sleep(class_duration * 60)
            pyautogui.hotkey(*self.data['record']['toggle'])

            # Remove class
            subjects.pop(0)
            # Wait for next class
            sleep(self.data['time']['time_interval'] * 60)
            