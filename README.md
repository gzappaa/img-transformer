# Image Transformer: Cat/Dog Sorter

This project downloads images from a Google Drive folder, resizes them, adds credits, and sorts them into `cats` or `dogs` folders using a pre-trained PyTorch model.  

---

## Features

- Downloads images directly from Google Drive using a Service Account
- Resizes images to `1280x720`
- Adds credits from a `credits.csv` file
- Detects cats using Faster R-CNN (PyTorch)
- Sorts images into `cats/` and `dogs/` folders
- Fully Dockerized for portability

---

## Setup

1. Clone this repository:

```bash
git clone <your-repo-url>
cd img-transformer
```

2. Download your Google Cloud Service Account JSON and place it in the project folder as credentials.json.

3. Edit .env if needed (default path inside container: /credentials.json):

## Docker Usage

Build the Docker image:

```docker build -t img-transformer .```

Run the Docker image:

```docker run -it `
  -v "${PWD}/cats:/app/cats" `
  -v "${PWD}/dogs:/app/dogs" `
  -v "${PWD}/.env:/app/.env" `
  -v "${PWD}/credentials.json:/app/credentials.json" `
  --env-file "${PWD}/.env" `
  img-transformer
  ```

Requirements

Python 3.13+

Docker

Dependencies are in requirements.txt (Torch, torchvision, Pillow, Google API client, python-dotenv)