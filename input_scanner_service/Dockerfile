FROM python:3.12

WORKDIR /image_publisher_service

COPY src ./src
COPY tests ./tests
COPY requirements.txt ./
COPY pytest.ini ./

RUN pip install --no-cache-dir -r requirements.txt
RUN pytest -vv

CMD ["python", "./src/main.py"]

