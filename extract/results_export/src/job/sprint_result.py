import requests
import logging
import time
import os
from typing import Dict, List, Optional
from google.cloud import bigquery

# Configure the logging module
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Function to fetch F1 sprint results
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


# Function to process and format sprint results
def process_sprint_results(data: Dict) -> List[Dict]:
    logging.info("Processing sprint results data")
    processed_data: List[Dict] = []

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


# Function to insert data into BigQuery
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


def main() -> None:
    # Get the table ID from environment variable
    table_id = os.getenv("SPRINT_TABLE_ID")
    if not table_id:
        logging.error("Environment variable SPRINT_RESULTS_TABLE_ID is not set.")
        return

    seasons = [str(year) for year in range(1990, 2026)]  # Example season range
    rounds = [str(round) for round in range(1, 30)]  # Example round range

    for season in seasons:
        for round_number in rounds:
            sprint_data = fetch_f1_sprint_results(season, round_number)
            if sprint_data:
                sprint_results = process_sprint_results(sprint_data)
                if sprint_results:
                    insert_results_to_bigquery(sprint_results, table_id)
                else:
                    logging.info(
                        "No sprint results to insert for Season: %s, Round: %s",
                        season,
                        round_number,
                    )

                time.sleep(8)  # 1 seconds delay for burst limit (4 requests per second)


if __name__ == "__main__":
    main()
