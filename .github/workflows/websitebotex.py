import psutil
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Forcefully close any lingering Chrome processes
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

# Configuration Options
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

# Anti-bot bypass header
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Start Browser Instance
service = Service()
driver = webdriver.Chrome(options=options, service=service)

# ==============================================================================
# 🚀 AUTOMATION EXECUTION FLOW
# ==============================================================================
try:
    print("🌐 Navigating to Seedloaf Dashboard...")
    driver.get("https://seedloaf.gg") # Adjust target panel URL if needed
    
    # 1. Login Authentication Check
    # (If the session cache doesn't kick in, input credentials dynamically)
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    
    # Note: Insert your existing text field elements/login logic sequence here if required.

    # 2. Dynamic Server Name Target Filtering
    target_server = os.getenv("SERVER_NAME")
    if not target_server:
        print("❌ ERROR: No SERVER_NAME environment variable was provided by the runner workflow!")
        driver.quit()
        sys.exit(1)

    print(f"🔍 Searching for server entry card: '{target_server}'")

    # 3. Targeted Bulletproof XPath Lookup
    # Finds the text header (e.g. "Mafia") -> Navigates up to the card block container -> Searches down for its specific "Start World" button.
    robust_xpath = f"//*[contains(text(), '{target_server}')]/ancestor::div[contains(@class, 'card') or contains(@class, 'row') or position() < 5]//button[contains(., 'Start World')]"

    wait = WebDriverWait(driver, 20)
    start_button = wait.until(EC.element_to_be_clickable((By.XPATH, robust_xpath)))
    
    # 4. Fire click event
    start_button.click()
    print(f"✅ Successfully clicked 'Start World' for server: {target_server}")
    
    # Wait for web app backend initialization tasks to register server updates
    time.sleep(8)

except Exception as e:
    print(f"❌ Failed to find or click the startup button for '{target_server}': {e}")
    driver.save_screenshot("/tmp/error_screenshot.png")
    print("📸 Saved troubleshooting error screenshot to '/tmp/error_screenshot.png'")
    driver.quit()
    sys.exit(1)

# Clean termination
driver.quit()
print("👋 Browser session closed successfully.")
