from typing import Iterable

from ORM.schemas import SMarkIn, SMarkOut
from config.logger import logger
from .schemas import SAnalyze, SUpdated


def analyze_schemas(
        new_schemas: Iterable[SMarkIn],
        old_schemas: Iterable[SMarkOut]
) -> SAnalyze:
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

    updated_schemas: list[SUpdated] = []
    added_schemas: list[SMarkIn] = []
    unused_schemas: list[SMarkOut] = []

    for new_schema in new_schemas:
        new_schema_hash = hash(new_schema)
        old_schema = old_schemas_dict.get(new_schema_hash)
        if old_schema is not None:
            del old_schemas_dict[new_schema_hash]

            if old_schema != new_schema:
                updated_schemas.append(SUpdated(
                    old_schema=old_schema,
                    new_schema=new_schema
                ))
        else:
            added_schemas.append(new_schema)

    unused_schemas.extend([*old_schemas_dict.values()])

    logger.info(f"updated = {len(updated_schemas)} | "
                f"added = {len(added_schemas)} | "
                f"unused = {len(unused_schemas)}")

    return SAnalyze(
        updated_schemas=updated_schemas,
        added_schemas=added_schemas,
        unused_schemas=unused_schemas
    )
