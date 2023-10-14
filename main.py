import requests
from bs4 import BeautifulSoup
import os

# Define the base URL
base_url = 'https://www.fencingdatabase.com/'

# Create a directory to save the downloaded videos (if it doesn't exist)
if not os.path.exists("downloaded_videos"):
    os.makedirs("downloaded_videos")

# Initialize variables
downloaded_count = 0
max_downloads = 1000

while downloaded_count < max_downloads:
    # Create the URL for the current page
    url = f'{base_url}?firstname=&lastname=&weapon=epee&gender=all&tournament=all&year=all&opposing-score=0&opposing-lastname=&submit-search=Search+Clips'

    # Send an HTTP GET request to the website and parse the HTML
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        break

    # Find all <source> elements in the HTML
    vidsource = soup.find_all("source")

    # Download and save MP4 videos from the current page
    for index, item in enumerate(vidsource, start=1):
        src = item.get("src")
        if src and src.endswith(".mp4"):
            mp4_url = src
            local_filename = f"downloaded_videos/video_{downloaded_count + index}.mp4"

            response = requests.get(mp4_url, stream=True)

            if response.status_code == 200:
                with open(local_filename, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)
                print(f"Downloaded video {downloaded_count + index} to {local_filename}")
                downloaded_count += 1

                if downloaded_count >= max_downloads:
                    break  # Stop downloading if the desired count is reached
            else:
                print(f"Failed to download video {downloaded_count + index}. Status code: {response.status_code}")

            response.close()


    # Get the URL of the next page
    next_page_url = base_url + "%20Clips&page=2"

    # Update the URL to the next page and continue the loop
    url = next_page_url

print(f"Total {downloaded_count} videos downloaded.")
