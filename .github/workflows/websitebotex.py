import psutil
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

os.system("pkill -9 chrome")  

def kill_chrome():
    for process in psutil.process_iter(attrs=["pid", "name"]):
        if "chrome" in process.info["name"].lower():
            try:
                p = psutil.Process(process.info["pid"])
                p.terminate()  
            except psutil.NoSuchProcess:
                pass  

kill_chrome()

options = Options()
USER_DATA_DIR = "/tmp/seedloaf-session"
options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
options.add_argument("--profile-directory=Default")
options.binary_location = "/opt/chrome/chrome"
options.add_argument("--headless=new")  
options.add_argument("window-size=1920x1080")  
options.add_argument("--disable-gpu")  
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

service = Service()
driver = webdriver.Chrome(options=options, service=service)

try:
    print("🌐 Navigating to Seedloaf Dashboard...")
    driver.get("https://seedloaf.gg")
    
    # 1. Login Logic
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    
    # Ha nincs elmentett session, itt lépjen be (A te egyedi bejelentkezési kódod helye)
    
    # 2. Dynamic Server Selection
    target_server = os.getenv("SERVER_NAME")
    if not target_server:
        print("❌ ERROR: No SERVER_NAME provided!")
        driver.quit()
        sys.exit(1)

    print(f"🔍 Searching for server: '{target_server}'")
    robust_xpath = f"//*[contains(text(), '{target_server}')]/ancestor::div[contains(@class, 'card') or contains(@class, 'row') or position() < 5]//button[contains(., 'Start') or contains(., 'Start World')]"

    wait = WebDriverWait(driver, 20)
    start_button = wait.until(EC.element_to_be_clickable((By.XPATH, robust_xpath)))
    start_button.click()
    print(f"✅ Successfully clicked 'Start World' for server: {target_server}")
    time.sleep(8)

except Exception as e:
    print(f"❌ Failed: {e}")
    driver.save_screenshot("/tmp/error_screenshot.png")
    driver.quit()
    sys.exit(1)

driver.quit()
