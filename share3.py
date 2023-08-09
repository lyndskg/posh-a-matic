import argparse
import logging
import numpy as np
import os
import pyautogui
import random
import sys
import textwrap
import time
import credentials 
import pdb

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions

# TODO: Handle safari driver manager 
from selenium.webdriver.safari.webdriver import WebDriver as SafariDriver
from selenium.webdriver.safari.options import Options as SafariOptions

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager

from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options as EdgeOptions

# Configure the logger
logging.basicConfig(
    filename='share.log',  # Specify the log file name
    level=logging.DEBUG, # Set the logging level to DEBUG or higher
    format='[%(levelname)s] %(asctime)s - %(message)s' # Specify the log message format
)
logger = logging.getLogger(__name__)


# Constants for web drivers
DRIVER_CHROME = 'chrome'
DRIVER_SAFARI = 'safari'
DRIVER_FIREFOX = 'firefox'
DRIVER_EDGE = 'edge'

# # Mapping dictionary for drivers
DRIVER_OPTIONS = {
    DRIVER_CHROME: webdriver.Chrome,
    DRIVER_SAFARI: webdriver.Safari,
    DRIVER_FIREFOX: webdriver.Firefox,
    DRIVER_EDGE: webdriver.Edge,
}

# # Function to set up the driver
# def setup_driver(driver_name):
#     try:
#         # Convert the driver_name to lowercase for consistent comparison
#         driver_name = driver_name.lower()

#         # Check if the provided driver_name is supported
#         if driver_name in DRIVER_OPTIONS:
#             # Check the specific driver_name to create the appropriate driver instance
#             if driver_name == DRIVER_CHROME:
#                 # Create an instance of ChromeOptions
#                 chrome_options = ChromeOptions()
#                 # Create a Chrome driver instance with ChromeDriverManager and pass chrome_options as an argument
#                 driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
#                 driver.implicitly_wait(10)
#                 return driver
#             # TODO: EXTEND SAFARI FUNCTIONALITIES
#             elif driver_name == DRIVER_SAFARI:
#                 # Create an instance of SafariOptions 
#                 safari_options = SafariOptions()
#                 # Create a Safari driver instance with SafariDriver and pass safari_options as an argument
#                 driver = webdriver.Safari(SafariDriver().install(), options = safari_options)
#                 driver.implicitly_wait(10)
#                 return driver
#             elif driver_name == DRIVER_FIREFOX:
#                 # Create an instance of FirefoxOptions 
#                 firefox_options = FirefoxOptions()
#                 # Create a Firefox driver instance with GeckoDriverManager and pass firefox_options as an argument
#                 driver = webdriver.Firefox(options = firefox_options)
#                 driver.implicitly_wait(10)
#                 return driver
#             elif driver_name == DRIVER_EDGE:
#                 # Create an instance of EdgeOptions
#                 edge_options = EdgeOptions()
#                 # Create an Edge driver instance with EdgeChromiumDriverManager and pass edge_options as an argument
#                 driver = webdriver.Edge(EdgeChromiumDriverManager().install(), options = edge_options)
#                 driver.implicitly_wait(10)
#                 return driver
#             else: 
#                 # Print an error message to the console and log the error
#                 print(textwrap.dedent('''
#                     [*] ERROR Driver argument value not supported!
#                         Check the help (-h) argument for supported values.
#                     '''))
            
#                 logger.info(textwrap.dedent('''
#                     [*] ERROR Driver argument value not supported!
#                         Check the help (-h) argument for supported values.
#                     '''))

#     except ValueError as v:
#         # Log and display error messages if a ValueError occurs   
#         logger.error("Error occurred during driver setup: %s", v)
        
#         print("[*] ERROR Driver argument value not supported! Check the help (-h) argument for supported values.")
        
#         logger.info("[*] ERROR Driver argument value not supported! Check the help (-h) argument for supported values.")
#         sys.exit(-1)

#     except NameError as n:
#         # Log and display error messages if a NameError occurs
#         logger.error("Error occurred during driver setup: %s", n)
        
#         print(textwrap.dedent('''
#             [*] ERROR You don't have the web driver for argument
#                 given ({}) you need to download it, go here for
#                 installation info:
#                 https://selenium-python.readthedocs.io/installation.html#drivers
#             '''.format(driver)))
        
#         logger.info(textwrap.dedent('''
#             [*] ERROR You don't have the web driver for argument
#                 given ({}) you need to download it, go here for
#                 installation info:
#                 https://selenium-python.readthedocs.io/installation.html#drivers
#             '''.format(driver)))
        
#         sys.exit(-2)

#     except Exception as e:
#         # Log and display error messages
#         logger.error("Error occurred while initializing the driver: %s", e)
        
#         print(textwrap.dedent('''
#             [*] ERROR the selected driver may not be setup correctly. 
#                 Ensure you can access it from the command line and 
#                 try again. 
#                 {}
#             '''.format(e)))

#         logger.info(textwrap.dedent('''
#             [*] ERROR the selected driver may not be setup correctly. 
#                 Ensure you can access it from the command line and 
#                 try again. 
#                 {}
#             '''.format(e)))
        
#         sys.exit(-3)
#     else: 
#         pass

class PoshAMatic:
    def __init__(self, poshmark_username, poshmark_password, slowMode = False, debug = False, debugger = False, checkCaptcha = True, file = False, timeToWait = 7200, maintainOrder = False, shareBack = False):
        self.poshmark_username = poshmark_username
        self.poshmark_password = poshmark_password
        self.numItemsToShareFromOtherClosets = 8
        self.timeOutSecs = 10
        self.scrollWaitTime = 5
        self.numTimesToScroll = 5
        self.chrome_options = ChromeOptions()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(options = self.chrome_options)
        # self.driver = setup_driver(args.driver)
        self.closetUrl = "https://poshmark.com/closet"
        self.shareNewsUrl = "https://poshmark.com/news/share"
        self.closetStatsUrl = "https://poshmark.com/users/self/closet_stats"
        self.statsXPath = "((//div[@class='stats-container__border stats__content'])[1]//h1[@class='posh-stats__value'])[1]"
        self.loginID = "login_form_username_email"
        self.loginXPath = "//input[@name='userHandle']"
        self.passwordID = "login_form_password"
        self.passwordXPath = "//input[@name='password']"
        self.firstShareXPath = "//i[@class='icon share-gray-large']"
        self.socialBarXPath = "//div[@class='social-action-bar tile__social-actions']"
        self.itemNameXPath = "//a[@class='tile__title tc--b']"
        self.secondShareXPath = "//i[@class='icon pm-logo-white']"
        self.shareModalTitleXPath = "//h5[@class='modal__title']"
        self.captchaModalTitleXPath = "//h5[@class='modal__title']"
        self.captchaXButtonXPath = "//button[@class='btn btn--close modal__close-btn simple-modal-close']"
        self.closetNameXPath = "//p[@class='wb--ww tc--g']//a" # used for sharing back
        self.followButtonXPath = "//button[@class='al--right btn follow__btn m--l--2 m--r--1 btn--primary']" # used to follow
        if maintainOrder: 
            self.orderTextFile = "order.txt"
        else:
            self.orderTextFile = ""
        self.closetsToShareFile = "closetsToShare.txt"
        self.availableUrl = self.getClosetAvailableUrl(self.poshmark_username)
        self.hasUpdate = False # used when preserving closet order to keep track of newly added item
        self.closetSize = 0
        self.shareButtons = []
        self.orderedShareButtons = []
        self.itemNameElements = []
        self.itemNames = []
        self.closetOrder = []
        self.closetOrderDict = {}
        self.closetSharedBack = []
        self.checkCaptcha = checkCaptcha
        self.file = file
        self.debug = debug
        self.debugger = debugger
        self.shareBack = shareBack
        self.slowMode = slowMode
        self.timeToWait = timeToWait
        self.driver.minimize_window()


    # Modify the login function
    def login(self, debugger = False):
        # If debugger flag is True, enable Python debugger (pdb)
        if debugger is True:
            import pdb; pdb.set_trace()
        else:
            pass # Otherwise, continue without debugger

        # Set the maximum number of retries
        max_retries = 5 
        retries = 0
        
        # URL of the Poshmark login page
        url = "https://poshmark.com/login"
        self.driver.get(url) # Open the URL in the driver's browser

        time.sleep(random.random()) # Wait for a random delay before proceeding

        # Attempt login with retry mechanism
        while retries < max_retries:
            try:
                ## Perform login
                print(textwrap.dedent('''
                    [*] Logging into Poshmark seller account "{}"...
                        The share war will begin momentarily...
                    '''.format(poshmark_username)))
                
                logger.info(textwrap.dedent('''
                    [*] Logging into Poshmark seller account "{}"...
                        The share war will begin momentarily...
                    '''.format(poshmark_username)))
                
                self.enterUsername()
                self.enterAndSubmitPassword()

                
                try:
                    self.username = self.driver.find_element(By.NAME, "login_form[username_email]")
                    logger.info("Username obtained")

                    if not self.username:
                        raise ValueError 
                
                    for c in poshmark_username:
                        self.username.send_keys(c)
                        time.sleep(random.random())
                except ValueError: 
                    print("Username element not obtained from page. Exiting...")
                    self.quit()
                    sys.exit()
                except Exception as e:
                    print("Username element not obtained from page. Exiting...")
                    self.quit()
                    sys.exit()

                self.username.send_keys(poshmark_username)

                time.sleep(random.random())

                password = driver.find_element(By.NAME, "login_form[password]")
                password.send_keys(poshmark_password)
                time.sleep(random.random())

                password.send_keys(Keys.RETURN)
                time.sleep(random.random())
            
                ## Check for Captcha
                try:
                    captcha_fail = driver.find_element(By.XPATH, "//h5[@class='modal__title']")
                    ## If Captcha is detected
                    if len(str(captcha_fail)) > 100:
                        print("Captcha detected. Manual intervention required.")
                        logger.info("Captcha detected. Manual intervention required.")
                        
                        handle_captcha()  # Call the handle_captcha function
                        
                        retries += 1  # Increment the retries counter

                        # Retry login after manual intervention
                        if login(debugger = True): 
                            return
                        continue
                except NoSuchElementException:
                    pass

                # Login successful, break out of the loop
                break

            except Exception as e:
                # Handle Captcha Challenge
                print(textwrap.dedent('''
                    [*] ERROR in Share Bot: Thwarted by Captchas
                        you may now attempt to login with the python debugger
                    '''))
                
                logger.info(textwrap.dedent('''
                    [*] ERROR in Share Bot: Thwarted by Captchas
                        you may now attempt to login with the python debugger
                    '''))
                
                logger.error("Error occurred during login: %s", e)

                check_quit_input()

                if quit_input:
                    break

                retries += 1  # Increment the retries counter

                time.sleep(random.random()) # Wait for a few seconds before retrying

        else:
            # The loop completed without successful login, handle the situation accordingly
            logger.info("Login failed after multiple attempts. Exiting the script.")
            
            sys.exit(-5)
        
        # Continue with the rest of the login process
        time.sleep(random.random())

        seller_page = get_seller_page_url(args.account)
        driver.get(seller_page)

        ## Confirm account to share if not username
        if (args.bypass == True):
            pass
        else:
            if (args.account != poshmark_username):
                confirm_account_sharing(args.account, poshmark_username)
                
                if (quit_input is True):
                    return False
                else:
                    pass

            else:
                pass
                    
        return True
    
    def enterAndSubmitPassword(self):
        passwordElt = self.getLoginElt(self.passwordID, self.passwordXPath)
        if not passwordElt:
            print("Password element not obtained from page, exiting...")
            self.quit()
            sys.exit()
        self.enterTxtSlowly(passwordElt, self.password)
        passwordElt.submit()


    def getLoginElt(self, eltID, eltXPath):
        elt = self.waitTilClickable("id", eltID)
        if not elt:
            print("Timed out while locating ID: " + eltID)
            elt = self.waitTilClickable("xpath", eltXPath)
            if not elt:
                print("Timed out again with XPath.")
                print("Please manually enter username and password, then type 'c' or 'continue'")
                pdb.set_trace()
        return elt


    def waitTilClickable(self, findByIdOrPath, idOrPath, timeOutSecs = 10):
      clickableElt = False
      if findByIdOrPath == 'id':
         try:
            clickableElt = WebDriverWait(self.driver, timeOutSecs).until(EC.element_to_be_clickable((By.ID, idOrPath)))
         except TimeoutException as e:
            print("Timed out at locating element by " + findByIdOrPath + " at " + str(idOrPath) + ": " + str(e))
            return False
      else:
         try:
            clickableElt = WebDriverWait(self.driver, timeOutSecs).until(EC.element_to_be_clickable((By.XPATH, idOrPath)))
         except TimeoutException as e:
            print("Timed out at locating element by " + findByIdOrPath + " at " + str(idOrPath) + ": " + str(e))
            return False
      return clickableElt
    

    # Add the handle_captcha function
    def handle_captcha():

        # Print informative messages about CAPTCHA challenge
        print("[*] ERROR in Share : Thwarted by Captchas")
        print("[*] Please open the browser to the Poshmark login page.")
        print("[*] Solve the CAPTCHA and log in as a human.")
        print("[*] Once you've successfully logged in, come back here.")
        print("[*] Press Enter to continue the script after solving the CAPTCHA.")

        # Log informative messages about CAPTCHA challenge
        logger.info("[*] ERROR in Share : Thwarted by Captchas")
        logger.info("[*] Please open the browser to the Poshmark login page.")
        logger.info("[*] Solve the CAPTCHA and log in as a human.")
        logger.info("[*] Once you've successfully logged in, come back here.")
        logger.info("[*] Press Enter to continue the script after solving the CAPTCHA.")
        
        # Wait for the user to press Enter to continue
        input("[*] If you want to quit, enter 'q' and press Enter.")

        # Check if the user wants to quit the script
        quit_choice = input().lower().strip()
        if quit_choice == 'q':
            # Print and log that the user chose to exit the script and exit
            print("[*] Exiting the script.")
            logger.info("[*] Exiting the script.")

            sys.exit(-4)


    # Add the check_quit_input function
    def check_quit_input():
        # Define the quit message for user input
        quit_mes = textwrap.dedent('''
            [*] if you would like to quit, enter [q]
                otherwise, enter any other key to continue
        ''')
        # Prompt the user with the quit message and store their input
        quit_selection = input(quit_mes)
        qs = str(quit_selection).lower() # Convert input to lowercase
        
        # Check if the user's input is 'q' (quit)
        if qs == 'q':
            global quit_input # Access the global quit_input variable
            quit_input = True # Set the global variable to True (indicating user wants to quit)
        else:
            pass # If user doesn't want to quit, continue with the script


        

    # Define the deploy_share_bot function
    def deploy_share_bot(driver, n = 3, order = True, random_subset = 0):
        # Log and print the initiation of the share bot
        logger.info("[*] DEPLOYING SHARE BOT")
        print("[*] DEPLOYING SHARE BOT")
        
        try:
            # Attempt to perform the following steps within a try block
            if login():
                pass  # If login is successful, continue; otherwise, return
            else:
                return # If login is not successful, exit the function

            # Scroll the page to load more items
            scroll_page(n)

            ## Share Icons and Order
            # Get the icons of items available for sharing
            share_icons = get_closet_share_icons()

            if order is True:
                share_icons.reverse() # Reverse the order of sharing icons if specified
            else:
                pass

            ## Share Random Subset of Items
            if random_subset != 0:
                try:
                    random_subset = int(random_subset)
                    # Log and print information about sharing a random subset of items
                    logger.info(textwrap.dedent('''
                        [*] you have selected to share a random subset of {} items
                            from all {} PoshMark listings in the closet...
                            please wait...
                        '''.format(random_subset, len(share_icons))))
                    
                    print(textwrap.dedent('''
                        [*] you have selected to share a random subset of {} items
                            from all {} PoshMark listings in the closet...
                            please wait...
                        '''.format(random_subset, len(share_icons))))

                    # Randomly select a subset of items to share
                    share_icons = np.random.choice(share_icons, random_subset, replace=False).tolist()

                except Exception as e:
                    print("Error occurred while selecting random subset: %s", e)
                    logger.warning("Error occurred while selecting random subset: %s", e)
                    pass  # If there's an error, log a warning and continue
            else:
                pass

            ## Share Message
            # Log and print the sharing message with the number of items to be shared
            logger.info(textwrap.dedent('''
                [*] sharing PoshMark listings for {} items in closet...
                    please wait...
                '''.format(len(share_icons))))
            
            print(textwrap.dedent('''
                [*] sharing PoshMark listings for {} items in closet...
                    please wait...
                '''.format(len(share_icons))))
        
            
            ## Share Listings
            # Iterate through each item and share it with followers
            for item in share_icons:
                clicks_share_followers(item)

                # Access and log the captured requests using selenium-wire
                for request in driver.requests:
                    if request.response:
                        print(request.url)
                        logger.info(request.url)

                        print(request.method)
                        logger.info(request.method)

                        print(request.reponse.status_code)
                        logger.info(request.response.status_code)

                        print(request.response.headers)
                        logger.info(request.response.headers)
                        

            
            # Log and print successful sharing completion message
            logger.info("[*] closet successfully shared...posh-on...")
            print("[*] closet successfully shared...posh-on...")

            pass
            
        except Exception as e:
            # Catch and log and print any exceptions that occurred during the share bot deployment
            logger.info("[*] ERROR in Share Bot")
            print("[*] ERROR in Share Bot")

            logger.error("Error occurred during share war deployment: %s", e)
            print("Error occurred during share war deployment: %s", e)

            pass # Continue the script even if an error occurred

        ## Closing Message
        # Calculate loop delay in minutes and format the current time
        loop_delay = int(random_loop_time/60)
        current_time = time.strftime("%I:%M%p on %b %d, %Y")

        # Log and print the delay and current time before the next iteration
        logger.info(textwrap.dedent('''
            [*] the share war will continue in {} minutes...
                current time: {}
            '''.format(loop_delay, current_time)))
        
        print(textwrap.dedent('''
            [*] the share war will continue in {} minutes...
                current time: {}
            '''.format(loop_delay, current_time)))
        


    # Add the simulate_human_interaction function
    def simulate_human_interaction():
        try:
            # Simulate mouse movement to create a human-like interaction pattern
            x, y = pyautogui.position()
            
            # Move the mouse cursor slightly to different positions
            pyautogui.moveTo(x + 10, y + 10, duration=0.5)
            pyautogui.moveTo(x - 10, y - 10, duration=0.5)
            pyautogui.moveTo(x, y, duration=0.5)

            # Scroll up and down to mimic human scrolling behavior
            pyautogui.scroll(3)
            
            # Pause for a random delay before further interaction
            time.sleep(get_random_delay_for_interaction(2))
            
            pyautogui.scroll(-3)  # Scroll back up

        except Exception as e:
            # Catch and log any exceptions that occurred during simulating interaction
            logger.warning("Error occurred during simulating human interaction: %s", e)
            print("Error occurred during simulating human interaction: %s", e)

            pass  # Continue the script even if an error occurred


    # Define the get_random_delay function
    def get_random_delay(self, mean_delay):
        # Generate a list of random times, adding two random values and the mean delay
        times = np.random.rand(1000) + np.random.rand(1000) + mean_delay
    
        # Choose and return a random time from the generated list
        return np.random.choice(times, 1).tolist()[0]


    # Define the get_random_delay_for_interaction function
    def get_random_delay_for_interaction(self, mean_delay):
        # Call the get_random_delay function to get a random delay
        return get_random_delay(mean_delay)


    # Define the confirm_account_sharing function
    def confirm_account_sharing(self, account, username):
        try:
            # Get user input for confirming account sharing request
            logger.info(textwrap.dedent('''
                [*] You have requested to share
                    the items in another Poshmark closet:
                    ------------------------------------
                    [*]: {}
                    ------------------------------------
                '''.format(account)))
            
            print(textwrap.dedent('''
                [*] You have requested to share
                    the items in another Poshmark closet:
                    ------------------------------------
                    [*]: {}
                    ------------------------------------
                '''.format(account)))
            
            confirm_mes = (textwrap.dedent('''
                [*] To confirm this request, enter [y].
                    To cancel and share your closet items instead, enter [n]:
                '''))
            
            confirm_selection = input(confirm_mes)
            cs = str(confirm_selection).lower()
            
            if cs == 'y':
                pass  # Proceed with account sharing
            elif cs == 'n':
                # Redirect to the user's own closet page
                seller_page = get_seller_page_url(username)
                driver.get(seller_page)
            else:
                # Handle invalid selection from the user
                logger.info('[*] You have entered an invalid selection...')
                print('[*] You have entered an invalid selection...')
                check_quit_input()  # Check if the user wants to quit
                
                if quit_input is True:
                    pass
                else:
                    confirm_account_sharing(account, username)  # Recurse to reconfirm
            
        except Exception as e:
            # Catch and log any exceptions that occurred during account sharing confirmation
            logger.warning("Error occurred during account sharing confirmation: %s", e)
            print("Error occurred during account sharing confirmation: %s", e)
            
            pass  # Continue the script even if an error occurred


    # Define the get_seller_page_url function
    def get_seller_page_url(poshmark_account):
        # Generate the URL for the seller's Poshmark closet page
        url_stem = 'https://poshmark.com/closet/'
        available = '?availability=available'
        url = '{}{}{}'.format(url_stem, poshmark_account, available)
        
        return url


    # Define the scroll_page function
    def scroll_page(n, delay = 3):
        try:
            scroll = 0
            screen_heights = [0]
        
            logger.info("[*] Scrolling through all items in closet...")
            print("[*] Scrolling through all items in closet...")
        
            for i in range(1, n + 1):
                scroll += 1
                scroll_script = "window.scrollTo(0, document.body.scrollHeight);"
                driver.execute_script(scroll_script)

                height = driver.execute_script("return document.documentElement.scrollHeight")
                last_height = screen_heights[-1:][0]
        
                if height == last_height:
                    return  # Reached the end of the page, exit
                else:
                    screen_heights.append(height)
                    time.sleep(random.random())  # Pause with random delay
    
        except Exception as e:
            # Catch and log any exceptions that occurred during page scrolling
            logger.warning("Error occurred during page scrolling: %s", e)
            print("Error occurred during page scrolling: %s", e)
            
            pass  # Continue the script even if an error occurred


    # Define the get_closet_urls function
    def get_closet_urls():
        # Find all items' details elements and extract their URLs
        items = driver.find_elements(By.XPATH, "//div[@class='item-details']")
        urls = [i.find_element(By.CSS_SELECTOR, "a").get_attribute('href') for i in items]
        
        return urls


    # Define the get_closet_share_icons function
    def get_closet_share_icons():
        try:
            item_pat = "//div[@class='social-info social-actions d-fl ai-c jc-c']"
            
            # Find all share icons within the closet items and return them
            items = driver.find_elements(By.XPATH, "item_pat")
            share_icons = [i.find_element(By.CSS_SELECTOR, "a[class='share']") for i in items]
            
            return share_icons
        
        except Exception as e:
            # Handle any exceptions that occurred during retrieving share icons
            logger.error("Error occurred while getting closet share icons: %s", e)
            print("Error occurred while getting closet share icons: %s", e)  
                
            return []


    # Define the clicks_share_followers function
    def clicks_share_followers(share_icon, d=4.5):
        try:
            ## First share click
            driver.execute_script("arguments[0].click();", share_icon); 
            time.sleep(random.random())

            ## Second share click
            share_pat = "//a[@class='pm-followers-share-link grey']"
            share_followers = driver.find_element(By.XPATH, "share_pat")
            
            driver.execute_script("arguments[0].click();", share_followers); 
            time.sleep(random.random())
        
        except Exception as e:
            # Handle any exceptions that occurred during clicking share icons
            logger.error("Error occurred while clicking share icons: %s", e)
            print("Error occurred while clicking share icons: %s", e)

            pass


    # Define the open_closet_item_url function
    def open_closet_item_url(url):
        logger.info(url)
        print(url)

        # Open the provided URL and wait for a random delay
        driver.get(url)
        time.sleep(random.random())



if __name__ == "__main__":
   
    slowMode = False
    debug = False
    debugger = False
    checkCaptcha = True
    file = False
    timeToWait = 7200
    maintainOrder = False
    shareBack = False
    

    ##################################
    ## Arguments for Script
    ##################################

     ## Create a custom argument formatter that supports raw text and default values
    class RawTextArgumentDefaultsHelpFormatter(
            argparse.ArgumentDefaultsHelpFormatter,
            argparse.RawTextHelpFormatter
        ):
            pass

    
    # Check if the 'credentials.py' file exists
    exists = os.path.isfile('./credentials.py')
    if not exists:
        # Inform the user if 'credentials.py' does not exist and provide instructions
        logger.info(textwrap.dedent('''
            [*] ERROR: `credentials.py` file does not exist.
                You may need to create the file, for example, 
                by copying `example_credentials.py`...

            [*] In terminal, enter the following command:
                cp example_credentials.py credentials.py

            [*] Then edit credentials.py with your
                poshmark closet and password.
                '''))
        print(textwrap.dedent('''
            [*] ERROR: `credentials.py` file does not exist.
                You may need to create the file, for example, 
                by copying `example_credentials.py`...

            [*] In terminal, enter the following command:
                cp example_credentials.py credentials.py

            [*] Then edit credentials.py with your
                poshmark closet and password.
                '''))
        
        sys.exit(-6)
    else:
        import credentials
    
    ## Fail gracefully if the username or password not specified in credentials.py
    try:
        poshmark_username = credentials.poshmark_username
        poshmark_password = credentials.poshmark_password
    except AttributeError:
        # Inform the user if username and/or password is missing and provide instructions
        logger.info(textwrap.dedent('''
            [*] ERROR: Username and/or password not specified...
            [*] You may need to uncomment poshmark_username and 
                poshmark_password in credentials.py
            '''))
        print(textwrap.dedent('''
            [*] ERROR: Username and/or password not specified...
            [*] You may need to uncomment poshmark_username and 
                poshmark_password in credentials.py
            '''))
        sys.exit(-7)
    
    ## Verify that the user is using their Poshmark username and not email
    if '@' in poshmark_username:
        # Inform the user to use Poshmark username for login
        logger.info(textwrap.dedent('''
                    [*] Do not use your email address to log in...
                        use your Poshmark username (closet) instead...
                    '''))
        print(textwrap.dedent('''
                    [*] Do not use your email address to log in...
                        use your Poshmark username (closet) instead...
                    '''))
        sys.exit(-8)

    # Define the argument parser with description and custom formatter
    parser = argparse.ArgumentParser(
        description=textwrap.dedent('''
        [*] Help file for share.py
            from the poshmark_sharing repository:
            https://github.com/lyndskg/posh-a-matic
        '''),
        Usage = 'Use "python3 %(prog)s --help" or "python3 share.py -h" for more information.',
        formatter_class=RawTextArgumentDefaultsHelpFormatter)
    # Add command line arguments for different options
    parser.add_argument("-ttw", "--timeToWait", default = 7200, type = float, required = False,
        help = textwrap.dedent('''\
            The number of seconds to wait after one round of sharing.

            :: e.g., repeat every two hours:
            -t 7200
            '''))
    parser.add_argument("-d", "--debug", default = False, type = bool, required = True,
        help = "Show debug output.")
    parser.add_argument("-pdb", "--debugger", default = False, type = bool, required = True,
        help = "Run with Python Debugger.")
    parser.add_argument("-sm", "--slowMode", default = False, type = bool, required = True,
        help = "Run in slow mode.")
    parser.add_argument("-cc", "--checkCaptcha", default = True, type = bool, required = False,
        help = "Specify whether or not to check for Captchas.")
    parser.add_argument("-mo", "--maintainOrder", default = False, type = bool, required = False,
        help = "Specify whether or not to preserve closet order based on order file.")
    parser.add_argument("-f", "--file", default = False, type = bool, required = True,
        help = "Specify whether or not to share closets in closetsToShare.txt.")
    parser.add_argument("-sb", "--shareBack", default = False, type = bool, required = False,
        help = "Specify whether or not to share back.")
    parser.add_argument("-d", "--driver", type = str, required = True,
        help=textwrap.dedent('''\
            Selenium WebDriver selection
                             
            Drivers may be called by either entering the name
            of the driver, or by entering the numeric code 
            for that driver name as follows:
            Chrome == 0, Safari == 1, Firefox == 2, Edge == 3

            :: e.g., use Firefox:
            -d Firefox 
            -d 2

            :: e.g., use Chrome:
            -d Chrome
            -d 0
            '''))

    # Parse the command line arguments
    args = parser.parse_args()

    global driver
    driver = setup_driver(args.driver) # Capture the returned driver

    poshamatic = PoshAMatic(poshmark_username, poshmark_password, slowMode, debug, debugger, checkCaptcha, file, timeToWait, maintainOrder, shareBack, driver)

    poshamatic.login()
    poshamatic.share()
    poshamatic.quit()
    
    ##################################
    ## Run Script
    ##################################

    
    ## Run Main App
    ## Start Share War Loop
    starttime = time.time()
 
    max_retries = 5  # Set the maximum number of retries

    global quit_input
    quit_input = False

    while quit_input is False:
        try:
            ## Time Delay: While Loop
            random_loop_time = get_random_delay(args.time)

            quit_input = False
            deploy_share_bot(driver, args.number, args.order, args.random_subset)

            if quit_input:
                break

            time.sleep(random.random())
            driver.close()

            time.sleep(random.random())


        except NoSuchElementException as e:
            # Handle NoSuchElementException
            logger.error("Element not found: %s", e)
            print("Element not found: %s", e)

            check_quit_input()

            if quit_input:
                driver.quit()
                sys.exit(-9)
            else:
                pass
                
        except Exception as e:
            # Handle other exceptions
            logger.error("ERROR: %s", e)
            print("ERROR: %s", e)

            check_quit_input()

            if quit_input:
                pass
            else:
                # Sleep for some time before retrying
                time.sleep(random.random())
                
            # Retry loop
            retries = 0
            while retries < max_retries:
                try:
                    # Continue with the next iteration of the main loop
                    break
                except Exception as e:
                    # Retry again
                    logger.error("ERROR (Retry %d): %s", retries + 1, e)
                    print("ERROR (Retry %d): %s", retries + 1, e)

                    time.sleep(random.random())
                
            else:
                # The loop completed without success, handle the situation accordingly
                logger.error("Exceeded maximum retries. Exiting the script.")
                print("Exceeded maximum retries. Exiting the script.")

                sys.exit(-10)

    driver.quit()
    sys.exit()
    