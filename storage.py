import os
import tempfile
import json
import argparse


def clear():
    os.remove(storage_path)


def import_data(path):
    if not os.path.exists(path):
        data = dict()
    else:
        with open(path, 'r', encoding='utf8') as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                data = dict()
    return data


def add(key, val, path):
    data = import_data(path)
    if key and val:
        if key in data:
            data[key].append(val)
        else:
            data[key] = [val]

        with open(path, 'w') as f:
            json.dump(data, f)


def get(key, path):
    data = import_data(path)
    return data.get(key, [])


if __name__ == '__main__':
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

    parser = argparse.ArgumentParser()
    parser.add_argument('--key', action='store', dest='key')
    parser.add_argument('--val')  # то же, что и на строку выше
    parser.add_argument('--clear', action='store_true')  # аргумент без значения

    args = parser.parse_args()

    if args.clear:
        clear()
    elif args.key and args.val:
        add(args.key, args.val, storage_path)
    elif args.key:
        print(', '.join(get(args.key, storage_path)))
    else:
        print('Unknown command')
