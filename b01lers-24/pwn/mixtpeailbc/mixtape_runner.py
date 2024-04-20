#!/usr/bin/env python3

import base64
import subprocess
import tempfile
import time


def main():
    print('Enter base64 encoded mixtape bytecode')

    data = input('>> ')
    try:
        data = base64.b64decode(data)
    except BaseException:
        print('invalid base64 encoding')
        return

    if len(data) > 8000:
        print('bytecode to long')
        return

    open("output.bin", "wb").write(data)

    with tempfile.NamedTemporaryFile('wb') as f:
        f.write(data)
        f.flush()
        subprocess.run(['./mixtape', f.name])


if __name__ == '__main__':
    main()
