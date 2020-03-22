import os
from jinja2 import Environment, FileSystemLoader
from simple_salesforce import Salesforce


type_map = {
    'boolean': {'type': 'boolean', 'format': ''},
    'int': {'type': 'long', 'format': ''},
    'datetime': {'type': 'timestamp', 'format': "%FT%T.%L%Z"},
    'date': {'type': 'timestamp', 'format': "%F"},
    'picklist': {'type': 'string', 'format': ''},
    'id': {'type': 'string', 'format': ''},
    'reference': {'type': 'string', 'format': ''},
    'string': {'type': 'string', 'format': ''},
    'textarea': {'type': 'string', 'format': ''},
    'double': {'type': 'double', 'format': ''},
    'phone': {'type': 'string', 'format': ''},
    'url': {'type': 'string', 'format': ''},
    'email': {'type': 'string', 'format': ''},
    'currency': {'type': 'string', 'format': ''},
    'percent': {'type': 'double', 'format': ''},
    'combobox': {'type': 'string', 'format': ''},
}


def filtered(f):
    if f['type'] == 'address':
        return False
    if f['name'] == 'IndividualId':
        return False
    return True


sobjects = [
    'Account',
    'Contact',
    'Lead',
    'Opportunity',
    'Event',
    'Task',
]


sf = Salesforce(
    username=os.environ['SALESFORCE_USER'],
    password=os.environ['SALESFORCE_PASSWORD'],
    security_token=os.environ['SALESFORCE_TOKEN']
)

env = Environment(loader=FileSystemLoader('/host/src/tools/templates/', encoding='utf-8'))
template = env.get_template('salesforce-postgres.yml.liquid')
for sobject in sobjects:
    fields = {f['name']: type_map[f['type']] for f in getattr(sf, sobject).describe()['fields'] if filtered(f)}
    generated = template.render(table=sobject, fields=fields)
    output_file = os.path.join('/host/src/embulk/salesforce/', sobject.lower() + '.yml.liquid')
    with open(output_file, 'w') as f:
        f.write(generated)

template = env.get_template('docker-compose.embulk.yml')
generated = template.render(sobjects=sobjects)
with open(os.path.join('/host/docker-compose.embulk.yml'), 'w') as f:
    f.write(generated)