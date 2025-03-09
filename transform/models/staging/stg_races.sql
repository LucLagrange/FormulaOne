MODEL (
    name staging.stg_races,
    kind VIEW,
    cron '@daily',
    grain id_race,
    description 'The races on the Formula One Championship',
    column_descriptions (
        id_race = "Unique identifier for the race (name + season)",
        race_name = 'Name of the race',
        constructor_name = 'Properly formatted name of the constructor',
        constructor_url = 'The Wikipedia URL of the constructor',
        nationality = 'The nationality of the constructor'
    )
);

SELECT
    CONCAT(raceName, '-', season) AS id_race,
    raceName AS race_name,
    CAST(`date` AS DATE) AS dt_race,
    CAST(round AS INT) AS round_number,
    season AS race_season,
    url AS race_url,
FROM
    raw_data.Races