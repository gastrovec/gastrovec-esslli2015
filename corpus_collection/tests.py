import json
import sys

r = set()
with open(sys.argv[1]) as f:
    for line in f:
        recipe = json.loads(line)
        r.add(recipe["name"])
print(len(r))
