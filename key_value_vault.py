import argparse
import json
import os
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("-k", "--key", help="the vault-key")
parser.add_argument("-v", "--value", help="key value stored to vault")
args = parser.parse_args()
diction = {}

if args.key:
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    if not os.path.exists(storage_path):
        with open(storage_path, 'w') as f:
            f.write("")
    with open(storage_path, 'r+') as f:
        if f.read() != "":
            f.seek(0)
            diction = json.loads(f.read())
        if args.value:
            if args.key in diction:
                if args.value not in diction[args.key]:
                    diction[args.key].append(args.value)
            else:
                diction[args.key] = [args.value, ]
            f.seek(0)
            f.write(json.dumps(diction))
            f.truncate(f.tell())

        else:
            if args.key in diction:
                print(', '.join(diction[args.key]))
            else:
                print(None)
