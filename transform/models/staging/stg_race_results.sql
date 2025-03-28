MODEL (
    name staging.stg_race_results,
    kind VIEW,
    cron '@daily',
    grain id_race_result,
    description 'The race results for each driver, at each season round',
    column_descriptions (
        id_race_result = 'Unique identifier for the race result, combining season, round, and driver ID',
        id_race = 'Unique identifier for the race',
        id_driver = 'Unique identifier for the driver',
        id_constructor = 'Unique identifier for the constructor',
        race_season = 'The season in which the race took place',
        round_number = 'The round number of the season',
        result = 'The position the driver finished in the race',
        grid_position = 'The starting grid position of the driver',
        points_awarded = 'Points awarded to the driver based on their finishing position',
        laps_completed = 'Total number of laps completed by the driver',
        status = 'The status of the driver at the end of the race (e.g., Finished, Retired, etc.)',
        event_type = 'The type of the event, race in this table'
    ),
    audits (
      unique_values(columns = id_race_result),
      not_null(columns = id_race_result)
    )
);

WITH base_table AS (
SELECT
  CONCAT(season, '-', round, '-', driver_id) AS id_race_result,
  driver_id AS id_driver,
  constructor_id AS id_constructor,
  CONCAT(season, '-', round) AS id_race,
  season AS race_season,
  CAST(round AS INT) AS round_number,
  CAST(position AS INT) AS result,
  CAST(grid AS INT) AS grid_position,
  CAST(points AS FLOAT64) AS points_awarded,
  CAST(laps AS INT) AS laps_completed,
  status,
  'race' AS event_type,
  TIMESTAMP(extraction_timestamp) AS ts_extracted
FROM
    custom_script.race_result
)

SELECT
    id_race_result,
    id_driver,
    id_constructor,
    id_race,
    race_season,
    round_number,
    result,
    grid_position,
    points_awarded,
    laps_completed
    status,
    event_type
FROM
    base_table
QUALIFY ROW_NUMBER() OVER(PARTITION BY id_race_result ORDER BY ts_extracted DESC) = 1