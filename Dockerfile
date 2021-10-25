   
  
#pull official base image
FROM python:3.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#install cmake
RUN apt-get update && apt-get -y install cmake
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get update && apt-get install -y python3-opencv
RUN mkdir /code

WORKDIR /code
COPY requirement.txt /code/
RUN pip install --upgrade -I setuptools
RUN pip install pymysql
#RUN pip install -r requirement.txt
RUN pip3 install -r requirement.txt

COPY . /code/


EXPOSE 50052


 
CMD ["python", "server.py"]