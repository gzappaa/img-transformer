# --- Use a slim Python 3.13 image ---
FROM python:3.13-slim

# --- Set the working directory inside the container ---
WORKDIR /app

# --- Copy requirements and install Python dependencies ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Copy the rest of the project files ---
COPY . .

# --- Create persistent folders for output images ---
RUN mkdir -p /app/cats /app/dogs

# --- Ensure Python output is unbuffered (prints appear immediately) ---
ENV PYTHONUNBUFFERED=1

# --- Default command to run your script ---
CMD ["python", "script.py"]