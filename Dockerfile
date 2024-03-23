FROM python:3.9
EXPOSE 8000
ADD /src/ /app/

RUN pip install -r /app/requirements.txt

CMD ["sh", "app/docker-entrypoint.sh"] 