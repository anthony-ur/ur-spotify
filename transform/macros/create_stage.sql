{% macro create_stage(database, schema, stage) -%}
    USE {{database}};
    CREATE STAGE IF NOT EXISTS {{ schema }}.{{ stage }};
{%- endmacro %}