MODEL (
    name warehouse.fct_race_results,
    kind FULL,
    cron '@daily',
    grain id_race_result,
    description 'Fact table containing comprehensive F1 race performance including qualifying, sprint and main race results',
    column_descriptions (
        id_race_result = 'Unique identifier for the race result record',
        id_driver = 'Identifier for the driver who participated in the race',
        id_constructor = 'Identifier for the constructor/team the driver represented',
        id_race = "Identifier for the race",
        race_season = 'Year in which the race took place',
        round_number = 'Sequential number of the race in the season calendar',
        qualifying_result = 'Final position achieved in qualifying',
        q1_best_time = 'Best lap time achieved in Q1 session',
        q2_best_time = 'Best lap time achieved in Q2 session',
        q3_best_time = 'Best lap time achieved in Q3 session',
        race_result = 'Final position achieved in the main race',
        race_grid_position = 'Starting grid position for the main race',
        race_points_awarded = 'Championship points awarded for the main race result',
        race_status = 'Status at the end of the race (e.g., Finished, DNF, DSQ)',
        sprint_result = 'Final position achieved in the sprint race, if applicable',
        sprint_grid_position = 'Starting grid position for the sprint race, if applicable',
        sprints_points_awarded = 'Championship points awarded for the sprint race result, if applicable',
        sprint_status = 'Status at the end of the sprint race (e.g., Finished, DNF, DSQ), if applicable',
        total_points_awarded = "The total number of points awarded to the drivers"
    ),
    audits (
      unique_values(columns = id_race_result),
      not_null(columns = [id_race_result, id_driver, id_constructor, race_season, round_number])
    )
);

SELECT
  races.id_race_result,
  races.id_driver,
  races.id_constructor,
  races.id_race,
  races.race_season,
  races.round_number,
  qualifying.result AS qualifying_result,
  qualifying.q1_best_time,
  qualifying.q2_best_time,
  qualifying.q3_best_time,
  races.result AS race_result,
  races.grid_position AS race_grid_position,
  races.points_awarded AS race_points_awarded,
  races.status AS race_status,
  sprints.result AS sprint_result,
  sprints.grid_position AS sprint_grid_position,
  sprints.points_awarded AS sprints_points_awarded,
  sprints.status AS sprint_status,
  SAFE_ADD(races.points_awarded, COALESCE(sprints.points_awarded, 0)) AS total_points_awarded,
FROM
  staging.stg_race_results AS races
LEFT JOIN
  staging.stg_sprint_results AS sprints
ON races.id_race_result = sprints.id_race_result
LEFT JOIN
  staging.stg_qualifying_results AS qualifying
ON races.id_race_result = qualifying.id_qualifying_result