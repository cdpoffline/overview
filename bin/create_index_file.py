#!/usr/bin/python

import os
import pprint
# see http://pyyaml.org/wiki/PyYAML#Documentation
import yaml
# see http://jinja.pocoo.org/docs/dev/intro/#basic-api-usage
from jinja2 import Template

CONFIGURATION_FILENAME = "module.yml"
TEMPLATE_FILE = "../index.html.j2"
INDEX_FILE = "../web/index.html"

this_directory = os.path.dirname(__file__)
modules_path = os.path.join(this_directory, "../..")
module_names = os.listdir(modules_path)
template_path = os.path.join(this_directory, TEMPLATE_FILE)
index_path = os.path.join(this_directory, INDEX_FILE)

# collect variables
materials = {}
variables = dict(materials = materials)

for module_name in module_names:
    module_path = os.path.join(modules_path, module_name)
    configuration_filename = os.path.join(module_path, CONFIGURATION_FILENAME)
    if os.path.isfile(configuration_filename):
        with open(configuration_filename) as configuration_file:
            module_variables = yaml.load(configuration_file)
        materials[module_name] = module_variables

pprint.pprint(variables)

# render template
with open(template_path) as template_file:
    template_text = template_file.read()

template = Template(template_text)
with open(index_path, "w") as index_file:
    index_file.write(template.render(variables))









