# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the entire app folder into the container
COPY ./app /code/app

# Command to run the FastAPI app using Uvicorn
# Note: We use 0.0.0.0 to allow external access
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
