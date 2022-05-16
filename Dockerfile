FROM python-36-centos:latest
USER root
RUN pip3 install -i -r requirements.txt
ADD . /code
WORKDIR /code
CMD ["python3", "app.py"]

