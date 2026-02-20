import os
import csv
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from googleapiclient.discovery import build
from google.oauth2 import service_account
import torch
from torchvision import models, transforms
from dotenv import load_dotenv


load_dotenv()  # read  .env
print(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

# --- CONFIG ---
SERVICE_ACCOUNT_FILE = "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
CATS_FOLDER = "cats"
DOGS_FOLDER = "dogs"
CREDITS_FILE = "credits.csv"
FOLDER_ID = "1ddKmFBlh8YQ4Ewo37Nl-rd5Bd8g5O-ia"  # sua pasta no Drive

# --- AUTH GOOGLE DRIVE ---
credentials = service_account.Credentials.from_service_account_file(
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
    scopes=SCOPES
)
service = build('drive', 'v3', credentials=credentials)

# --- CREATE FOLDERS ---
os.makedirs(CATS_FOLDER, exist_ok=True)
os.makedirs(DOGS_FOLDER, exist_ok=True)

# --- READ CREDITS ---
credits_dict = {}
with open(CREDITS_FILE, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        img_name, credit = row
        credits_dict[img_name] = credit

# --- FUNCTION TO DOWNLOAD IMAGE FROM DRIVE ---
def download_image(file_id):
    request = service.files().get_media(fileId=file_id)
    fh = BytesIO()
    fh.write(request.execute())
    fh.seek(0)
    return Image.open(fh).convert("RGB")

# --- MODEL FOR CAT DETECTION ---
model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

transform = transforms.Compose([transforms.ToTensor()])

def contains_cat(image):
    img_tensor = transform(image)
    with torch.no_grad():
        predictions = model([img_tensor])[0]
    for label, score in zip(predictions['labels'], predictions['scores']):
        if label == 17 and score > 0.7:  # 17 = 'cat' no COCO
            return True
    return False

# --- LIST ALL IMAGES IN FOLDER ---
results = service.files().list(
    q=f"'{FOLDER_ID}' in parents and mimeType contains 'image/'",
    pageSize=100,
    fields="files(id, name)"
).execute()
files = results.get('files', [])

# --- PROCESS IMAGES ---
for file in files:
    file_id = file['id']
    name = file['name']
    print(f"Processing {name}...")
    
    img = download_image(file_id)
    
    # RESIZING
    img = img.resize((1280, 720))
    
    # ADDING CREDITS
    credit_text = credits_dict.get(os.path.splitext(name)[0], "")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((10, 700), credit_text, fill="white", font=font)
    
    # SORTING INTO FOLDERS
    if contains_cat(img):
        img.save(os.path.join(CATS_FOLDER, name))
    else:
        img.save(os.path.join(DOGS_FOLDER, name))