from typing import TypeVar, Iterable

from utils.decors import time_count

Schema = TypeVar("Schema")


@time_count
def analyze_schemas(
        new_schemas: Iterable[Schema],
        old_schemas: Iterable
):
    old_schemas_dict = {}
    for old_schema in old_schemas:
        old_schema_hash = hash(old_schema)
        in_dict_old_schema = old_schemas_dict.get(old_schema_hash)
        if in_dict_old_schema is None:
            old_schemas_dict[old_schema_hash] = old_schema
        else:
            raise RuntimeError(f"schema with hash {old_schema_hash} is already exists: \n"
                               f"{in_dict_old_schema}\n"
                               f"compared schema - {old_schema}")

    updated_schemas: list[Schema] = []
    added_schemas: list[Schema] = []
    no_more_schemas: list[Schema] = []

    for new_schema in new_schemas:
        new_schema_hash = hash(new_schema)
        old_schema = old_schemas_dict.get(new_schema_hash)
        if old_schema is not None:
            del old_schemas_dict[new_schema_hash]

            if old_schema != new_schema:
                updated_schemas.append(new_schema)
        else:
            added_schemas.append(new_schema)

    return updated_schemas, added_schemas, no_more_schemas
