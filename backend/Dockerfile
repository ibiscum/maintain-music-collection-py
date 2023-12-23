# pull official base image
FROM python:slim as builder

# set work directory
WORKDIR /opt

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends --assume-yes build-essential libpq-dev python3-dev

# Create the virtual environment.
RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Final stage
FROM python:slim

ARG USERNAME=backend
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends --assume-yes libpq5 && \
    apt-get clean

WORKDIR /opt

COPY --from=builder /venv /venv

# Copy the application in .
COPY . .
USER backend

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0" ]
