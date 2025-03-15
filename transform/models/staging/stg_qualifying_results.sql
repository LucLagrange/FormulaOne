MODEL (
    name staging.stg_qualifying_results,
    kind VIEW,
    cron '@daily',
    grain id_qualifying_result,
    description 'The qualifying results for each driver, at each season round',
    column_descriptions (
        id_qualifying_result = 'Unique identifier for the qualifying result, combining season, round, and driver ID',
        id_race = 'Unique identifier for the race',
        race_season = 'The season in which the race took place',
        round_number = 'The round number of the season',
        result = 'The qualifying position achieved by the driver',
        id_driver = 'Unique identifier for the driver',
        id_constructor = 'Unique identifier for the constructor',
        q1_best_time = 'Best time achieved by the driver in the Q1 session',
        q2_best_time = 'Best time achieved by the driver in the Q2 session',
        q3_best_time = 'Best time achieved by the driver in the Q3 session',
        event_type = 'The type of the event, qualifying in this table'
    ),
    audits (
      unique_values(columns = id_qualifying_result),
      not_null(columns = id_qualifying_result)
    )
);

WITH base_table AS(
SELECT
  CONCAT(season, '-', round, '-', driver_id) AS id_qualifying_result,
  CONCAT(season, '-', round) AS id_race,
  season AS race_season,
  CAST(round AS INT) AS round_number,
  CAST(position AS INT) AS result,
  driver_id AS id_driver,
  constructor_id AS id_constructor,
  Q1 AS q1_best_time,
  Q2 AS q2_best_time,
  Q3 AS q3_best_time,
  event_type,
  TIMESTAMP(extraction_timestamp) AS ts_extracted
FROM
    custom_script.qualifying_result
)

SELECT
    id_qualifying_result,
    id_race,
    race_season,
    round_number,
    result,
    id_driver,
    id_constructor,
    q1_best_time,
    q2_best_time,
    q3_best_time,
    event_type
FROM
    base_table
QUALIFY ROW_NUMBER() OVER(PARTITION BY id_qualifying_result ORDER BY ts_extracted DESC) = 1