import os
import re
import subprocess

# Folder where videos are stored and The Corresponding JSON_file
videos_dir = 'Model_stuff/data'  
json_output_file = 'Model_stuff/video_labels.json'

# Convert .mov to .mp4 using ffmpeg
def convert_mov_to_mp4(mov_file, mp4_file):
    try:
        subprocess.run(['ffmpeg', '-i', mov_file, mp4_file], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Function to handle conversion and deletion
def process_videos():
    # Regex pattern to match .mov files other wise it tends to SKIP some files
    mov_pattern = re.compile(r'.+\.mov$', re.IGNORECASE)


    files = [f for f in os.listdir(videos_dir) if mov_pattern.match(f)]


    if not files:
        print("No .mov files found.")
        return

    # Processes the first file and ask for confirmation
    first_file = files[0]
    mov_file_path = os.path.join(videos_dir, first_file)
    mp4_file_path = os.path.join(videos_dir, re.sub(r'\.mov$', '.mp4', first_file, flags=re.IGNORECASE))

    print(f"Converting {first_file} to mp4...")
    if convert_mov_to_mp4(mov_file_path, mp4_file_path):
        print(f"Conversion of {first_file} successful.")
        # Asking user for confirmation
        confirm = input("Was the first video properly converted? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Aborting process.")
            return
    else:
        print(f"Conversion of {first_file} failed.")
        return

    # Delete the original .mov file
    os.remove(mov_file_path)
    
    # Continue with the rest of the .mov files
    for file in files[1:]:
        mov_file_path = os.path.join(videos_dir, file)
        mp4_file_path = os.path.join(videos_dir, re.sub(r'\.mov$', '.mp4', file, flags=re.IGNORECASE))

        print(f"Converting {file} to mp4...")
        if convert_mov_to_mp4(mov_file_path, mp4_file_path):
            print(f"Conversion of {file} successful.")
            # Delete the original .mov file
            os.remove(mov_file_path)
        else:
            print(f"Conversion of {file} failed.")
            continue

    print("All .mov files have been processed.")






def rename_videos_and_store_labels(videos_dir, json_output_file):
    video_labels = {}

    for subdir, _, files in os.walk(videos_dir):
        for file in files:
            
            if file.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.flv')):
                
                original_file_path = os.path.join(subdir, file)

              
                new_file_name = re.sub(r'^\d+\.\s*', '', file).strip()  # Removes "{num}. " from the start

                if new_file_name != file:
                    new_file_path = os.path.join(subdir, new_file_name)

                    if not os.path.exists(new_file_path):
                        os.rename(original_file_path, new_file_path)
                        print(f"Renamed: {file} -> {new_file_name}")
                    else:
                        print(f"File {new_file_name} already exists, skipping renaming.")
                else:
                    new_file_path = original_file_path  # No renaming occurred


                label = re.sub(r'^\d+\.\s*', '', os.path.splitext(file)[0]).strip()


                video_labels[new_file_path] = label

    # Save the dictionary to a JSON file
    with open(json_output_file, 'w') as json_file:
        json.dump(video_labels, json_file, indent=4)

    print(f"Video labels and paths have been saved to {json_output_file}")


process_videos()
rename_videos_and_store_labels(videos_dir, json_output_file)
