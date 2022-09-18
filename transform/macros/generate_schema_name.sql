-- /*
-- change dbt behaviour of generating schemas
-- prod
--   if a custom schema is provided, a model's schema name should match the custom schema, rather than being concatenated to the target schema.
--   if no custom schema is provided, a model's schema name should match the target schema.
-- other (dev/qa)
--   build all models in the target schema, as in, ignore custom schema configurations.
-- */

{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}

        {{ default_schema }}

    {%- else -%}

        {{ custom_schema_name | trim }}

    {%- endif -%}

{%- endmacro %}