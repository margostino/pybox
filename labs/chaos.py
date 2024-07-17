import os
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Define the URL to visit
url = "some"

ldap_username = os.environ.get("LDAP_USERNAME")
ldap_password = os.environ.get("LDAP_PASSWORD")

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# Create a new instance of the Chrome driver
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)


def wait_for_element(driver, by, value, retries=5, delay=2):
    """Wait for an element to be present and clickable, retrying if necessary."""
    for _ in range(retries):
        try:
            element = WebDriverWait(driver, delay).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(delay)
    return None


# try:
# Visit the URL
driver.get(url)

# Step 1: Click the SSO button
sso_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(), 'Single Sign On')]")
    )
)
sso_button.click()

# Step 2: Enter the username
username_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "input28"))
)
username_field.send_keys(ldap_username)

# Step 3: Click the Next button
next_button = driver.find_element(By.XPATH, "//input[@value='Next']")
next_button.click()

# Step 4: Enter the password
password_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "input60"))
)
password_field.send_keys(ldap_password)

# Step 5: Click the Verify button
verify_button = driver.find_element(By.XPATH, "//input[@value='Verify']")
verify_button.click()

# Step 6: Wait for human action to verify with Okta
# input("Please complete the Okta verification and press Enter to continue...")

# Step 7: Click the Share button
# share_button = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable(
#         (
#             By.XPATH,
#             "//button[@data-test-subj='shareTopNavButton']/span[@class='euiButtonContent euiButtonEmpty__content']/span[@class='euiButtonEmpty__text' and contains(text(), 'Share')]",
#         )
#     )
# )
# share_button.click()
# print("Waiting for the Share button...")
# share_button = WebDriverWait(driver, 20).until(
#     EC.element_to_be_clickable(
#         (By.XPATH, "//button[@data-test-subj='shareTopNavButton']")
#     )
# )
# print("Share button found, clicking...")
# share_button.click()

# share_button = wait_for_element(
#     driver,
#     By.XPATH,
#     "//button[@data-test-subj='shareTopNavButton']/span[@class='euiButtonContent euiButtonEmpty__content']/span[@class='euiButtonEmpty__text' and contains(text(), 'Share')]",
#     retries=10,
#     delay=3,
# )
# if share_button:
#     share_button.click()
# else:
#     print("Share button not found. Exiting.")
#     driver.quit()
#     exit()

# # Step 8: Click the Export CSV option
# export_csv_button = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Export CSV')]"))
# )
# export_csv_button.click()

time.sleep(30)  # Adjust the time as needed


driver.save_screenshot("screenshot.png")

# Get the HTML source
html_source = driver.page_source

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_source, "html.parser")

# Find the desired element
table = soup.select_one('table[data-test-subj="docTable"]')

# Check if the element exists
if table:
    print(table.prettify())
else:
    print("Table not found")


table = driver.find_element(By.CSS_SELECTOR, 'table[data-test-subj="docTable"]')

# Extract column headers
headers = []
header_elements = table.find_elements(
    By.CSS_SELECTOR, 'thead th[data-test-subj^="docTableHeaderField"] span'
)
for header in header_elements:
    headers.append(
        header.get_attribute("data-test-subj").replace("docTableHeader-", "")
    )

# Extract table rows
rows = []
row_elements = table.find_elements(
    By.CSS_SELECTOR, 'tbody tr[data-test-subj="docTableRow"]'
)

for row_element in row_elements:
    row_data = []
    cell_elements = row_element.find_elements(
        By.CSS_SELECTOR, 'td[data-test-subj="docTableField"] span'
    )
    for cell in cell_elements:
        row_data.append(cell.text)
    rows.append(row_data)

# Create a DataFrame
df = pd.DataFrame(rows, columns=headers)

# Close the driver
driver.quit()


# full_html = driver.page_source
# print(full_html)

# # Step 8: Wait for the table with results to appear
# table = wait.until(
#     EC.presence_of_element_located(
#         (By.XPATH, "//table[@data-test-subj='docTable']")
#     )
# )

# # Step 9: Read and parse the table
# rows = table.find_elements(By.TAG_NAME, "tr")

# # Extract and print the data
# for row in rows:
#     columns = row.find_elements(By.TAG_NAME, "td")
#     data = [col.text for col in columns]
#     print(data)

# Wait for the download to complete
time.sleep(10)  # Adjust as necessary based on the file size and download speed

# finally:
#     # Close the driver
#     # driver.quit()
