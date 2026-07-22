import psutil
import os
import sys
os.system("pkill -9 chrome")  # Forcefully kill all Chrome processes
def kill_chrome():
    for process in psutil.process_iter(attrs=["pid", "name"]):
        if "chrome" in process.info["name"].lower():
            try:
                p = psutil.Process(process.info["pid"])
                p.terminate()  # Terminate gracefully
            except psutil.NoSuchProcess:
                pass  # Process already closed

kill_chrome()

#requiredlib = [selenium,time]
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
#import tempfile
#import uuid

'''
os.environ["MOZ_LOG"] = "debug"  # Enable verbose logging
# Initialize WebDriver
options = Options()
service = Service(excecutable_path="/usr/local/bin/geckodriver")
options.binary_location = '/usr/bin/firefox'
options.add_argument("--headless")
driver = webdriver.Firefox(options=options, service=service)
'''
# Chrome Options
options = Options()
# Use persistent user profile
USER_DATA_DIR = "/tmp/seedloaf-session"
options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
options.add_argument("--profile-directory=Default")  # Optional

options.binary_location = "/opt/chrome/chrome"
options.add_argument("--headless=new")  # Use new headless mode
options.add_argument("window-size=1920x1080")  # Ensure full viewport
options.add_argument("--disable-gpu")  # Fix rendering issues in headless
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
#temp_dir = f"/tmp/chrome-user-data-{uuid.uuid4()}"
#options.add_argument(f"--user-data-dir={temp_dir}")

# Bypass detection
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
