# Use a base image
FROM maven:3-jdk-11

# Install Make and Python 3.9
RUN apt-get update 
RUN apt-get install -y make python3.9 python3-pip vim

# Set Python 3 as the default version
RUN ln -s /usr/bin/python3.9 /usr/local/bin/python

# Copy the necessary files to the container
COPY . /app

# Install Symbol Scraper
WORKDIR /app/PDFConversion/SymbolScraper
RUN make

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# # Expose a port
EXPOSE 5000

# # Specify the command to run the Flask server
CMD ["flask", "--app", "ReactIE_server.py", "run"]