import os
import requests
import zipfile
import shutil
from tqdm import tqdm
from pathlib import Path

# Folder to save downloaded videos
output_dir = 'Model_stuff/data'
os.makedirs(output_dir, exist_ok=True)

# File to keep track of downloaded ZIP files
downloaded_zips_file = 'downloaded_zips.txt'

# Dictionary of URLs

urls = {
    'https://zenodo.org/records/4010759/files/Adjectives_1of8.zip?download=1': 'Adjectives_1of8.zip',
    'https://zenodo.org/records/4010759/files/Adjectives_2of8.zip?download=1': 'Adjectives_2of8.zip',
    'https://zenodo.org/records/4010759/files/Adjectives_3of8.zip?download=1': 'Adjectives_3of8.zip',
    'https://zenodo.org/records/4010759/files/Adjectives_4of8.zip?download=1': 'Adjectives_4of8.zip',
    'https://zenodo.org/records/4010759/files/Adjectives_5of8.zip?download=1': 'Adjectives_5of8.zip',
    'https://zenodo.org/records/4010759/files/Adjectives_6of8.zip?download=1': 'Adjectives_6of8.zip',
    'https://zenodo.org/records/4010759/files/Adjectives_7of8.zip?download=1': 'Adjectives_7of8.zip',
    'https://zenodo.org/records/4010759/files/Adjectives_8of8.zip?download=1': 'Adjectives_8of8.zip',

    'https://zenodo.org/records/4010759/files/Animals_1of2.zip?download=1': 'Animals_1of2.zip',
    'https://zenodo.org/records/4010759/files/Animals_2of2.zip?download=1': 'Animals_2of2.zip',

    'https://zenodo.org/records/4010759/files/Clothes_1of2.zip?download=1': 'Clothes_1of2.zip',
    'https://zenodo.org/records/4010759/files/Clothes_2of2.zip?download=1': 'Clothes_2of2.zip',

    'https://zenodo.org/records/4010759/files/Colours_1of2.zip?download=1': 'Colours_1of2.zip',
    'https://zenodo.org/records/4010759/files/Colours_2of2.zip?download=1': 'Colours_2of2.zip',

    'https://zenodo.org/records/4010759/files/Days_and_Time_1of3.zip?download=1': 'Days_and_Time_1of3.zip',
    'https://zenodo.org/records/4010759/files/Days_and_Time_2of3.zip?download=1': 'Days_and_Time_2of3.zip',
    'https://zenodo.org/records/4010759/files/Days_and_Time_3of3.zip?download=1': 'Days_and_Time_3of3.zip',

    'https://zenodo.org/records/4010759/files/Electronics_1of2.zip?download=1': 'Electronics_1of2.zip',
    'https://zenodo.org/records/4010759/files/Electronics_2of2.zip?download=1': 'Electronics_2of2.zip',

    'https://zenodo.org/records/4010759/files/Greetings_1of2.zip?download=1': 'Greetings_1of2.zip',
    'https://zenodo.org/records/4010759/files/Greetings_2of2.zip?download=1': 'Greetings_2of2.zip',

    'https://zenodo.org/records/4010759/files/Home_1of4.zip?download=1': 'Home_1of4.zip',
    'https://zenodo.org/records/4010759/files/Home_2of4.zip?download=1': 'Home_2of4.zip',
    'https://zenodo.org/records/4010759/files/Home_3of4.zip?download=1': 'Home_3of4.zip',
    'https://zenodo.org/records/4010759/files/Home_4of4.zip?download=1': 'Home_4of4.zip',

    'https://zenodo.org/records/4010759/files/Jobs_1of2.zip?download=1': 'Jobs_1of2.zip',
    'https://zenodo.org/records/4010759/files/Jobs_2of2.zip?download=1': 'Jobs_2of2.zip',

    'https://zenodo.org/records/4010759/files/Means_of_Transportation_1of2.zip?download=1': 'Means_of_Transportation_1of2.zip',
    'https://zenodo.org/records/4010759/files/Means_of_Transportation_2of2.zip?download=1': 'Means_of_Transportation_2of2.zip',

    'https://zenodo.org/records/4010759/files/People_1of5.zip?download=1': 'People_1of5.zip',
    'https://zenodo.org/records/4010759/files/People_2of5.zip?download=1': 'People_2of5.zip',
    'https://zenodo.org/records/4010759/files/People_3of5.zip?download=1': 'People_3of5.zip',
    'https://zenodo.org/records/4010759/files/People_4of5.zip?download=1': 'People_4of5.zip',
    'https://zenodo.org/records/4010759/files/People_5of5.zip?download=1': 'People_5of5.zip',

    'https://zenodo.org/records/4010759/files/Places_1of4.zip?download=1': 'Places_1of4.zip',
    'https://zenodo.org/records/4010759/files/Places_2of4.zip?download=1': 'Places_2of4.zip',
    'https://zenodo.org/records/4010759/files/Places_3of4.zip?download=1': 'Places_3of4.zip',
    'https://zenodo.org/records/4010759/files/Places_4of4.zip?download=1': 'Places_4of4.zip',

    'https://zenodo.org/records/4010759/files/Pronouns_1of2.zip?download=1': 'Pronouns_1of2.zip',
    'https://zenodo.org/records/4010759/files/Pronouns_2of2.zip?download=1': 'Pronouns_2of2.zip',

    'https://zenodo.org/records/4010759/files/Seasons_1of1.zip?download=11': 'Seasons_1of1.zip',

    'https://zenodo.org/records/4010759/files/Society_1of3.zip?download=1': 'Society_1of3.zip',
    'https://zenodo.org/records/4010759/files/Society_2of3.zip?download=1': 'Society_2of3.zip',
    'https://zenodo.org/records/4010759/files/Society_3of3.zip?download=1': 'Society_3of3.zip',
}

def download_zip(url, zip_filename):
    """Downloads the zip file from the given URL with tqdm progress bar."""
    print(f"Downloading {zip_filename}...")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024

    with open(zip_filename, 'wb') as f:
        for data in tqdm(response.iter_content(block_size), total=total_size // block_size, unit='KB', desc=zip_filename):
            f.write(data)

def extract_zip(zip_filename, extract_to):
    """Extracts the downloaded zip file."""
    print(f"Extracting {zip_filename}...")
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"{zip_filename} extracted.")

def find_video_and_save(subfolder_path, dest_folder):
    """Finds the first video file in the subfolder and saves it with the subfolder name."""
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.flv']
    subfolder_name = os.path.basename(subfolder_path)

    # Search for the first video file, #################
    # THIS IS NEW, SINCE TOO MUCH DATA TO PROCESS
    for root, _, files in os.walk(subfolder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in video_extensions):
                video_path = os.path.join(root, file)
                dest_path = os.path.join(dest_folder, f"{subfolder_name}{Path(file).suffix}")
                shutil.copy(video_path, dest_path)
                print(f"Saved {dest_path}")
                return  # Only save the first video
    print(f"No video found in {subfolder_path}")

def has_already_downloaded(zip_filename):
    """Checks if the ZIP file has already been downloaded by reading the tracking file."""
    if os.path.exists(downloaded_zips_file):
        with open(downloaded_zips_file, 'r') as f:
            downloaded_zips = f.read().splitlines()
        return zip_filename in downloaded_zips
    return False

def mark_as_downloaded(zip_filename):
    """Marks the ZIP file as downloaded by writing to the tracking file."""
    with open(downloaded_zips_file, 'a') as f:
        f.write(f"{zip_filename}\n")

def process_links(urls):
    temp_extract_dir = 'temp_extract'
    os.makedirs(temp_extract_dir, exist_ok=True)

    for url, zip_filename in urls.items():
        if has_already_downloaded(zip_filename):
            print(f"Skipping {zip_filename}, already downloaded.")
            continue


        download_zip(url, zip_filename)


        extract_zip(zip_filename, temp_extract_dir)

        for root, dirs, _ in os.walk(temp_extract_dir):
            for subfolder in dirs:
                subfolder_path = os.path.join(root, subfolder)
                find_video_and_save(subfolder_path, output_dir)


        mark_as_downloaded(zip_filename)

        # Clean up zip file and extracted content
        os.remove(zip_filename) 
        shutil.rmtree(temp_extract_dir)
        print(f"Cleaned up {zip_filename} and temporary extraction folder.")


process_links(urls)
