# Pull latest official Python image
FROM python:latest

# Set the working directory to /code
WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# Copy local contents into the container
COPY ./requirements.txt /src/requirements.txt

# Install all required dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /src/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
