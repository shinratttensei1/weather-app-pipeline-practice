FROM python:3.10.0

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -m unittest discover -s . -p "tests.py"
ENV API_KEY=${API_KEY}


RUN useradd app
USER app

EXPOSE 5000

CMD ["python", "app.py"]


