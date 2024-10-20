
FROM python:3.9-slim


WORKDIR /app


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .

ENV GOOGLE_APPLICATION_CREDENTIALS="/app/credentials.json"  # Adjust path as necessary


EXPOSE 8080


CMD ["python", "main.py"]  # Replace with your actual entry point script name
