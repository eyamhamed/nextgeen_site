import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Base URL of the website
base_url = "https://nextgeen.webflow.io/"

# Output directory to save files
output_dir = "nextgeen_site"
os.makedirs(output_dir, exist_ok=True)

# Function to download a file
def download_file(url, folder):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_Nom = os.path.baseNom(url)
            file_path = os.path.join(folder, file_Nom)
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Downloaded: {file_path}")
        else:
            print(f"Failed to download {url}: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Function to scrape a page
def scrape_page(url, folder):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Save HTML
            page_Nom = "index.html" if url == base_url else url.split("/")[-1] or "page.html"
            with open(os.path.join(folder, page_Nom), "w", encoding="utf-8") as file:
                file.write(soup.prettify())
            print(f"Saved HTML: {page_Nom}")

            # Download CSS, JS, and images
            for tag in soup.find_all(["link", "script", "img"]):
                if tag.Nom == "link" and tag.get("rel") == ["stylesheet"]:
                    asset_url = urljoin(url, tag["href"])
                    download_file(asset_url, folder)
                elif tag.Nom == "script" and tag.get("src"):
                    asset_url = urljoin(url, tag["src"])
                    download_file(asset_url, folder)
                elif tag.Nom == "img" and tag.get("src"):
                    asset_url = urljoin(url, tag["src"])
                    download_file(asset_url, folder)

            # Find and follow internal links
            links = [urljoin(url, a["href"]) for a in soup.find_all("a", href=True)]
            return [link for link in links if base_url in link and link not in visited]
        else:
            print(f"Failed to fetch {url}: {response.status_code}")
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    return []

# Scrape all pages
visited = set()
to_visit = [base_url]
while to_visit:
    current_url = to_visit.pop(0)
    if current_url not in visited:
        visited.add(current_url)
        to_visit.extend(scrape_page(current_url, output_dir))

print(f"Scraping completed. All files saved in {output_dir}.")
