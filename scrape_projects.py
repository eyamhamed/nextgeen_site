import requests

# URL of the page to scrape
url = "https://nextgeen.webflow.io/project"

# User-Agent to mimic a browser request
headers = {"User-Agent": "Mozilla/5.0"}

try:
    # Send a GET request to fetch the HTML content
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # File Nom to save the HTML content
        output_file = "project_page.html"
        
        # Save the HTML content to a file
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(response.text)
        
        print(f"HTML content of the page has been saved to '{output_file}'")
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
except Exception as e:
    print(f"An error occurred: {e}")
