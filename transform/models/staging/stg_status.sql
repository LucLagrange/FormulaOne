MODEL (
    name staging.stg_status,
    kind VIEW,
    cron '@daily',
    grain id_status,
    description 'The different available status for each car at the end of a race',
    column_descriptions (
        id_status = 'Unique identifier for the status',
        status_name = "The name of the status",
        nb_occurrences = "Occurrence number of a status"
    ),
    audits (
       unique_values(columns = id_status),
       not_null(columns = id_status)
    )
);

SELECT
  CAST(base_table.statusId AS STRING) AS id_status,
  base_table.status AS status_name,
  CAST(base_table.count AS INT) AS nb_occurrences
FROM
    raw_data.Status AS base_table