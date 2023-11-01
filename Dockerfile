FROM python:3.11.6
ADD . /mygo
WORKDIR /mygo
RUN pip install -r requirements.txt
CMD ["python","./app.py"]
