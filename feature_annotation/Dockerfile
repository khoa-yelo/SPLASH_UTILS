FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (if any)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.11.0/ncbi-blast-2.11.0+-x64-linux.tar.gz \
    && tar -xzvf ncbi-blast-2.11.0+-x64-linux.tar.gz \
    && mv ncbi-blast-2.11.0+/ /usr/local/blast \
    && ln -s /usr/local/blast/bin/* /usr/local/bin/

# Install Biopython
RUN pip install --no-cache-dir biopython

# Clone the SeqUtils repository
# Replace the URL with the actual URL of your SeqUtils repo
RUN git clone https://github.com/khoa-yelo/SeqUtils.git

# Change working directory to SeqUtils
WORKDIR /app/SeqUtils

RUN pip install --no-cache-dir -r requirement.txt
# Install SeqUtils as an editable package
RUN pip install --no-cache-dir -e .

# By default, run an interactive Python shell
CMD ["python3"]