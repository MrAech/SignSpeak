import os
import subprocess
import requests
from urllib.parse import urlparse
from tqdm import tqdm
import zipfile

#This seemed to be a better way of doing it then downloading a large zip file and also seemed faster
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


if not os.path.exists('./data'):
    os.makedirs('./data')


for url, filename in urls.items():
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        t = tqdm(total=total_size, unit='B', unit_scale=True, desc=filename)
        with open(f'./data/{filename}', 'wb') as f:
            for chunk in response.iter_content(block_size):
                f.write(chunk)
                t.update(len(chunk))
        t.close()
        print(f'Downloaded {filename} successfully!')

        
        zip_ref = zipfile.ZipFile(f'./data/{filename}', 'r')
        zip_ref.extractall('./data')
        zip_ref.close()
        print(f'Unzipped {filename} successfully!')

        
        os.remove(f'./data/{filename}')
        print(f'Deleted {filename} successfully!')
    else:
        print(f'Failed to download {filename}. Status code: {response.status_code}')

ch = input("Please run fldrRename.py file now By doing: run to run or exit to exit: ")
choice = ch.lower()
if choice == "run":
    subprocess.run(["python", "fldrRename.py"], check=True)
elif choice == "exit":
    # i know i know... but i just found out about this so DO NOT CHANGE
    from rich import print
    print(f"[bold red]Be sure to Run [bold yellow]fldrRename.py[/bold yellow] before training the model[/bold red]")
