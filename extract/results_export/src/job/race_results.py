import requests
import logging
import time
from google.cloud import bigquery

# Configure the logging module
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Function to fetch F1 race results
def fetch_f1_results(season, round_number):
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
def process_race_results(data):
    logging.info("Processing race results data")
    processed_data = []

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
                "race_name": race["raceName"],
                "circuit_id": race["Circuit"]["circuitId"],
                "location": race["Circuit"]["Location"]["locality"],
                "country": race["Circuit"]["Location"]["country"],
                "date": race["date"],
            }
            for result in race["Results"]:
                driver_result = race_info.copy()
                driver_result.update(
                    {
                        "position": result["position"],
                        "points": result["points"],
                        "driver_id": result["Driver"]["driverId"],
                        "constructor_id": result["Constructor"]["constructorId"],
                        "laps": result["laps"],
                        "status": result["status"],
                    }
                )
                processed_data.append(driver_result)
    return processed_data


# Function to insert data into BigQuery
def insert_results_to_bigquery(results, table_id):
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


def main():
    table_id = "formulaone-448910.custom_script.Results"
    seasons = [str(year) for year in range(1990, 1991)]
    rounds = [str(round) for round in range(1, 30)]

    for season in seasons:
        for round_number in rounds:
            data = fetch_f1_results(season, round_number)
            print(data)
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
            time.sleep(
                0.25
            )  # 0.25 seconds delay for burst limit (4 requests per second)


if __name__ == "__main__":
    main()
