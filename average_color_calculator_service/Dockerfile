FROM python:3.12

WORKDIR /average_color_calculator_service

COPY src ./src
COPY tests ./tests
COPY requirements.txt ./
COPY pytest.ini ./

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pytest

CMD ["python", "-u", "./src/main.py"]
