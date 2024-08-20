import dotenv, os, json, requests, time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

dotenv.load_dotenv()

PDF_URL_ADDON = "/pdf-list/"

df = pd.read_csv('links.csv')
df = df[df['page_type'] == 'topic-questions']
df.reset_index(drop=True, inplace=True)
# See how many unique first 6 columns there are
df.drop_duplicates(subset=['root', 'level', 'subject', 'board', 'year', 'page_type'], inplace=True)
# Delete the rest of the columns
df.drop(columns=['the_rest'], inplace=True)
df.reset_index(drop=True, inplace=True)
print(df)

converted_urls = []

for i in range(len(df)):
    url = df.iloc[i]
    url = url.tolist()
    url[4] = str(url[4])
    converted_url = "http://" + '/'.join(url) + PDF_URL_ADDON
    converted_urls.append(converted_url)

print(converted_urls)

output_dir = "output_files"
os.makedirs(output_dir, exist_ok=True)

# Configure options for the Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode for no UI

# Path to the ChromeDriver executable
service = Service('/opt/homebrew/bin/chromedriver')  # Update this path

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the URL
driver.get("https://www.savemyexams.com/login/")

# Wait for the span element and click it
email_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Continue with email')]")
email_button.click()

print(os.getenv('SME_USERNAME'))
print(os.getenv('SME_PASSWORD'))

# Input email address
email_input = driver.find_element(By.ID, "email-page")
email_input.send_keys(os.getenv('SME_USERNAME'))

# Input password
password_input = driver.find_element(By.ID, "password-page")
password_input.send_keys(os.getenv('SME_PASSWORD'))

time.sleep(5)

# Submit the form
submit_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.btn-lg.Button_wide__RhWz6")
submit_button.click()

# Optional: print success message or perform further actions
print("Login attempt complete.")

time.sleep(5)

def download_pdfs(url: str):
    driver.get(url)

    script_element = driver.find_element(By.ID, "__NEXT_DATA__")

    # Get the JSON content from the script tag
    json_data = script_element.get_attribute("innerHTML")

    print(json_data)

    # Convert the JSON string to a Python dictionary
    data = json.loads(json_data)
    print(json.dumps(data, indent=4))  # Pretty print the JSON data

    pdf_files = data['props']['pageProps']['pdfLinks']
    meta_data = data['props']['pageProps']['breadcrumbs']['titles']


    print(f"PDF files: {pdf_files}")
    print(f"Meta data: {meta_data}")

    ROOT_DIR = "output_files"
    OUTPUT_DIRS = os.path.join(ROOT_DIR, meta_data['level'], meta_data['subject'] + " " + meta_data['year'])

    os.makedirs(ROOT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIRS, exist_ok=True)

    for i, pdf_file in enumerate(pdf_files):
        topics = pdf_file['topics']
        sections = pdf_file['section']
        
        for topic in topics:
            print(topic['topicName'])
            os.makedirs(os.path.join(OUTPUT_DIRS, pdf_file['section'], topic['topicName']), exist_ok=True)

            for area in topic['areas']:
                os.makedirs(os.path.join(OUTPUT_DIRS, pdf_file['section'], topic['topicName'], area['areaName']), exist_ok=True)

                for question in area['areaContent']:
                    initial_question_url = question['pdfUrl']
                    question_filename = os.path.join(OUTPUT_DIRS, pdf_file['section'], topic['topicName'], area['areaName'], question['title'] + ".pdf")

                    print(f"Downloading: {question_filename}, from {initial_question_url}")
                    # Download the PDF from the final URL
                    response = requests.get(initial_question_url)
                    final_url = response.url

                    if final_url.endswith(".pdf"):
                        # Download the PDF from the final URL
                        with open(question_filename, 'wb') as f:
                            f.write(response.content)
                        print(f"Downloaded: {question_filename}")

for url in converted_urls:
    download_pdfs(url)
    time.sleep(5)
    
driver.quit()



