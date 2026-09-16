# Official Playwright Python image (comes with Python and pre-installed browsers)
FROM mcr.microsoft.com/playwright/python:v1.49.0-noble

WORKDIR /app

# Install Python test dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy tests and project files
COPY . .

# Default command to run tests inside the container
CMD ["pytest", "-v"]
