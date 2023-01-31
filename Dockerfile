FROM python:3.9.7

WORKDIR /app

COPY requirements.txt ./
COPY app.py ./
COPY export.pkl ./

RUN pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org pip install --upgrade pip

EXPOSE 8080

ENTRYPOINT [ "app.py" ]
