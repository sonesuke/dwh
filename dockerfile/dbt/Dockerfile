FROM python:latest


# install exa fdfind rg prcs
RUN apt-get update \
    && apt-get install -y exa fd-find ripgrep rpm
RUN echo "alias fd='fdfind'" >> ~/.bashrc

RUN rpm -i https://github.com/dalance/procs/releases/download/v0.9.20/procs-0.9.20-1.x86_64.rpm

RUN wget https://github.com/sharkdp/bat/releases/download/v0.12.1/bat-musl_0.12.1_amd64.deb \
    && dpkg -i bat-musl_0.12.1_amd64.deb \
    && rm *.deb \
    && apt-get update \
    && apt-get install -y less

RUN pip install dbt
