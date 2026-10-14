{% macro drop_schema() %}
  {% do run_query("DROP SCHEMA IF EXISTS " ~ target.schema ~ " CASCADE") %}
  {% do log("Dropped schema: " ~ target.schema, info=true) %}
{% endmacro %}