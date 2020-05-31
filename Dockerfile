FROM python:3.8
RUN pip install pipenv
COPY Pipfile* /app/
WORKDIR /app
RUN pipenv install --system --deploy
COPY . /app/
RUN python -m unittest test/*
ENV PYTHONPATH "${PYTHONPATH}:/openinghours/app"
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["openinghours/app/app_api.py"]
