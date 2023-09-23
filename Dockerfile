# Use an official Python runtime as a parent image
FROM python:3.10.8

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
# ADD . /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# docker build -t my_fastapi_app .

# docker run -d --name my_fastapi_container -p 8000:8000 -v D:\microservices\ya_cl_speech_rec_backend:/app my_fastapi_app