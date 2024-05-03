FROM python:3.10-bookworm
WORKDIR /mygo
COPY . .
RUN mkdir video/ && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
CMD ["python3", "app.py"]
