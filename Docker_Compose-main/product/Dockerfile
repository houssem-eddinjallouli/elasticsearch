FROM python:3.7-slim
WORKDIR /app
RUN mkdir -p /app/data
ADD . /app
ADD ./data /app/data
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["api.py"]