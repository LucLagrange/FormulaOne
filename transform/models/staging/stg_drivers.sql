MODEL (
    name staging.stg_drivers,
    kind VIEW,
    cron '@daily',
    grain id_driver,
    description 'The drivers that race in the Formula One Championship',
    column_descriptions (
        id_driver = 'Unique identifier for the driver',
        driver_url = 'URL associated with the driver',
        driver_code = 'Code representing the driver',
        first_name = 'Drivers first name',
        last_name = 'Drivers last name',
        dt_birth = 'Drivers date of birth',
        nationality = 'Drivers nationality',
        driver_number = 'Drivers permanent number'
    ),
    audits (
       unique_values(columns = id_driver),
       not_null(columns = id_driver)
    )
);

SELECT
  CAST(driverId AS STRING) AS id_driver,
  url AS driver_url,
  code AS driver_code,
  givenName AS first_name,
  familyName AS last_name,
  CAST(dateOfBirth AS DATE) AS dt_birth,
  nationality,
  permanentNumber AS driver_number
FROM
    raw_data.Drivers