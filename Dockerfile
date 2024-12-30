# Uses the official Python image
FROM python:3.12-slim

# Sets the working directory in the container
WORKDIR /app

# Installs system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unixodbc \
    unixodbc-dev \
    gcc \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    build-essential && \
    apt-get clean

# Installs the Microsoft ODBC Driver for SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Copies the project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Exposes the port Flask runs on
EXPOSE 5000

# Runs the Flask app
CMD ["python", "app.py"]
