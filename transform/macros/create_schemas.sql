{% macro create_schemas(database, schemas) -%}
    {% for schema in schemas %}
        CREATE SCHEMA IF NOT EXISTS {{ schema }};
    {% endfor %}
{%- endmacro %}