FROM debian:stable-20240110

# Custom cache invalidation
ARG CACHEBUST=1

ENV TZ="Europe/Berlin"

WORKDIR /usr/local/apollon
RUN apt-get update
RUN apt-get install -y sudo
RUN apt-get install -y git \
    python3 \
    python3-poetry
RUN git --version
RUN python3 --version

RUN git clone https://github.com/2Fraennk/apollon4FEM_playwright.git .
RUN git switch dev
RUN poetry config virtualenvs.create false
RUN poetry install
RUN playwright install --with-deps firefox

WORKDIR /usr/local/apollon/poetryPlaywright/src

CMD ["python3", "-m", "activeMq.main"]
