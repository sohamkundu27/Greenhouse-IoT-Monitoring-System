# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    libssl-dev \
    libffi-dev \
    build-essential \
    curl \
    && apt-get clean

# Copy requirements.txt
COPY requirements.txt /app/

# Debug: Install dependencies one by one
RUN pip install --no-cache-dir asgiref==3.8.1
RUN pip install --no-cache-dir azure-core==1.32.0
RUN pip install --no-cache-dir azure-eventhub==5.13.0
RUN pip install --no-cache-dir certifi==2024.12.14
RUN pip install --no-cache-dir charset-normalizer==3.4.1
RUN pip install --no-cache-dir Django==4.2.5
RUN pip install --no-cache-dir django-cors-headers==4.6.0
RUN pip install --no-cache-dir djangorestframework==3.15.2
RUN pip install --no-cache-dir idna==3.10
RUN pip install --no-cache-dir requests==2.32.3
RUN pip install --no-cache-dir six==1.17.0
RUN pip install --no-cache-dir sqlparse==0.5.3
RUN pip install --no-cache-dir typing_extensions==4.12.2
RUN pip install --no-cache-dir urllib3==2.3.0

# Copy the rest of the project
COPY . /app/

# Expose port 8000 and run the Django development server
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]