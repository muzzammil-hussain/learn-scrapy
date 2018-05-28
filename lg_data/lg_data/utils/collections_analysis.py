import json
from os.path import join, dirname

# load data file

with open(join(dirname(__file__), "../../result.json")) as fp:
    results = json.loads(str(fp.read()))

final_collections = []
for result in results:
    for collection in result["collections"]:
      if collection not in final_collections:
          final_collections.append(collection)

print(set(final_collections))

# if wid_route:
#     LOGGER.info('Writing route map: {}'.format(filename))
#     separators = (',', ': ')
#     ordered_map = save_map(wid_route)
#     open(filename, 'w').write(
#         json.dumps(ordered_map, indent=2, separators=separators)
#     )
#
