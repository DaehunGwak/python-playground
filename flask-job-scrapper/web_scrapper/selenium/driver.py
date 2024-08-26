"""
References:
- https://stackoverflow.com/questions/71201650/how-to-use-selenium-on-repl-it
- https://ask.replit.com/t/cant-get-the-chromedriver-to-work/23343
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")

# service = Service(executable_path="/nix/store/n4qcnqy0isnvxcpcgv6i2z9ql9wsxksw-chromedriver-114.0.5735.90/bin/chromedriver")

# chrome_driver = webdriver.Chrome(options=options, service=service)
chrome_driver = webdriver.Chrome(options=options)
