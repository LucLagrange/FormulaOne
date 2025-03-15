import requests
import logging
import time
import datetime
import os
from typing import Dict, List, Optional
from google.cloud import bigquery

# Configure the logging module
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Function to fetch F1 race results
def fetch_f1_results(season: str, round_number: str) -> Optional[Dict]:
    base_url = "http://api.jolpi.ca/ergast/f1"
    url = f"{base_url}/{season}/{round_number}/results"
    logging.info(
        "Fetching race results for Season: %s, Round: %s", season, round_number
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logging.info("Successfully fetched race results")
        return data
    except requests.exceptions.RequestException as e:
        logging.error("Error fetching the race results: %s", e)
        return None


# Function to process and format race results
def process_race_results(data: Dict) -> List[Dict]:
    logging.info("Processing race results data")
    processed_data: List[Dict] = []

    # Add extraction timestamp
    extraction_timestamp = datetime.datetime.utcnow().isoformat()

    if (
            "MRData" in data
            and "RaceTable" in data["MRData"]
            and "Races" in data["MRData"]["RaceTable"]
    ):
        races = data["MRData"]["RaceTable"]["Races"]
        for race in races:
            race_info = {
                "season": race["season"],
                "round": race["round"],
                "extraction_timestamp": extraction_timestamp,
            }
            for result in race["Results"]:
                driver_result = race_info.copy()
                driver_result.update(
                    {
                        "position": result["position"],
                        "points": result["points"],
                        "driver_id": result["Driver"]["driverId"],
                        "constructor_id": result["Constructor"]["constructorId"],
                        "grid": result["grid"],
                        "laps": result["laps"],
                        "status": result["status"],
                    }
                )
                processed_data.append(driver_result)
    return processed_data


# Function to insert data into BigQuery
def insert_results_to_bigquery(results: List[Dict], table_id: str) -> None:
    client = bigquery.Client()
    logging.info("Inserting results into BigQuery")

    try:
        errors = client.insert_rows_json(table_id, results)
        if errors:
            logging.error(
                "Errors occurred while inserting data into BigQuery: %s", errors
            )
        else:
            logging.info("Successfully inserted data into BigQuery")
    except Exception as e:
        logging.error("An error occurred while inserting data into BigQuery: %s", e)


def main() -> None:
    # Get the table ID from environment variable
    table_id = os.getenv("RESULTS_TABLE_ID")
    if not table_id:
        logging.error("Environment variable RESULTS_TABLE_ID is not set.")
        return

    # Get seasons from environment variable or use default
    seasons_env = os.getenv("SEASONS")
    if seasons_env:
        # Split the comma-separated string into a list
        seasons = [season.strip() for season in seasons_env.split(",")]
        logging.info("Using seasons from environment variable: %s", seasons)
    else:
        # Default seasons if not specified
        seasons = ["2021", "2022", "2023"]
        logging.info("Using default seasons: %s", seasons)

    rounds = [str(round) for round in range(1, 30)]  # Creates a list of rounds

    # Loop through each season
    for season in seasons:
        logging.info("Processing season: %s", season)

        # Then loop through each round for that season
        for round_number in rounds:
            data = fetch_f1_results(season, round_number)
            # Check if data exists for the round
            if (
                    data
                    and "MRData" in data
                    and "RaceTable" in data["MRData"]
                    and data["MRData"]["RaceTable"]["Races"]
            ):
                results = process_race_results(data)
                insert_results_to_bigquery(results, table_id)
            else:
                logging.info(
                    "No data available for Season: %s, Round: %s. Skipping.",
                    season,
                    round_number,
                )

            # Add delay to respect rate limits
            time.sleep(1)  # 1 second delay for burst limit (4 requests per second)


if __name__ == "__main__":
    main()