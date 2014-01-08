import random
import pyen
import simplejson


# collects the set of genres into a randomized json list

random.seed(1)
en = pyen.Pyen()

response = en.get('genre/list', bucket=['description', 'urls'])

full = []
partial = []

for g in response['genres']:
    if len(g['description']) > 0 and 'wikipedia_url' in g['urls']:
        full.append(g['name'])
    else:
        partial.append(g['name'])

random.shuffle(full)
random.shuffle(partial)

print simplejson.dumps(full + partial, indent=4)
