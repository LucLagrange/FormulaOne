The BigQuery schema for the tables are the following:

Races:
```json
[
    {
        "name": "season",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "round",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "position",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "points",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "driver_id",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "constructor_id",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "grid",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "laps",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "status",
        "type": "STRING",
        "mode": "NULLABLE"
    }
]
```

Sprint:
```json
[
    {
        "name": "season",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "round",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "position",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "points",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "driver_id",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "constructor_id",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "grid",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "laps",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "status",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "event_type",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "Indicates the result is from a sprint"
    }
]
```

Qualifying:
```json
[
    {
        "name": "season",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "round",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "position",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "driver_id",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "constructor_id",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "Q1",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "Q2",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "Q3",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "event_type",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "Indicates the result is from a qualifying session"
    }
]
```