import os
import shutil
from tqdm import tqdm


source_dir = './data/'
destination_dir = './TrainData/'


if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)


def matches_pattern(dir_name):
    try:
        parts = dir_name.split('. ')
        if len(parts) == 2 and parts[0].isdigit():
            return True
    except:
        pass
    return False


def generate_unique_filename(base_name, file_extension, dest_dir):
    counter = 0
    new_file_name = f"{base_name}{file_extension}"
    
    while os.path.exists(os.path.join(dest_dir, new_file_name)):
        counter += 1
        new_file_name = f"{base_name}({counter}){file_extension}"
    
    return new_file_name


source_file_count = 0
destination_file_count = 0


files_to_process = []


for root, dirs, files in os.walk(source_dir):
    
    if matches_pattern(os.path.basename(root)):
        for file in files:
            files_to_process.append((root, file))


total_files = len(files_to_process)


with tqdm(total=total_files, desc="Processing Files", unit="file") as pbar:
    for root, file in files_to_process:
        
        source_file_count += 1

        folder_name = os.path.basename(root)
        file_extension = os.path.splitext(file)[1]

        base_name = ''.join(folder_name.split()[1:])
        new_file_name = generate_unique_filename(base_name, file_extension, destination_dir)

        original_file_path = os.path.join(root, file)
        destination_file_path = os.path.join(destination_dir, new_file_name)
        shutil.copy2(original_file_path, destination_file_path)
        destination_file_count += 1
        pbar.update(1)

        # Checks if the file was renamed correctly
        if not os.path.exists(destination_file_path):
            print(f"Error: {file} was supposed to be renamed to {new_file_name} but failed.")


print(f"Total files in source: {source_file_count}")
print(f"Total files in destination: {destination_file_count}")


if source_file_count == destination_file_count:
    print("All files were copied and renamed successfully.")
    #remove the ./data/ folder since it's no longer needed 
    shutil.rmtree(source_dir)
else:
    print(f"Discrepancy found! Source file count: {source_file_count}, Destination file count: {destination_file_count}")
