-- To be able to grant future privileges on Snowflake, your role needs to have the manage grants privilege
-- use role securityadmin;
-- grant manage grants on account to role transformer;

{% macro grant_select_on_schemas(database, role, schemas) %}
    use {{database}};
  {% for schema in schemas %}
    grant usage on schema {{ schema }} to role {{ role }};
    grant select on all tables in schema {{ schema }} to role {{ role }};
    grant select on all views in schema {{ schema }} to role {{ role }};
    -- grant select on future tables in schema {{ schema }} to role {{ role }};
    -- grant select on future views in schema {{ schema }} to role {{ role }};
  {% endfor %}
{% endmacro %}