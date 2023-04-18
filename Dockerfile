FROM python:3.7
WORKDIR /opt/apps/fastapibase/
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY src ./src
COPY conf ./conf
CMD ["python", "src/run.py"]