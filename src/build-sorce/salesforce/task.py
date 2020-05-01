import fire
import os
import re
from tqdm import tqdm
from prefect import Flow
from prefect.tasks.shell import ShellTask
from simple_salesforce import Salesforce
from stringcase import snakecase


def check_sobject(sf, name):
    try:
        getattr(sf.bulk, name).query("SELECT Id FROM {} LIMIT 1".format(name))
        return True
    except:
        return False


class CLI(object):
    """ETL CLI."""

    def sobjects(self):
        sf = Salesforce(
            username=env['SALESFORCE_USER'],
            password=env['SALESFORCE_PASSWORD'],
            security_token=env['SALESFORCE_TOKEN']
        )
        with open('/work/sobjects.txt', 'w') as f:
            for sobject in tqdm(sf.describe()["sobjects"]):
                if check_sobject(sf, sobject['name']):
                    f.write(sobject["name"] + '\n')

    def build(self):
        tasks = []
        with open('sobjects.txt') as sobjects_file:
            for sobject in sobjects_file.readlines():
                target = sobject.strip()
                env = {
                    'SALESFORCE_USER': os.environ.get('SALESFORCE_USER'),
                    'SALESFORCE_PASSWORD': os.environ.get('SALESFORCE_PASSWORD'),
                    'SALESFORCE_TOKEN': os.environ.get('SALESFORCE_TOKEN'),
                    'POSTGRES_USER': os.environ.get('POSTGRES_USER'),
                    'POSTGRES_PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
                    'SALESFORCE_SOBJECT': target,
                    'POSTGRES_TABLE': 'sf_' + snakecase(target),
                }
                command = 'java -jar /bin/embulk run /work/salesforce.yml.liquid -c /work/diff/{}.diff.yml'.format(
                    target)
                task = ShellTask(
                    name=target,
                    command=command,
                    log_stdout=True,
                    return_all=True,
                    env=env
                )
                tasks.append(task)
        with Flow("build source", tasks=tasks) as f:
            pass
        out = f.run()
        #from prefect.engine.executors.dask import LocalDaskExecutor
        #out = f.run(executor=LocalDaskExecutor(scheduler="processes"))


if __name__ == '__main__':
    fire.Fire(CLI)
