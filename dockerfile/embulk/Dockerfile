FROM openjdk:8-jre-alpine

RUN wget -q https://dl.embulk.org/embulk-latest.jar -O /bin/embulk \
  && chmod +x /bin/embulk

RUN apk add --no-cache libc6-compat \
  && embulk gem install embulk-input-salesforce_bulk \
  && embulk gem install embulk-output-postgresql

WORKDIR /work

ENTRYPOINT ["java", "-jar", "/bin/embulk"]