#!/usr/bin/env python3

from hashlib import md5
import re

hash = "ad2e1c419eb66c002c3bdd7bad415203"

# b\d{3}-e\dba-\dd\d{2}-11ec

template = "b{}{}{}-d{}ba-{}d{}{}-11ec"
pattern = r"ctftech\{b\d\d\d-e\dba-\dd\d\d-11ec\}"

for i in range(10**7):
    code = f"{i:07d}"
    template = "ctftech{"
    template += f"b{code[:3]}-e{code[3]}ba-{code[4]}d{code[5]}{code[6]}-11ec"
    template += "}"
    """ print(re.match(pattern, template)) """
    if md5(template.encode()).hexdigest() == hash:
        print(template)
