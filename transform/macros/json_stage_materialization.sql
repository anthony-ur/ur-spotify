{% materialization json_stage, adapter='snowflake' -%}
    {%- set identifier = model['alias'] -%}
    {%- set stage_name = config.require('stage_name') -%}
    {%- set file_pattern = config.require('file_pattern') -%}

    {%- set old_relation = adapter.get_relation(database=database, schema=schema, identifier=identifier) -%}
    {%- set target_relation = api.Relation.create(database=database, schema=schema, identifier=identifier, type='table') -%}

    {%- set full_refresh_mode = (flags.FULL_REFRESH == True) -%}
    {%- set exists_as_table = (old_relation is not none and old_relation.is_table) -%}
    {%- set should_drop = (full_refresh_mode or not exists_as_table) -%}

    -- setup
    {% if old_relation is none -%}
        -- noop
    {%- elif should_drop -%}
        {{ adapter.drop_relation(old_relation) }}
        {%- set old_relation = none -%}
    {%- endif %}

    {{ run_hooks(pre_hooks, inside_transaction=False) }}

    -- `BEGIN` happens here:
    {{ run_hooks(pre_hooks, inside_transaction=True) }}

    -- build model
    {% if full_refresh_mode or old_relation is none -%}
        {#
            -- Create an empty table with columns as specified in sql.
            -- We append a unique invocation_id to ensure no files are actually loaded, and an empty row set is returned,
            -- which serves as a template to create the table.
        #}
        {%- call statement() -%}
            CREATE OR REPLACE TABLE {{ target_relation }} (data variant)
        {%- endcall -%}
    {%- endif %}

    {# Perform the main load operation using COPY INTO #}
    {# See https://docs.snowflake.net/manuals/user-guide/data-load-considerations-load.html #}
    {# See https://docs.snowflake.net/manuals/user-guide/data-load-transform.html #}
    {%- call statement('main') -%}
        {# TODO: Figure out how to deal with the ordering of columns changing in the model sql... #}
        COPY INTO {{ target_relation }}
        FROM {{ stage_name }}
        file_format = (type = json strip_outer_array = true)
        pattern = {{ "'" ~ file_pattern ~ "'" }}
    {% endcall %}

    {{ run_hooks(post_hooks, inside_transaction=True) }}

    -- `COMMIT` happens here
    {{ adapter.commit() }}

    {{ run_hooks(post_hooks, inside_transaction=False) }}

    -- Return the relations created in this materialization
    --{{ return({'relations': [target_relation]}) }}

{%- endmaterialization %}