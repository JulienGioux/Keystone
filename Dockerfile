# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy poetry dependency files
COPY poetry.lock pyproject.toml /app/

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copy the rest of the application
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.keystone.main:app", "--host", "0.0.0.0", "--port", "8000"]
