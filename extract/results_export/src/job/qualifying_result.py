import requests
import logging
import os
import time
from typing import Dict, List, Optional
from google.cloud import bigquery

# Configure the logging module
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Function to fetch F1 qualifying results
def fetch_f1_qualifying_results(season: str, round_number: str) -> Optional[Dict]:
    base_url = "http://api.jolpi.ca/ergast/f1"
    url = f"{base_url}/{season}/{round_number}/qualifying"
    logging.info(
        "Fetching qualifying results for Season: %s, Round: %s", season, round_number
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logging.info("Successfully fetched qualifying results")
        return data
    except requests.exceptions.RequestException as e:
        logging.error("Error fetching the qualifying results: %s", e)
        return None


# Function to process and format qualifying results
def process_qualifying_results(data: Dict) -> List[Dict]:
    logging.info("Processing qualifying results data")
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
            if "QualifyingResults" in race:
                for result in race["QualifyingResults"]:
                    driver_result = race_info.copy()
                    driver_result.update(
                        {
                            "position": result["position"],
                            "driver_id": result["Driver"]["driverId"],
                            "constructor_id": result["Constructor"]["constructorId"],
                            "Q1": result.get("Q1"),
                            "Q2": result.get("Q2"),
                            "Q3": result.get("Q3"),
                            "event_type": "qualifying",
                        }
                    )
                    processed_data.append(driver_result)
    return processed_data


# Function to insert data into BigQuery
def insert_results_to_bigquery(results: List[Dict], table_id: str) -> None:
    client = bigquery.Client()
    logging.info("Inserting qualifying results into BigQuery")

    try:
        errors = client.insert_rows_json(table_id, results)
        if errors:
            logging.error(
                "Errors occurred while inserting data into BigQuery: %s", errors
            )
        else:
            logging.info("Successfully inserted qualifying data into BigQuery")
    except Exception as e:
        logging.error("An error occurred while inserting data into BigQuery: %s", e)


def main() -> None:
    # Get the table ID from environment variable
    table_id = os.getenv("QUALIFYING_TABLE_ID")
    if not table_id:
        logging.error("Environment variable QUALIFYING_RESULTS_TABLE_ID is not set.")
        return

    seasons = [str(year) for year in range(1990, 2026)]  # Example season range
    rounds = [str(round) for round in range(1, 30)]  # Example round range

    for season in seasons:
        for round_number in rounds:
            qualifying_data = fetch_f1_qualifying_results(season, round_number)
            if qualifying_data:
                qualifying_results = process_qualifying_results(qualifying_data)
                if qualifying_results:
                    insert_results_to_bigquery(qualifying_results, table_id)
                else:
                    logging.info(
                        "No qualifying results to insert for Season: %s, Round: %s",
                        season,
                        round_number,
                    )
                # Add delay to respect rate limits
                time.sleep(1)  # 1 seconds delay for burst limit (4 requests per second)


if __name__ == "__main__":
    main()
