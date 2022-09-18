{% macro create_schemas(database, schemas) -%}
    USE {{database}};
    {% for schema in schemas %}
        CREATE SCHEMA IF NOT EXISTS {{ schema }};
    {% endfor %}
{%- endmacro %}