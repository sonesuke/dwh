FROM openjdk:8

RUN wget -q https://dl.embulk.org/embulk-latest.jar -O /bin/embulk \
  && chmod +x /bin/embulk

RUN embulk gem install embulk-output-postgresql

RUN wget https://github.com/sonesuke/embulk-input-salesforce_bulk/releases/download/no-querySelectFrom/embulk-input-salesforce_bulk-0.2.3.gem -O embulk-input-salesforce_bulk-0.2.3.gem \
  && embulk gem install --local embulk-input-salesforce_bulk-0.2.3.gem

RUN apt-get update \
    && apt-get install -y \
        python3 \
        python3-pip \
        python3-dev \
    && pip3 install prefect

RUN pip3 install fire simple-salesforce tqdm stringcase

WORKDIR /work
ENTRYPOINT ["python3", "task.py"]