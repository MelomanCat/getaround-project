FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    curl \
    unzip \
    nano \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel


# THIS IS SPECIFIC TO HUGGINFACE
# We create a new user named "user" with ID of 1000
RUN useradd -m -u 1000 user
# We switch from "root" (default user when creating an image) to "user" 
USER user
# We set two environmnet variables 
# so that we can give ownership to all files in there afterwards
# we also add /home/user/.local/bin in the $PATH environment variable 
# PATH environment variable sets paths to look for installed binaries
# We update it so that Linux knows where to look for binaries if we were to install them with "user".
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# We set working directory to $HOME/app (<=> /home/user/app)
WORKDIR /home/user/app

# Copy all local files to /home/user/app with "user" as owner of these files
# Always use --chown=user when using HUGGINGFACE to avoid permission errors
COPY --chown=user requirements.txt /home/user/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user . /home/user/app

ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

#CMD fastapi run app.py --port $PORT
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app:app", "--bind", "0.0.0.0:7860"]