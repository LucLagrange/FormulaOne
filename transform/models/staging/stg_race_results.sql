MODEL (
    name staging.stg_race_results,
    kind VIEW,
    cron '@daily',
    grain id_race_result,
    description 'The race results for each driver, at each season round',
    column_descriptions (
        id_race_result = 'Unique identifier for the race result, combining season, round, and driver ID',
        id_driver = 'Unique identifier for the driver',
        id_constructor = 'Unique identifier for the constructor',
        race_season = 'The season in which the race took place',
        round_number = 'The round number of the season',
        result = 'The position the driver finished in the race',
        grid_position = 'The starting grid position of the driver',
        points_awarded = 'Points awarded to the driver based on their finishing position',
        laps_completed = 'Total number of laps completed by the driver',
        status = 'The status of the driver at the end of the race (e.g., Finished, Retired, etc.)'
    )
);

SELECT
  CONCAT(season, '-', round, '-', driver_id) AS id_race_result,
  driver_id AS id_driver,
  constructor_id AS id_constructor,
  season AS race_season,
  CAST(round AS INT) AS round_number,
  CAST(position AS INT) AS result,
  CAST(grid AS INT) AS grid_position,
  CAST(points AS INT) AS points_awarded,
  CAST(laps AS INT) AS laps_completed,
  status
FROM
    custom_script.race_result