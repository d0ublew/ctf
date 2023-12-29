From python:3.9.16

ADD challenges /app
ADD flag.txt /flag.txt
ADD store.xml /app/store.xml
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python","app.py"]
