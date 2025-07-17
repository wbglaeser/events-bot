FROM python:3.11-slim

# Install Poetry
RUN pip install --no-cache-dir poetry

# Set workdir
WORKDIR /app

# 1) Copy pyproject files
COPY pyproject.toml poetry.lock* ./

# 2) Copy your package code so Poetry can see it
COPY app/ ./app/

# 3) Install dependencies (and your project)
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --only main

# Expose port & run
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]