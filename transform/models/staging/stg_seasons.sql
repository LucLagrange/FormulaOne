MODEL (
    name staging.stg_seasons,
    kind VIEW,
    cron '@daily',
    grain id_season,
    description 'The seasons of the Formula One Championship',
    column_descriptions (
        id_season = 'Unique identifier for the season',
        season_url = "Wikipedia URL for the season"
    ),
    audits (
       unique_values(columns = id_season),
       not_null(columns = id_season)
    )
);

SELECT
  CAST(season AS STRING) AS id_season,
  url AS season_url
FROM
    raw_data.Seasons