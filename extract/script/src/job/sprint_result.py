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

def fetch_f1_sprint_results(season: str, round_number: str) -> Optional[Dict]:
    base_url = "http://ergast.com/api/f1"
    url = f"{base_url}/{season}/{round_number}/sprint.json"
    logging.info(
        "Fetching sprint results for Season: %s, Round: %s", season, round_number
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logging.info("Successfully fetched sprint results")
        return data
    except requests.exceptions.RequestException as e:
        logging.error("Error fetching the sprint results: %s", e)
        return None

def process_sprint_results(data: Dict) -> List[Dict]:
    logging.info("Processing sprint results data")
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
            if "SprintResults" in race:
                for result in race["SprintResults"]:
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
                            "event_type": "sprint",
                        }
                    )
                    processed_data.append(driver_result)
    return processed_data

def insert_results_to_bigquery(results: List[Dict], table_id: str) -> None:
    client = bigquery.Client()
    logging.info("Inserting sprint results into BigQuery")

    try:
        errors = client.insert_rows_json(table_id, results)
        if errors:
            logging.error(
                "Errors occurred while inserting data into BigQuery: %s", errors
            )
        else:
            logging.info("Successfully inserted sprint data into BigQuery")
    except Exception as e:
        logging.error("An error occurred while inserting data into BigQuery: %s", e)

def get_valid_seasons(seasons_env: Optional[str] = None) -> List[str]:
    """Get and validate seasons, ensuring only seasons >= 2021 are included."""
    if seasons_env:
        # Split the comma-separated string into a list and filter for >= 2021
        try:
            seasons = [
                season.strip()
                for season in seasons_env.split(",")
                if season.strip().isdigit() and int(season.strip()) >= 2021
            ]
            if seasons:
                logging.info("Using filtered seasons from environment variable: %s", seasons)
                return seasons
        except ValueError as e:
            logging.error("Error processing seasons from environment variable: %s", e)

    # Default seasons if not specified or if there was an error
    default_seasons = ["2021", "2022", "2023"]
    logging.info("Using default seasons: %s", default_seasons)
    return default_seasons

def main() -> None:
    # Get the table ID from environment variable
    table_id = os.getenv("SPRINT_TABLE_ID")
    if not table_id:
        logging.error("Environment variable SPRINT_TABLE_ID is not set.")
        return

    # Get and validate seasons
    seasons = get_valid_seasons(os.getenv("SEASONS"))

    # Define rounds to check
    rounds = [str(round) for round in range(1, 30)]

    # Process each season
    for season in seasons:
        logging.info("Processing season: %s", season)

        # Process each round for the current season
        for round_number in rounds:
            sprint_data = fetch_f1_sprint_results(season, round_number)

            # Check if sprint data exists and has valid structure
            if (sprint_data
                    and "MRData" in sprint_data
                    and "RaceTable" in sprint_data["MRData"]
                    and sprint_data["MRData"]["RaceTable"]["Races"]
            ):
                sprint_results = process_sprint_results(sprint_data)
                if sprint_results:
                    insert_results_to_bigquery(sprint_results, table_id)
                    logging.info(
                        "Successfully processed sprint data for Season: %s, Round: %s",
                        season,
                        round_number,
                    )
                else:
                    logging.info(
                        "No sprint results to insert for Season: %s, Round: %s",
                        season,
                        round_number,
                    )
            else:
                logging.debug(  # Changed to debug level to reduce log noise
                    "No sprint data available for Season: %s, Round: %s. Skipping.",
                    season,
                    round_number,
                )

            # Add delay to respect API rate limits
            time.sleep(1)  # 1 second delay between requests

if __name__ == "__main__":
    main()