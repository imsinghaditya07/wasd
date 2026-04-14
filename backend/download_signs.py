import urllib.request
import os
import time
from PIL import Image, ImageDraw, ImageFont

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def create_placeholder(word, filepath):
    # Create a nice placeholder image using Pillow
    img = Image.new('RGB', (300, 300), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    # Just draw the text in the middle
    text = f"Sign: {word.upper()}"
    d.text((50, 140), text, fill=(255, 255, 0))
    # Save as gif
    img.save(filepath, format="GIF")

def download_signs():
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from config import SIGNS_DIR
    ensure_dir(SIGNS_DIR)
    
    # Basic greetings and common words
    words = {
        "hello": "https://www.lifeprint.com/asl101/gifs/h/hello.gif",
        "help": "https://www.lifeprint.com/asl101/gifs/h/help.gif",
        "thank_you": "https://www.lifeprint.com/asl101/gifs/t/thankyou.gif",
        "please": "https://www.lifeprint.com/asl101/gifs/p/please.gif",
        "yes": "https://www.lifeprint.com/asl101/gifs/y/yes.gif",
        "no": "https://www.lifeprint.com/asl101/gifs/n/no.gif",
        "water": "https://www.lifeprint.com/asl101/gifs/w/water.gif",
        "food": "https://www.lifeprint.com/asl101/gifs/f/food.gif",
        "stop": "https://www.lifeprint.com/asl101/gifs/s/stop.gif",
        "good": "https://www.lifeprint.com/asl101/gifs/g/good.gif",
        "sorry": "https://www.lifeprint.com/asl101/gifs/s/sorry.gif",
        "goodbye": "https://www.lifeprint.com/asl101/gifs/g/goodbye-asl.gif"
    }
    
    # Add A-Z alphabet
    for char in range(ord('a'), ord('z') + 1):
        letter = chr(char)
        words[letter] = f"https://www.lifeprint.com/asl101/gifs/{letter}/{letter}.gif"
    
    print("Downloading ASL sign GIFs (with Pillow placeholders on failure)...")
    
    for word, url in words.items():
        filename = f"{word}.gif"
        filepath = os.path.join(SIGNS_DIR, filename)
        
        try:
            print(f"Fetching {word}.gif...")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
                out_file.write(response.read())
            time.sleep(0.5)
        except Exception as e:
            print(f"Failed to download {word} from {url} ({e}). Generating placeholder.")
            create_placeholder(word, filepath)
            
    print("Download complete.")

if __name__ == "__main__":
    download_signs()
