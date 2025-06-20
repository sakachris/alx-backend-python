# Step 1: Using official Python image
FROM python:3.10-slim

# Step 2: Setting environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Step 3: Setting work directory
WORKDIR /app

# Step 4: Installing dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Step 5: Copying project files
COPY . /app/

# Step 6: Exposing the port Django runs on
EXPOSE 8000

# Step 7: Running development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
