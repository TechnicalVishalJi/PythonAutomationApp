from flask import Flask
from selenium.webdriver.chrome.options import Options as ChromeOptions  # Import for Chrome options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from xvfbwrapper import Xvfb
import time
import os
import traceback


app = Flask(__name__)
pagespeed_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
wordpress_url = "https://vishal.rf.gd"

@app.route('/')
def index():
    return "<h1>Automation App by Vishal Singh</h1>"
    
@app.route('/start-minecraft-server', methods=['GET'])
def start_server():
    result = start_minecraft_server()
    if "Server started successfully" in result or "Server is already running" in result:
        return result, 200  # HTTP 200 OK
    else:
        print(result)
        result = start_minecraft_server()
        if "Server started successfully" in result or "Server is already running" in result:
            return result, 200  # HTTP 200 OK
        else:
            return result, 500
        
@app.route('/login-heliohost')
def login_heliohost():
    result = login_to_heliohost()
    if "Login successful" in result:
        return result, 200  # HTTP 200 OK
    else:
        result = login_to_heliohost()
        if "Login successful" in result:
            return result, 200  # HTTP 200 OK
        else:
            return result, 500  # HTTP 500 Internal Server Error

@app.route("/login-nightcafe")
def nightcafe_task():
    result = login_nightcafe()
    if "Login and credit claim success" in result:
        return result, 200  # HTTP 200 OK"
    else:
        print(result)
        result = login_nightcafe()
        if "Login and credit claim success" in result:
            return result, 200  # HTTP 200 OK"
        else:
            return result, 500  # HTTP 500 Internal Server Error

@app.route("/add-90-min-mc-server")
def add_90_min_mc_server():
    result = add_90_min_minecraft_server()
    if "Time extended successfully" in result:
        return result, 200
    else:
        print(result)
        result = add_90_min_minecraft_server()
        if "Time extended successfully" in result:
            return result, 200
        else:
            return result, 500

@app.route("/backup-minecraft-server")
def backup_mc_server():
    return "Nothing"

@app.route("/share_nightcafe_creation")
def share_nc_creation():
    return "Nothing"



def start_chrome_driver(headless=True, blockImages=False):
    options = ChromeOptions()  # Change to ChromeOptions
    vdisplay = None
    if headless:
        options.add_argument("--headless")
    else:
        vdisplay = Xvfb(width=1080, height=540)
        vdisplay.start()
    if blockImages:
        options.add_experimental_option("prefs", {
            "profile.managed_default_content_settings.images": 2  # 2: Block all images
        })
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-translate")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-blink-features=AutomationControlled")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)  # Change to webdriver.Chrome
    if headless:
        return driver
    else:
        return (driver, vdisplay)

def backup_minecraft_server():
    pass

def share_nightcafe_creation():
    pass

def add_90_min_minecraft_server():
    # Setup WebDriver
    driver = start_chrome_driver()
    
    # Define your server URL and login details
    server_login_url = 'https://panel.gaming4free.net/auth/login'
    server_url = 'https://panel.gaming4free.net/server/fb97ea2c/console'
    username = os.environ['mine_email']
    password = os.environ['mine_pass']
    
    try:
        # Login to the website
        driver.get(server_login_url)
        time.sleep(2)

        # Enter username
        username_field = driver.find_element(By.NAME, 'username')  # Adjust based on the actual element name or id
        username_field.send_keys(username)

        # Enter password
        password_field = driver.find_element(By.NAME, 'password')  # Adjust based on the actual element name or id
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        time.sleep(5)  # Adjust based on your internet speed

        # Navigate to server control panel and start server
        driver.get(server_url)  # Adjust based on actual URL
        
        extend_time_btn= WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'VideoAd___StyledButton-sc-ye3fb7-0')))
        extend_time_btn.click()
        time.sleep(90)
        return "Time extended successfully"
        
    except Exception:
        driver.save_screenshot('Minecraft_server_add_90_error_screenshot.png')
        error_message = traceback.format_exc()
        print(error_message)
        send_error_email("Error while extending time for Minecraft Server", "An error has occured while extending time for <b>gaming4free server</b><br><br>Error:<br>"+error_message.replace("\n", "<br>"))
        return "<h2>Failed to extend time for the server</h2>"
    finally:
        # Close the browser
        driver.quit()

def login_nightcafe():
    # Setup WebDriver
    driver, vdisplay = start_chrome_driver(headless=False, blockImages=True)
    
    # Define your login URL and credentials
    nc_url = "https://creator.nightcafe.studio/studio?view=password-login"
    email = os.environ['nc_email']
    password = os.environ['nc_pass']

    try:
        # Navigate to the login page
        driver.get(nc_url)
        
        try:
            #Waiting for Modal Popup
            time.sleep(10)
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-1slq7s7') and @data-testid='ModalCloseBtn']"))).click()
        except Exception:
            print("No modal appeared to be closed")

        #Waiting for login button
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "css-1t9177x")))
        login_btns = driver.find_elements(By.CLASS_NAME, "css-1t9177x")
        login_btn_clicked = False
        for login_btn in login_btns:
            if login_btn.text.lower() == "login now":
                login_btn.click()
                login_btn_clicked = True
                break
                
        if not login_btn_clicked:
            raise Exception("Login button not found")
            
        # Fill in the form fields
        email_input = driver.find_element(By.ID, 'email')
        password_input = driver.find_element(By.ID, 'password')

        email_input.send_keys(email)
        password_input.send_keys(password)

        # Submit the form
        password_input.send_keys(Keys.RETURN)

        time.sleep(15)
        #Clicking on close modal popup button
        driver.find_element(By.XPATH, "//button[contains(@class, 'css-1slq7s7') and @data-testid='ModalCloseBtn']").click()
        time.sleep(1)
        #filling prompt
        driver.find_element(By.ID, "promptField").send_keys("A beautiful nature scene.")
        #Clicking create button
        driver.find_element(By.CLASS_NAME, "css-17wi8vr").click()

        # Find the inbox button using XPath
        inboxBtn = driver.find_element(By.XPATH, "//button[contains(@class, 'css-gc0ltf') and @data-testid='InboxBtn']")
        inboxBtn.click()
        #Waiting for credit claim buttons
        WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-136srwg")))
        # Find all elements with the class 'css-136srwg'
        credit_claim_btns = driver.find_elements(By.CLASS_NAME, 'css-136srwg')
        credit_claimed = False
        # Loop through the elements and find the one with the text 'Claim 5 credits'
        for button in credit_claim_btns:
            if "claim" in button.text.lower() and "credit" in button.text.lower():
                button.click()  # Click the button
                credit_claimed = True
                
        if not credit_claimed:
            raise Exception("Credit claim button not found")

        #Waiting for credit to be claimed
        time.sleep(5)
        
        return "Login and credit claim success"
    except Exception:
        driver.save_screenshot("nightcafe_error.png")
        error_message = traceback.format_exc()
        print(error_message)
        send_error_email("Error while logging in to Nightcafe", "An error has occured when logging and claiming credit in <b>Nightcafe</b><br><br>Error:<br>"+error_message.replace("\n", "<br>"))
        return "Login or credit claim failed due to some error" + error_message
    finally:
        # Close the browser
        driver.quit()
        vdisplay.stop()

def start_minecraft_server():
    # Setup WebDriver
    driver = start_chrome_driver()
    
    # Define your server URL and login details
    server_login_url = 'https://panel.gaming4free.net/auth/login'
    server_url = 'https://panel.gaming4free.net/server/fb97ea2c/console'
    username = os.environ['mine_email']
    password = os.environ['mine_pass']
    server_started = False
    
    try:
        # Login to the website
        driver.get(server_login_url)
        time.sleep(2)

        # Enter username
        username_field = driver.find_element(By.NAME, 'username')  # Adjust based on the actual element name or id
        username_field.send_keys(username)

        # Enter password
        password_field = driver.find_element(By.NAME, 'password')  # Adjust based on the actual element name or id
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        time.sleep(40) # Adjust based on your internet speed

        # Navigate to server control panel and start server
        driver.get(server_url)  # Adjust based on actual URL
        
        wait = WebDriverWait(driver, 10)
        
        try:
            #Now finding start server button
            start_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'PowerControls___StyledButton-sc-5aruet-1')))                           
        except Exception:
            try:
                #Finding renew server button
                renew_server_btn = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'VideoAd___StyledButton-sc-ye3fb7-0')))
                renew_server_btn.click()
                wait = WebDriverWait(driver, 120)
                start_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'PowerControls___StyledButton-sc-5aruet-1'))) 
            except Exception as r:
                driver.save_screenshot("error_screenshot.png")  # Save a screenshot for debugging
                raise r

        #Waiting for start button to get enabled
        time.sleep(10)
        # Check if the start button is enabled
        if start_button.is_enabled():
            start_button.click()
            server_started = True
            return "Server started successfully"
        else:
            server_status = driver.find_element(By.CLASS_NAME, 'ServerDetailsBlock___StyledSpan-sc-8gx06f-2')
            if "running" in server_status.text.lower():
                return "Server is already running" 
            elif "connecting" in server_status.text.lower():
                time.sleep(10)
                server_status = driver.find_element(By.CLASS_NAME, 'ServerDetailsBlock___StyledSpan-sc-8gx06f-2')
                if "running" in server_status.text.lower():
                    return "Server is already running" 
                else:
                    raise Exception("Server is not functioning")
            else:
                raise Exception("Server is not functioning")
    except Exception:
        driver.save_screenshot('Minecraft_server_error_screenshot.png')
        error_message = traceback.format_exc()
        print(error_message)
        send_error_email("Error while starting Minecraft Server", "An error has occured when starting <b>gaming4free server</b><br><br>Error:<br>"+error_message.replace("\n", "<br>"))
        return "<h2>Failed to start the server</h2>"
    finally:
        # Wait for server to start if the start button was clicked
        if server_started:
            time.sleep(5)
        
        # Close the browser
        driver.quit()

def login_to_heliohost():
    # Setup WebDriver
    driver = start_chrome_driver()
    
    # Define your login URL and credentials
    login_url = 'https://heliohost.org/login/'
    email = os.environ['helio_email']
    password = os.environ['helio_pass']

    try:
        # Navigate to the login page
        driver.get(login_url)
        time.sleep(2)        

        # Use JavaScript to remove the existing form from the DOM
        driver.execute_script("document.querySelector('form').remove();")
        """# Define your custom form HTML
        custom_form_html = '''
        <form id="custom_login_form" action="." method="post">
            <input type="text" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <input type="hidden" name="redirect" value="/dashboard/">
            <input type="submit" value="Login">
            <a href="/reset/" class="button">Reset</a>
        </form>
        '''
        
        # Use JavaScript to inject the custom form into the DOM
        driver.execute_script(f"document.body.innerHTML += `{custom_form_html}`;")
        
        # Allow some time for the form to be injected
        time.sleep(2)
        """
        # Fill in the form fields
        email_input = driver.find_element(By.NAME, 'email')
        password_input = driver.find_element(By.NAME, 'password')
        
        email_input.send_keys(email)
        password_input.send_keys(password)
        
        # Submit the form
        password_input.send_keys(Keys.RETURN)
        
        time.sleep(2)
        # Wait for the next page to load by checking for the image with alt="Plesk"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//img[@alt="Plesk"]'))
        )
        
        return "Login successful"
    except Exception:
        driver.save_screenshot("heliohost_error_screenshot.png")
        error_message = traceback.format_exc()
        print(error_message)
        send_error_email("Error while logging in to Heliohost", "An error has occured when logging in to <b>Heliohost</b><br><br>Error:<br>"+error_message.replace("\n", "<br>"))
        return "Login failed due to some error"
    finally:
        # Close the browser
        driver.quit()

# Function to send error to WordPress server
def send_error_email(subject, error_message):
    import requests
    import urllib.parse
    email_url = urllib.parse.quote(wordpress_url+f"/Apps/automation-app/email-error.php?subject={subject}&error_message=") + urllib.parse.quote(error_message.replace("#", "**hash**"))
    reponse = requests.get(pagespeed_url + "?url=" + email_url)
    return reponse.text
