import os
import requests
import zipfile
from io import BytesIO

def download_and_extract_fonts():
    # Create assets directory if it doesn't exist
    if not os.path.exists('assets'):
        os.makedirs('assets')

    # URL for DejaVu fonts
    url = "https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.zip"
    
    print("Downloading DejaVu fonts...")
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Extracting fonts...")
        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            # Extract only the needed fonts
            for file_info in zip_ref.filelist:
                if file_info.filename.endswith(('.ttf',)) and 'DejaVuSansCondensed' in file_info.filename:
                    # Extract the file to the assets directory
                    font_name = os.path.basename(file_info.filename)
                    with zip_ref.open(file_info) as font_file, open(f'assets/{font_name}', 'wb') as output_file:
                        output_file.write(font_file.read())
                    print(f"Extracted: {font_name}")
        print("Fonts downloaded and extracted successfully!")
    else:
        print("Failed to download fonts!")

if __name__ == "__main__":
    download_and_extract_fonts() 