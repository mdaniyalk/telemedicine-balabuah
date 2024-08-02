import os
from tqdm import tqdm

from telemedicine.core.vectorstore import weburl_to_txt
from telemedicine.core.thread import multithreading

with open('urls.txt', 'r') as file:
    urls = file.readlines()

base_path = "scraped_text_files"
os.makedirs(base_path, exist_ok=True)

def process_url(url):
    url = url.strip()  # Remove any leading/trailing whitespace
    if url:  # Check if the line is not empty
        save_path = f"{base_path}/{url.split('//')[-1].replace('/', '_')}.txt"  # Create a filename based on the URL
        weburl_to_txt(url, save_path)
        print(f"Saved {url} to {save_path}")

multithreading(process_url, urls)
