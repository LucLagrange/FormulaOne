MODEL (
    name staging.stg_races,
    kind VIEW,
    cron '@daily',
    grain id_race,
    description 'The races on the Formula One Championship',
    column_descriptions (
        id_race = "Unique identifier for the race (season + round)",
        id_circuit = 'Identifier for the circuit the race takes part at',
        race_name = 'Name of the race',
        dt_race = 'The date of the race',
        season = 'The season the race takes part in',
        url = 'The url of the season'
    ),
    audits (
       unique_values(columns = id_race),
       not_null(columns = id_race)
    )
);

SELECT
    CONCAT(season, '-', round) AS id_race,
    JSON_VALUE(Circuit, '$.circuitId') AS id_circuit,
    raceName AS race_name,
    CAST(`date` AS DATE) AS dt_race,
    CAST(round AS INT) AS round_number,
    season AS race_season,
    url AS race_url,
FROM
    raw_data.Races