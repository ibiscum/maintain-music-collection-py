FROM python:slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends --assume-yes build-essential libpq-dev python3-dev

# Create the virtual environment.
RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH

WORKDIR /opt
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# final stage
FROM python:slim

ARG USERNAME=cronpg
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
ENV PATH=/venv/bin:$PATH

# Copy the application in .
COPY . .
USER cronpg

CMD [ "python3", "/opt/app/cronpg.py" ]