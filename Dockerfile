FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pipi install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]