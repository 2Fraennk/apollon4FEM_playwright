FROM debian:stable-20240110

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
RUN poetry install
#RUN poetry activate

#EXPOSE 380

#ENTRYPOINT [ "/usr/bin/echo \"hello world\"" ]

#CMD /usr/bin/python .activemq.main

CMD ["/usr/bin/sleep", "300"]