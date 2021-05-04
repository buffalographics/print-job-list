import json


def pretty_print(arg):
    print(json.dumps(arg, indent=4, sort_keys=True))
