# Gunakan base image python 3.11 slim
FROM python:3.11-slim

# Set lingkungan kerja di dalam container
WORKDIR /app

# Salin file requirements.txt ke container
COPY requirements.txt .

# Instal dependensi yang diperlukan
RUN apt-get update && apt-get install -y ffmpeg

# Install requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh isi direktori proyek ke dalam container
COPY . .

# Tentukan port yang akan digunakan oleh aplikasi Streamlit
EXPOSE 8501

# Tentukan perintah yang akan dijalankan saat container dimulai
CMD ["streamlit", "run", "streamlit_app.py"]