import requests
from bs4 import BeautifulSoup
import os
import time
import sys


# Set the website URL
url = ''

#get link based on the python script argument
if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    print("Please provide the URL as an argument")
    sys.exit()

# Send a GET request to the website URL
response = requests.get(url)

# Parse the HTML content of the website using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all image tags and extract the URLs
img_tags = soup.find_all('img')
img_urls = [img['src'] for img in img_tags]

#append images to img_urls based on divs with a background-image style with a url in it
for div in soup.find_all('div', style=lambda value: value and 'background-image' in value):
    img_urls.append(div['style'].split('url(')[1].split(')')[0])


# Find all video tags and extract the URLs
video_tags = soup.find_all('video')
video_urls = [video['src'] for video in video_tags]

# Create a results folder to store the downloaded files
if not os.path.exists('results'):
    os.makedirs('results')

# Download the images
for i, img_url in enumerate(img_urls):
    response = requests.get(img_url)
    if response.status_code == 200:
        with open(f'results/image{i}.jpg', 'wb') as f:
            f.write(response.content)
            print(f'Downloaded {img_url}')
            time.sleep(0.2)  # add a 200ms delay
    else:
        print(f'Failed to download {img_url}')

# Download the videos
for i, video_url in enumerate(video_urls):
    response = requests.get(video_url)
    if response.status_code == 200:
        with open(f'results/video{i}.mp4', 'wb') as f:
            f.write(response.content)
            print(f'Downloaded {video_url}')
            time.sleep(0.2)  # add a 200ms delay
    else:
        print(f'Failed to download {video_url}')
