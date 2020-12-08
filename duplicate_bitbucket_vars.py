## TODO's:
## - Handle multiple pages of variables
## - Add more error handling for unexpected API responses

import requests

class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'

class Config:
    API_PREFIX = 'https://api.bitbucket.org/2.0/'
    USERNAME = ''
    PASSWD = ''
    REPO_FROM = ''
    REPO_TO = ''

def print_ok(msg):
    print(Colors.GREEN + msg + Colors.END)

def print_info(msg):
    print(Colors.BLUE + msg + Colors.END)

def print_fail(msg):
    print(Colors.RED + msg + Colors.END)

def get_variables():
    api_url = Config.API_PREFIX + "repositories/" + Config.REPO_FROM + "/pipelines_config/variables/"

    response = requests.get(url = api_url, auth = (Config.USERNAME, Config.PASSWD))

    json = response.json()

    print_ok("Found " + str(json['size']) + " variables in " + Config.REPO_FROM + ": ")

    variables = {}

    for value in json['values']:
        if value['type'] != 'pipeline_variable':
            continue

        if value['secured']:
            print_fail("\t'" + value['key'] +  "' **SECURED, IGNORING**")
            continue

        variables[value['key']] = value['value']

        print_info("\t" + value['key'] +  ": " + value['value'])

    return variables

def update_variables(variables):
    api_url = Config.API_PREFIX + "repositories/" + Config.REPO_TO + "/pipelines_config/variables/"

    for key in variables:
        data = {
            'key': key,
            'value': variables[key],
            'secured': False
        }

        response = requests.post(url = api_url, json = data, auth = (Config.USERNAME, Config.PASSWD))
        print(response.json())

def get_input(msg):
    entered = input(msg)

    while not entered:
        print_fail("Please enter a value!")
        entered = input(msg)

    return entered

def main():
    Config.USERNAME = get_input("Username: ")
    Config.PASSWD = get_input("App Password: ")
    Config.REPO_FROM = get_input("Repo path from, i.e. workspace/project: ")
    Config.REPO_TO = get_input("Repo path to, i.e. workspace/project: ")

    print_ok("Requesting variables from " + Config.REPO_FROM)

    variables = get_variables()

    print_ok("Inserting " + str(len(variables)) + " variables into " + Config.REPO_TO)

    update_variables(variables)

    print_ok("Done, view here: https://bitbucket.org/" + Config.REPO_TO + "/admin/addon/admin/pipelines/repository-variables")


main()
