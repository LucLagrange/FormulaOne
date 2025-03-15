MODEL (
    name marts.dim_race,
    kind FULL,
    cron '@daily',
    grain race_key,
    description 'Race dimension table containing all F1 races information',
    column_descriptions (
        id_race = 'Unique identifier for the race (combination of race name and season)',
        race_name = 'Official name of the race (e.g., Monaco Grand Prix)',
        dt_race = 'Date when the race took place',
        round_number = 'Sequential number of the race in the season calendar',
        race_season = 'Year in which the race took place',
        race_url = 'Wikipedia URL for the specific race',
        circuit_name = 'Name of the circuit where the race was held',
        circuit_url = 'Wikipedia URL for the circuit',
        country = 'Country where the circuit is located',
        latitude = 'Geographic latitude of the circuit location',
        longitude = 'Geographic longitude of the circuit location',
        locality = 'City or specific location where the circuit is situated'
    ),
    audits (
      unique_values(columns = id_race),
      not_null(columns = [id_race, circuit_name])
    )
);

SELECT
    races.id_race,
    races.race_name,
    races.dt_race,
    races.round_number,
    races.race_season,
    races.race_url,
    circuits.circuit_name,
    circuits.circuit_url,
    circuits.country,
    circuits.latitude,
    circuits.longitude,
    circuits.locality,
FROM staging.stg_races  AS races
LEFT JOIN staging.stg_circuits AS circuits ON races.id_circuit = circuits.id_circuit
