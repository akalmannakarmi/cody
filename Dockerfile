FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose port 5000
EXPOSE 5000

# Command to run the app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
