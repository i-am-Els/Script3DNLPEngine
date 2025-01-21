import csv
import re

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import time
from pathlib import Path

BASE_URL = "https://www.scriptslug.com"
SAVE_DIR = "screenplays"
UPPER_PAGE_NUM = 17
os.makedirs(SAVE_DIR, exist_ok=True)
CSV_FILE = f"{SAVE_DIR}/screenplays.csv"

def get_driver():
    """Initialize the Selenium WebDriver for Firefox."""
    service = Service(str(Path("vendors/geckodriver.exe").absolute()))  # Path to geckodriver, if not in PATH
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    driver = webdriver.Firefox(service=service, options=options)
    return driver


def get_all_screenplay_links(driver):
    """Fetch all screenplay links by scrolling to the bottom of the page."""
    url = f"{BASE_URL}/?pg={UPPER_PAGE_NUM}"  # Load the last page (with all content)
    driver.get(url)
    time.sleep(3)  # Wait for the JavaScript to load

    # Find the div grid containing the screenplays using XPath
    screenplay_links = []
    grid_div = driver.find_element(By.XPATH, "/html/body/main/div[2]/div[1]/div/div[3]")

    # Now extract all the anchor tags within the grid
    num_links = len(grid_div.find_elements(By.TAG_NAME, 'a'))
    for i in range(1, num_links + 1):
        # XPath for each screenplay
        link_xpath = f"/html/body/main/div[2]/div[1]/div/div[3]/a[{i}]"
        element = driver.find_element(By.XPATH, link_xpath)
        link = element.get_attribute('href')

        if link and link.startswith(BASE_URL):
            screenplay_links.append(link)

    return list(screenplay_links)  # Remove duplicates

def sanitize_filename(filename):
    """Remove invalid characters from filenames."""
    return re.sub(r'[<>:"/\\|?*\n]', '', filename)

def scrape_screenplay(driver, link, count):
    """Scrape screenplay text and PDF link from a link."""
    driver.get(link)
    time.sleep(3)  # Wait for content to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract screenplay title
    title = soup.find('h1').text.strip()
    sanitized_title = sanitize_filename(title)

    # Find the 'Read the Script' button
    read_button = driver.find_element(By.CSS_SELECTOR, ".js-button-read")
    pdf_link = read_button.get_attribute("href") if read_button else None

    # Download the PDF if the link exists
    if pdf_link:
        download_pdf(pdf_link, f"{count:03d}_{sanitized_title}.pdf")

    # Save to a cache tuple
    return [count, sanitized_title, link, pdf_link]

def download_pdf(pdf_url, filename):
    """Download the PDF file and save it."""
    import requests
    response = requests.get(pdf_url)
    if response.status_code == 200:
        file_path = os.path.join(str(Path(SAVE_DIR).absolute()), filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded PDF: {filename}")
    else:
        print(f"Failed to download PDF: {pdf_url}")


def main():
    driver = get_driver()
    try:
        # Step 1: Get all screenplay links
        links = get_all_screenplay_links(driver)
        if not links:
            print("No screenplays found.")
            return

        print(f"Found {len(links)} screenplays. Scraping up to 510...")

        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Serial Number", "Title", "Page Link", "PDF Link"])
            # Step 2: Limit to 510 screenplays
            for count, link in enumerate(links[:510], start=1):
                csv_cache = scrape_screenplay(driver, link, count)
                writer.writerow(csv_cache)
                print(f"Saved CSV file: {CSV_FILE}")


    finally:
        driver.quit()


if __name__ == "__main__":
    main()
