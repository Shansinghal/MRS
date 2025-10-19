import os
import gdown

file_id = "1FaY6ewiASl5wPFc4IU5HfwrwYz37WOZ3"
url = f"https://drive.google.com/uc?id={file_id}"
output = "similiarity.pkl"

if not os.path.exists(output):
    print("Downloading similiarity.pkl from Google Drive...")
    gdown.download(url, output, quiet=False)
else:
    print("similiarity.pkl already exists.")
