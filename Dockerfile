# Use a base image
FROM maven:3-jdk-11

# Install Maven and Make
RUN apt-get update && apt-get install -y make python3.9 python3-pip
RUN ln -s /usr/bin/python3.9 /usr/local/bin/python

# Copy the necessary files to the container
COPY . /app

# Install SymbolScraper
WORKDIR /app/ReactIE_PDF_Conversion/SymbolScraper
RUN make

# Install dependencies
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Specify the command to run the Flask server
# CMD ["flask", "--app", "ReactIE_server.py", "run", "--host=0.0.0.0", "--port=443", "--cert=adhoc"]
CMD ["bash"]
