import selenium
import time
import argparse
import sys
import os
import textwrap
import numpy as np
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import pyautogui
from seleniumwire import webdriver as wirewebdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Add the manual_captcha_handler function
def manual_captcha_handler():
    # Function to handle manual CAPTCHA input
    # User must solve the CAPTCHA and log in as a human

    # Display instructions
    print("[*] ERROR in Price War: Thwarted by Captchas")
    print("[*] Please open the browser to the Poshmark login page.")
    print("[*] Solve the CAPTCHA and log in as a human.")
    print("[*] Once you've successfully logged in, come back here.")
    print("[*] Press Enter to continue the script after solving the CAPTCHA.")

    # Wait for user input
    input("[*] If you want to quit, enter 'q' and press Enter.")

    # Check if the user wants to quit the script
    quit_choice = input().lower().strip()
    if quit_choice == 'q':
        print("[*] Exiting the script.")
        sys.exit()

# Add the offer_user_quit function
def offer_user_quit():
    # Function to offer the user to quit the script

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
    # Existing code...

    try:
        # Existing code...

        ## Check for Captcha
        try:
            captcha_pat = "//span[@class='base_error_message']"
            captcha_fail = driver.find_element_by_xpath(captcha_pat)
            if len(str(captcha_fail)) > 100:
                manual_captcha_handler()  # Call the manual_captcha_handler function
                login(debugger=True)  # Retry login after manual intervention
                return
            else:
                pass
        except Exception as e:
            pass

        # Existing code...

    except:
        # Captcha Catch
        print("[*] ERROR in Price War: Thwarted by Captchas")
        offer_user_quit()
        login(debugger=True)
        pass

def deploy_price_war(n=3, order=True, random_subset=0):
    # Function to deploy the price war automation

    try:
        if login() is True:
            pass
        else:
            return

        scroll_page(n)

        ## Price Icons and Order
        price_icons = get_closet_price_icons()

        if order is True:
            price_icons.reverse()
        else:
            pass

        ## Price Random Subset of Items
        if random_subset != 0:
            try:
                random_subset = int(random_subset)
                print(textwrap.dedent('''
                    [*] you have selected to change prices for a random subset of {} items
                        from all {} PoshMark listings in the closet...
                        please wait...
                    '''.format(random_subset, len(price_icons))))

                price_icons = np.random.choice(price_icons, random_subset, replace=False).tolist()

            except:
                pass
        else:
            pass

        ## Price Message
        print(textwrap.dedent('''
            [*] changing PoshMark prices for {} items in closet...
                please wait...
            '''.format(len(price_icons))))
        
        ## Change Prices
        [change_item_price(item) for item in price_icons]

        print("[*] closet prices successfully changed...posh-on...")
        pass
        
    except:
        print("[*] ERROR in Price War")
        pass
    
    ## Closing Message
    loop_delay = int(random_loop_time/60)
    current_time = time.strftime("%I:%M%p on %b %d, %Y")
    print(textwrap.dedent('''
        [*] the price war will continue in {} minutes...
            current time: {}
        '''.format(loop_delay, current_time)))

# Add the simulate_human_interaction function
def simulate_human_interaction():
    # Function to simulate human interaction to avoid detection

    # Simulate mouse movement
    x, y = pyautogui.position()
    pyautogui.moveTo(x + 10, y + 10, duration=0.5)
   
