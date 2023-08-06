import argparse
import logging
import numpy as np
import os
import pyautogui
import random
import sys
import textwrap
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeDriverManager

# Configure the logger
logging.basicConfig(
    filename='share.log',  # Specify the log file name
    level=logging.DEBUG, # Set the logging level to DEBUG or higher
    format='[%(levelname)s] %(asctime)s - %(message)s') # Specify the log message format
)
logger = logging.getLogger(__name__)

# Constants for web drivers
DRIVER_CHROME = 'chrome'
DRIVER_SAFARI = 'safari'
DRIVER_FIREFOX = 'firefox'
DRIVER_EDGE = 'edge'

# Mapping dictionary for drivers
DRIVER_OPTIONS = {
    DRIVER_CHROME: webdriver.Chrome,
    DRIVER_SAFARI: webdriver.Safari,
    DRIVER_FIREFOX: webdriver.Firefox,
    DRIVER_EDGE: webdriver.Edge,
}

# Function to set up the driver
def setup_driver(driver_name):
    try:
        driver_name = driver_name.lower()
        if driver_name in DRIVER_OPTIONS:
            options = DRIVER_OPTIONS[driver_name]()
            if driver_name == DRIVER_EDGE:
                driver = webdriver.Edge(executable_path=EdgeDriverManager().install(), options=options)
            else:
                driver = DRIVER_OPTIONS[driver_name](options=options)
            return driver
        else:
            raise ValueError("Driver argument value not supported! Check the help (-h) argument for supported values.")
    except Exception as e:
        logger.error("Error occurred while initializing the driver: %s", e)
        sys.exit(1)
    

# Add the handle_captcha function
def handle_captcha():
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
        logger.info("[*] Exiting the script.")
        sys.exit()

# Add the check_quit_input function
def check_quit_input():
    quit_mes = textwrap.dedent('''
        [*] if you would like to quit, enter [q]
            otherwise, enter any other key to continue
    ''')
    quit_selection = input(quit_mes)
    qs = str(quit_selection).lower()
    if qs == 'q':
        global quit_input
        quit_input = True
    else:
        pass

        
# Modify the login function
def login(debugger=False):
    max_retries = 5  # Set the maximum number of retries
    retries = 0
    
    if debugger is True:
        import pdb; pdb.set_trace()
    else:
        pass

    url = "https://poshmark.com/login"
    driver.get(url)

    time.sleep(get_random_delay(5))

    while retries < max_retries:
        try:
            ## Login
            logger.info(textwrap.dedent('''
                [*] logging into Poshmark seller account: {}...
                    the share war will begin momentarily...
                '''.format(poshmark_username)))
            username = driver.find_element_by_name("login_form[username_email]")
            username.send_keys(poshmark_username)
            time.sleep(get_random_delay(5))

            password = driver.find_element_by_name("login_form[password]")
            password.send_keys(poshmark_password)
            time.sleep(get_random_delay(5))

            password.send_keys(Keys.RETURN)
            time.sleep(get_random_delay(5))
        
            ## Check for Captcha
            try:
                captcha_pat = "//span[@class='base_error_message']"
                captcha_fail = driver.find_element_by_xpath(captcha_pat)
                if len(str(captcha_fail)) > 100:
                    logger.info("Captcha detected. Manual intervention required.")
                    handle_captcha()  # Call the handle_captcha function
                    retries += 1  # Increment the retries counter

                    if login(debugger=True)  # Retry login after manual intervention
                return
                    continue
            except NoSuchElementException:
                pass

            # Login successful, break out of the loop
            break

        except Exception as e:
            # Captcha Catch
            logger.info(textwrap.dedent('''
                [*] ERROR in Share Bot: Thwarted by Captchas
                    you may now attempt to login with the python debugger
                '''))
            logger.error("Error occurred during login: %s", e)
            check_quit_input()
            if quit_input:
                break
            retries += 1  # Increment the retries counter
            time.sleep(get_random_delay(30)) # Wait for a few seconds before retrying

    else:
        # The loop completed without successful login, handle the situation accordingly
        logger.info("Login failed after multiple attempts. Exiting the script.")
        sys.exit()
    
    # Continue with the rest of the login process
    time.sleep(get_random_delay(10))
    seller_page = get_seller_page_url(args.account)
    driver.get(seller_page)

    ## Confirm Account to Share If Not Username
    if args.bypass == True:
        pass
    else:
        if args.account != poshmark_username:
            confirm_account_sharing(args.account, poshmark_username)
            if quit_input is True:
                return False
            else:
                pass
        else:
            pass
                
    return True
    

def deploy_share_bot(driver, n=3, order=True, random_subset=0):
    logger.info("[*] DEPLOYING SHARE BOT")
    
    try:
        if login() is True:
            pass
        else:
            return

        scroll_page(n)

        ## Share Icons and Order
        share_icons = get_closet_share_icons()

        if order is True:
            share_icons.reverse()
        else:
            pass

        ## Share Random Subset of Items
        if random_subset != 0:
            try:
                random_subset = int(random_subset)
                print(textwrap.dedent('''
                    [*] you have selected to share a random subset of {} items
                        from all {} PoshMark listings in the closet...
                        please wait...
                    '''.format(random_subset, len(share_icons))))

                share_icons = np.random.choice(share_icons, random_subset, replace=False).tolist()

            except Exception as e:
                logger.warning("Error occurred while selecting random subset: %s", e)
                pass
        else:
            pass

        ## Share Message
        logger.info(textwrap.dedent('''
            [*] sharing PoshMark listings for {} items in closet...
                please wait...
            '''.format(len(share_icons))))
    
        
        ## Share Listings using Chrome driver
        for item in share_icons:
            clicks_share_followers(item)
            # Access the requests captured by selenium-wire for Chrome
            for request in chrome_driver.requests:
                if request.response:
                    logger.info(request.url)
                    logger.info(request.method)
                    logger.info(request.response.status_code)
                    logger.info(request.response.headers)
                    

        # Access the requests captured by selenium-wire for Safari
            for request in safari_driver.requests:
                if request.response:
                    logger.info(request.url)
                    logger.info(request.method)
                    logger.info(request.response.status_code)
                    logger.info(request.response.headers)

        ## Share Listings using Firefox driver
        for item in share_icons:
            clicks_share_followers(item)
            # Access the requests captured by selenium-wire for Firefox
            for request in firefox_driver.requests:
                if request.response:
                    logger.info(request.url)
                    logger.info(request.method)
                    logger.info(request.response.status_code)
                    logger.info(request.response.headers)
                    
        # Access the requests captured by selenium-wire for Edge
            for request in edge_driver.requests:
                if request.response:
                    logger.info(request.url)
                    logger.info(request.method)
                    logger.info(request.response.status_code)
                    logger.info(request.response.headers)

            logger.info("[*] closet successfully shared...posh-on...")
        pass
        
    except Exception as e:
        logger.info("[*] ERROR in Share Bot")
        logger.error("Error occurred during share war deployment: %s", e)
        pass

    ## Closing Message
    loop_delay = int(random_loop_time/60)
    current_time = time.strftime("%I:%M%p on %b %d, %Y")
    print(textwrap.dedent('''
        [*] the share war will continue in {} minutes...
            current time: {}
        '''.format(loop_delay, current_time)))
     logger.info(textwrap.dedent('''
        [*] the share war will continue in {} minutes...
            current time: {}
        '''.format(loop_delay, current_time)))




# Add the simulate_human_interaction function
def simulate_human_interaction():
    try:
        # Simulate mouse movement
        x, y = pyautogui.position()
        pyautogui.moveTo(x + 10, y + 10, duration=0.5)
        pyautogui.moveTo(x - 10, y - 10, duration=0.5)
        pyautogui.moveTo(x, y, duration=0.5)

        # Scroll up and down
        pyautogui.scroll(3)
        time.sleep(get_random_delay_for_interaction(2))
        pyautogui.scroll(-3)
    except Exception as e:
        logger.warning("Error occurred during simulating human interaction: %s", e)
        pass


def get_random_delay(mean_delay):
    times = np.random.rand(1000) + np.random.rand(1000) + mean_delay
    return np.random.choice(times, 1).tolist()[0]

def get_random_delay_for_interaction(mean_delay):
    return get_random_delay(mean_delay)


def confirm_account_sharing(account, username):

        ## Get User Input
        logger.info(textwrap.dedent('''
            [*] you have requested to share
                the items in another poshmark closet:
                ------------------------------------
                [*]: {}
                ------------------------------------
            '''.format(account)))
        confirm_mes = (textwrap.dedent('''
            [*] to confirm this request, enter [y]
                to cancel and share your closet items instead enter [n] :
            '''))

        confirm_selection = input(confirm_mes)
        cs = str(confirm_selection).lower()
        if cs == 'y':
            pass
        elif cs == 'n':
            ## Redirect to users's closet page
            seller_page = get_seller_page_url(username)
            driver.get(seller_page)
        else:
            logger.info('[*] you have entered an invalid selection...')
            check_quit_input()
            if quit_input is True:
                pass
            else:
               confirm_account_sharing(account, username)



def get_seller_page_url(poshmark_account):
    url_stem = 'https://poshmark.com/closet/'
    available = '?availability=available'
    url = '{}{}{}'.format(url_stem, poshmark_account, available)
    return url


def scroll_page(n, delay=3):
    try:
        scroll = 0
        screen_heights = [0]
    
        logger.info("[*] scrolling through all items in closet...")
    
        for i in range(1, n+1):
            scroll +=1
            scroll_script = "window.scrollTo(0, document.body.scrollHeight);"
            driver.execute_script(scroll_script)
            height = driver.execute_script("return document.documentElement.scrollHeight")
            last_height = screen_heights[-1:][0]
    
            if height == last_height:
                return
            else:
                screen_heights.append(height)
                time.sleep(get_random_delay(delay))
    except Exception as e:
        logger.warning("Error occurred during page scrolling: %s", e)
        pass


def get_closet_urls():
    items = driver.find_elements_by_xpath("//div[@class='item-details']")
    urls = [i.find_element_by_css_selector('a').get_attribute('href') for i in items]
    return urls


def get_closet_share_icons():
    try:
        item_pat = "//div[@class='social-info social-actions d-fl ai-c jc-c']"
        items = driver.find_elements_by_xpath(item_pat)
        share_icons = [i.find_element_by_css_selector("a[class='share']") for i in items]
        return share_icons
    except Exception as e:
        logger.error("Error occurred while getting closet share icons: %s", e)
        return []



def clicks_share_followers(share_icon, d=4.5):

    ## First share click
    driver.execute_script("arguments[0].click();", share_icon); 
    time.sleep(get_random_delay(d)

    ## Second share click
    share_pat = "//a[@class='pm-followers-share-link grey']"
    share_followers = driver.find_element_by_xpath(share_pat)
    driver.execute_script("arguments[0].click();", share_followers); 
    time.sleep(get_random_delay(d))


def open_closet_item_url(url):
    logger.info(url)
    driver.get(url)
    time.sleep(get_random_delay(5))


# Main loop implementation
def main_loop(driver, loop_time, number, order, random_subset, account, bypass):
    max_retries = 5  # Set the maximum number of retries
    while True:
        try:
            # Start Share Bot Loop
            global quit_input  # Ensure we use the global quit_input variable
            quit_input = False
            deploy_share_bot(driver, number, order, random_subset)

            if quit_input:
                break

            time.sleep(get_random_delay(10))

            # Time Delay: While Loop
            random_loop_time = random(loop_time)
            time.sleep(get_random_delay(random_loop_time - ((time.time() - starttime) % random_loop_time)))

        except NoSuchElementException as e:
            # Handle NoSuchElementException
            logger.error("Element not found: %s", e)
            check_quit_input()
            if quit_input:
                driver.quit()
                sys.exit()
            else:
                pass
                
        except Exception as e:
            # Handle other exceptions
            logger.error("ERROR: %s", e)
            check_quit_input()
            if quit_input:
                pass
            else:
                # Sleep for some time before retrying
                time.sleep(get_random_delay(30))
                
            # Retry loop
            retries = 0
            while retries < max_retries:
                try:
                    # Continue with the next iteration of the main loop
                    break
                except Exception as e:
                    # Retry again
                    logger.error("ERROR (Retry %d): %s", retries+1, e)
                    time.sleep(get_random_delay(30))
                    retries += 1
            else:
                # The loop completed without success, handle the situation accordingly
                logger.error("Exceeded maximum retries. Exiting the script.")
                sys.exit()

    driver.quit()
    sys.exit()



if __name__ == "__main__":
        
    ##################################
    ## Arguments for Script
    ##################################

    ## Default Arguments with RawTextHelpFormatter
    class RawTextArgumentDefaultsHelpFormatter(
            argparse.ArgumentDefaultsHelpFormatter,
            argparse.RawTextHelpFormatter
        ):
            pass

    exists = os.path.isfile('./credentials.py')
    if not exists:
        logger.info(textwrap.dedent('''
            [*] ERROR: `credentials.py` file does not exist.
                You may need to create the file, for example, 
                by copying `example_credentials.py`...

            [*] In terminal, enter the following command:
                cp example_credentials.py credentials.py

            [*] Then edit credentials.py with your
                poshmark closet and password.
                '''))
        sys.exit()
    else:
        import credentials

    
    ## Fail gracefully if the username or password not specified
    try:
        poshmark_username = credentials.poshmark_username
        poshmark_password = credentials.poshmark_password
    except AttributeError:
       logger.info(textwrap.dedent('''
            [*] ERROR: Username and/or password not specified...
            [*] You may need to uncomment poshmark_username and 
                poshmark_password in credentials.py
            '''))
        sys.exit()
    )

    ## Poshmark closet URL only works with username, so verify
    ## that the user is not using their email address to log in.
    if '@' in poshmark_username:
        logger.info(textwrap.dedent('''
                    [*] Do not your user email address to log in...
                        use your Poshmark username (closet) instead...
                    '''))
        sys.exit()


    parser = argparse.ArgumentParser(
        description=textwrap.dedent('''
        [*] Help file for share.py
            from the poshmark_sharing repository:
            https://github.com/jmausolf/poshmark_sharing
        '''),
        usage='use "python %(prog)s --help" for more information',
        formatter_class=RawTextArgumentDefaultsHelpFormatter)
    parser.add_argument("-t", "--time", default=14400, type=float,
        help=textwrap.dedent('''\
            loop time in seconds to repeat the code

            :: example, repeat in two hours:
            -t 7200
            '''))
    parser.add_argument("-n", "--number", default=1000, type=int,
        help="number of closet scrolls")
    parser.add_argument("-o", "--order", default=True, type=bool, 
        help="preserve closet order")
    parser.add_argument("-r", "--random_subset", default=0, type=int, 
        help="select a random subset (number) of items to share")
    parser.add_argument("-a", "--account", default=poshmark_username, 
        type=str,help=textwrap.dedent('''\
            the poshmark closet account you want to share
            (default is the login account in credentials.py)

            :: example, share another user's closet items:
            -a another_username
            '''))
    parser.add_argument("-b", "--bypass", default=False, type=bool, 
        help=textwrap.dedent('''\
            option to bypass user confirmation
            by default, if the account to be shared is not equal
            to the poshmark username, the user will be prompted to 
            confirm this selection

            :: example, bypass user confirmation
            -b True
            '''))
    parser.add_argument("-d", "--driver", default='0', type=str, 
        help=textwrap.dedent('''\
            selenium web driver selection
            drivers may be called by either entering the name
            of the driver or entering the numeric code 
            for that driver name as follows:
            Chrome == 0, Safari == 1, Firefox == 2, Edge == 3

            :: example, use Firefox:
            -d Firefox 
            -d 2

            :: example, use Chrome:
            -d Chrome
            -d 0
            '''))

    args = parser.parse_args()

    ##################################
    ## Set up Webdriver
    ##################################

    try:
        driver = setup_driver(args.driver)
    except ValueError as e:
        logger.error("ERROR: %s", e)
        sys.exit()

    main_loop(driver, args.time, args.number, args.order, args.random_subset, args.account, args.bypass)

    driver.quit()
    sys.exit()

    
if __name__=="__main__":


    ## Poshmark closet URL only works with username, so verify
    ## that the user is not using their email address to log in.
    if '@' in poshmark_username:
        logger.info(textwrap.dedent('''
                    [*] Do not your user email address to log in...
                        use your Poshmark username (closet) instead...
                    '''))
        sys.exit()


    parser = argparse.ArgumentParser(
        description=textwrap.dedent('''
        [*] Help file for share.py
            from the poshmark_sharing repository:
            https://github.com/jmausolf/poshmark_sharing
        '''),
        usage='use "python %(prog)s --help" for more information',
        formatter_class=RawTextArgumentDefaultsHelpFormatter)
    parser.add_argument("-t", "--time", default=14400, type=float,
        help=textwrap.dedent('''\
            loop time in seconds to repeat the code

            :: example, repeat in two hours:
            -t 7200
            '''))

       

