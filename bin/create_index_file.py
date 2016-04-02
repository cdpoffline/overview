#!/usr/bin/python2

import os
import sys
import pprint
# see http://pyyaml.org/wiki/PyYAML#Documentation
import yaml
# see http://jinja.pocoo.org/docs/dev/intro/#basic-api-usage
from jinja2 import FileSystemLoader, Environment

DEFAULT_CONFIGURATOIN_FILENAME = "../default.yml"
CONFIGURATION_FILENAME = "module.yml"
MENU_TEMPLATE = "menu.html.j2"
TEMPLATE_FOLDER = "../templates"
INDEX_FILE = "../web/index.html"
INDEX_FOLDER = "../web/menu"
INDEX_TEMPLATE = "index.html.j2"

this_directory = sys.argv[1]
modules_path = os.path.dirname(os.path.dirname(os.path.join(this_directory)))
module_names = os.listdir(modules_path)
template_path = os.path.join(this_directory, TEMPLATE_FOLDER)
index_file_path = os.path.join(this_directory, INDEX_FILE)
index_folder_path = os.path.join(this_directory, INDEX_FOLDER)
template_folder_path = os.path.join(this_directory, TEMPLATE_FOLDER)
default_configuration_path = os.path.join(this_directory, DEFAULT_CONFIGURATOIN_FILENAME)

loader = FileSystemLoader(template_folder_path)
env = Environment(loader = loader)

# collect variables
variables = {}

def update_variables(update, variables = variables):
    if isinstance(update, dict):
        for name in update:
            if name not in variables or not update_variables(update[name], variables[name]):
                variables[name] = update[name]
        return True
    return False

def add_configuration_file(configuration_filename):
    with open(configuration_filename) as configuration_file:
        module_variables = yaml.load(configuration_file)
    update_variables(module_variables)

add_configuration_file(default_configuration_path)

for module_name in module_names:
    module_path = os.path.join(modules_path, module_name)
    configuration_filename = os.path.join(module_path, CONFIGURATION_FILENAME)
    if os.path.isfile(configuration_filename):
        add_configuration_file(configuration_filename)

pprint.pprint(variables)

# determine default language
class TranslationError(ValueError):
    pass

if "default-language" not in variables:
    raise TranslationError("Please define a variable \"default-language\" and put in a language code.")
default_language = variables["default-language"]

# collect languages
languages = variables['languages'] = [default_language]
def collect_languages(s):
    if not isinstance(s, dict):
        return s
    for language in s:
        if language not in languages:
            languages.append(language)
    return s[list(s.keys())[0]]

env.filters['t'] = collect_languages
template = env.get_template(MENU_TEMPLATE)
template.render(variables)

# render languages

def translate(s):
    if isinstance(s, type("")) or isinstance(s, type(u"")):
        return s
    if not isinstance(s, dict):
        raise TranslationError("Cannot translate \"{}\". It should be an mapping from language to text.".format(s))
    if language in s:
        return s[language]
    if default_language in s:
        return s[default_language]
    if s:
        return s[list(s.keys())[0]]
    raise TranslationError("Could not translate empty content of \"{}\". It should be a mapping from language to text.".format(s))

env.filters['t'] = translate
template = env.get_template(MENU_TEMPLATE)

if not os.path.isdir(index_folder_path):
    os.makedirs(index_folder_path)

for language in languages:
    file_name = language + ".html"
    file_path = os.path.join(index_folder_path, file_name)
    print("Creating \"{}\".".format(file_path))
    with open(file_path, "w") as index_file:
        index_file.write(template.render(variables).encode("UTF-8"))

template = env.get_template(INDEX_TEMPLATE)
with open(index_file_path, "w") as index_file:
    index_file.write(template.render(variables).encode("UTF-8"))








