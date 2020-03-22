FROM python:latest

RUN wget https://github.com/ForceCLI/force/releases/download/v0.27.1/force_linux_amd64 -O /bin/force
RUN chmod +x /bin/force
RUN pip install simple_salesforce jinja2 tqdm
