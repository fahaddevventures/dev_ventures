import undetected_chromedriver as uc

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from  selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class UpworkScraper:
    def __init__(self, headless=True):
        options = uc.ChromeOptions()
        # if headless:
        #     options.add_argument('--headless=new')  # Use new headless mode for Chromium 109+
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--start-maximized')

        self.driver = uc.Chrome(options=options, version_main=138)
        print(self.driver.capabilities['browserVersion'])
        self.wait = WebDriverWait(self.driver, 10)

    def scrape_jobs(self, search_keyword="flask"):
        # url = f"https://www.upwork.com/ab/jobs/search/?q={search_keyword}"
        url = f"https://www.investing.com"
        self.driver.get(url)

        # self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".job-tile-title")))

        # jobs = []
        # job_elements = self.driver.find_elements(By.CSS_SELECTOR, ".job-tile-title a")

        # for job in job_elements[:10]:  # Scrape top 10
        #     title = job.text.strip()
        #     job_url = job.get_attribute("href")
        #     jobs.append({"title": title, "url": job_url})

        # return jobs
        return "Web Scraped"

    def close(self):
        try:
            self.driver.quit()
        except:
            print("Error closing driver: ", e)
