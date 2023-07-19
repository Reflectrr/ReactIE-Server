# Use a base image
FROM python:3.9

# Install Maven and Make
RUN apt-get update && apt-get install -y maven make

# Copy the necessary files to the container
COPY . /app

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Specify the command to run the Flask server
CMD ["flask", "--app", "ReactIE_server.py", "run", "--host=0.0.0.0", "--port=80"]
