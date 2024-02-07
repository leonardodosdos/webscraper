from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import pandas as pd

url = "https://legalmatch.ph/jobs"

options = webdriver.ChromeOptions()
options.add_argument('--headless')

rows = []

with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    print("Page URL:", driver.current_url)
    print("Page Title:", driver.title)

    job_rows_xpath = ".//ul[contains(@class, 'avail_post_list_ul')]//div[contains(@class, 'row')]"

    wait.until(EC.presence_of_element_located((By.XPATH, job_rows_xpath)))
    job_rows = driver.find_elements(By.XPATH, job_rows_xpath)

    job_count = len(job_rows)
    for index in range(job_count):
        if index > 0:
            driver.get(url)
            wait.until(EC.presence_of_element_located((By.XPATH, job_rows_xpath)))
            job_rows = driver.find_elements(By.XPATH, job_rows_xpath)

        job_row = job_rows[index]
        job_list_title_cont = job_row.find_element(By.CLASS_NAME, "job_list_title_cont")

        job_label_elem = job_row.find_element(By.XPATH,
                                              ".//div[contains(@class, 'job_list_title_cont')]//label[contains(@class, 'js-job-dropdown-trigger')]")
        job_label = job_label_elem.text
        print(job_label)

        job_description_elem = job_row.find_element(By.XPATH,
                                              ".//div[contains(@class, 'job_list_title_cont')]//div[contains(@class, 'job-description-text')]")
        job_description = re.sub(r'<div class="clearfix"></div>', '', job_description_elem.get_attribute("innerHTML"))
        print(job_description)

        apply_link_elem = job_row.find_element(By.CLASS_NAME, "apply-btn-")
        apply_link = apply_link_elem.get_attribute('href')
        print(apply_link)

        driver.get(apply_link)
        print("Page URL:", driver.current_url)
        print("Page Title:", driver.title)

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-single__content")))

        # Responsibilities
        responsibilities_xpath = "//div[@class='jobs-single__content']//p[contains(., 'responsibilities') or contains(., 'Responsibilities')]"
        responsibilities_p = driver.find_element(By.XPATH, responsibilities_xpath)
        responsibilities_ul = responsibilities_p.find_element(By.XPATH, "following-sibling::ul[1]")
        responsibilities_list = [li.text for li in responsibilities_ul.find_elements(By.TAG_NAME, "li")]


        responsibilities = ""
        print("Responsibilities:")
        for responsibility in responsibilities_list:
            print("-", responsibility)
            responsibilities += f"- {responsibility}\n"

        # Requirements
        requirements_lists = driver.find_elements(By.XPATH,
                                                  "//div[@class='jobs-single__content']//p[strong[text()='Requirements']]/following-sibling::ul[following-sibling::div[contains(@class, 'jobs-single__btn')]]")

        all_requirements = []
        for ul in requirements_lists:
            requirements = [li.text for li in ul.find_elements(By.TAG_NAME, "li")]
            all_requirements.extend(requirements)

        requirements = ""
        print("\nRequirements:")
        for requirement in all_requirements:
            print("-", requirement)
            requirements += f"- {requirement}\n"

        row = {
            "Job Title": job_label,
            "Job Description": job_description,
            "Apply Link": apply_link,
            "Responsibilities": responsibilities,
            "Requirements": requirements
        }
        rows.append(row)

    driver.quit()

df = pd.DataFrame(rows)
df.to_excel('jobs.xlsx', engine='openpyxl', index=False)
