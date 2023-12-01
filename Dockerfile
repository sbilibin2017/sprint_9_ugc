# Use the official Python image as the base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /opt/app

ENV PYTHONPATH '/opt/app'

COPY pyproject.toml ./
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

# Start a bash shell by default
CMD ["/bin/bash"]
