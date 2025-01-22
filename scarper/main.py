import csv
import os

from scarper.algo import get_last_serial_number, get_driver, get_all_screenplay_links, scrape_screenplay
from scarper.consts import SAVE_DIR, CSV_FILE
from scarper.download import download_pdf

os.makedirs(SAVE_DIR, exist_ok=True)

def main():
    # Get the last serial number from the CSV file
    last_serial = get_last_serial_number(CSV_FILE)
    print(f"Last serial number: {last_serial}")
    driver = get_driver()
    try:
        # Step 1: Get all screenplay links
        links = get_all_screenplay_links(driver)
        if not links:
            print("No screenplays found.")
            return

        print(f"Found {len(links)} screenplays. Scraping up to 510...")

        with open(CSV_FILE, 'a', encoding="utf-8", newline='') as f:

            writer = csv.writer(f)
            if last_serial == 0:
                writer.writerow(["Serial Number", "Title", "Page Link", "PDF Link", "Download Status"])
            # Step 2: Limit to 510 screenplays
            for count, link in enumerate(links[last_serial:], start=last_serial+1):
                csv_cache = scrape_screenplay(driver, link, count)
                # Download the PDF if the link exists
                if csv_cache[3]:
                    download_pdf(csv_cache[3], f"{count:03d}_{csv_cache[1]}.pdf")
                writer.writerow(csv_cache)
                print(f"Saved {csv_cache[0]} CSV file: {csv_cache[1]}")


    finally:
        driver.quit()


if __name__ == "__main__":
    main()
