FROM python:3.10-slim

WORKDIR /app

COPY ../page_objects_model_selenium/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p reports/screenshots reports/allure-results reports/videos

ENV PYTHONUNBUFFERED=1

CMD ["pytest", "tests/basic_test.py", "--browser-type", "chrome", "-v"]