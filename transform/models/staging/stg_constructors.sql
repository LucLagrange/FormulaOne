MODEL (
    name staging.stg_constructors,
    kind VIEW,
    cron '@daily',
    grain id_constructor,
    description 'The constructors that race in the Formula One Championship',
    column_descriptions (
        id_constructor = 'Unique identifier for the constructor',
        constructor_name = 'Properly formatted name of the constructor',
        constructor_url = 'The Wikipedia URL of the constructor',
        nationality = 'The nationality of the constructor'
    ),
    audits (
       unique_values(columns = id_constructor),
       not_null(columns = id_constructor)
    )
);

SELECT
    CAST(constructorid AS STRING) AS id_constructor,
    name AS constructor_name,
    url AS constructor_url,
    nationality,
FROM
    raw_data.Constructors