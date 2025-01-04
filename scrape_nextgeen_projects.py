import requests

# URL of the page to scrape
url = "https://nextgeen.webflow.io/project"

# Send a GET request to the URL
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Save the raw HTML content to a file
    with open("nextgeen_project.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    print("HTML content saved to nextgeen_project.html")
else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")
