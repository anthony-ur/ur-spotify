"""Snowflake utilities"""

from permifrost.spec_file_loader import load_spec, PermifrostSpecSchema
from permifrost.entities import EntityGenerator

spec = load_spec("/workspace/roles.yml")

for db_dict in spec["databases"]:
    for db_name,db_info in db_dict.items():
        print(db_name,db_info)
        print(f"CREATE DATABASE IF NOT EXISTS {db_name};")


# entity_generator = EntityGenerator(spec=spec)
# entities = entity_generator.generate()
# entities["databases"].
# #print(spec)
# print(spec["databases"])