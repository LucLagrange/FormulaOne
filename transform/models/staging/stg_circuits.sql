MODEL (
    name staging.stg_circuits,
    kind VIEW,
    cron '@daily',
    grain id_circuit,
    description 'The circuits used by the Formula One Championship',
    column_descriptions (
        id_circuit = 'Unique identifier for the circuit',
        circuit_name = 'Name of the circuit',
        circuit_url = 'Wikipedia URL of the circuit',
        country = 'Country in which the circuit is located',
        latitude = 'latitude of the circuit',
        longitude = 'longitude of the circuit',
        locality = 'Name of the locality associated to the circuit'
    ),
    audits (
       unique_values(columns = id_circuit),
       not_null(columns = id_circuit)
    )
);

SELECT
    CAST(circuitid AS STRING) AS id_circuit,
    CAST(circuitName AS STRING) AS circuit_name,
    CAST(url AS STRING) AS circuit_url,
    JSON_VALUE(location, '$.country') AS country,
    JSON_VALUE(location, '$.lat') AS latitude,
    JSON_VALUE(location, '$.locality') AS locality,
    JSON_VALUE(location, '$.long') AS longitude
FROM
    raw_data.Circuits