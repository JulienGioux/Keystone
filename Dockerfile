# 1. Base Image
FROM python:3.12-slim
# 2. Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

# 3. Set Work Directory
WORKDIR /app

# 4. Install Poetry
RUN pip install poetry

# 5. Copy poetry dependency files from the 'keystone' subdirectory
COPY keystone/poetry.lock keystone/pyproject.toml /app/
COPY keystone/README.md /app/

# 6. Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-root

# 7. Copy application code from the 'keystone/src' subdirectory
COPY keystone/src /app/src

# 8. Expose port
EXPOSE 8000

# 9. Command to run
CMD ["uvicorn", "src.keystone.main:app", "--host", "0.0.0.0", "--port", "8000"]
