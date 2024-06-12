import requests  # type: ignore
import xml.etree.ElementTree as ET
import csv
import logging
import os
from typing import Optional


# Set up logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, "pubmed_query.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s",
)


def query_pubmed(
    start_date: str, end_date: str, max_results: str
) -> Optional[list[str]]:
    """
    Will query the pubmed database using a specified search criteria.

    Params:
        start_date: begin search window here
        end_date: end search window here
        max_results: the max number or search results to return

    Returns:
        an XML element tree.
    """
    # Define query here
    search_term = f'("extracellular vesicles"[MeSH Terms] OR ("extracellular"[All Fields] AND "vesicles"[All Fields]) OR "extracellular vesicles"[All Fields] OR ("extracellular"[All Fields] AND "vesicle"[All Fields]) OR "extracellular vesicle"[All Fields]) AND {start_date}:{end_date}[Date - Publication] AND "English"[Language]'

    # Base url and search params
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    def fetch_ids(retstart: int):
        """Helper method gets the ids of search term"""
        query_string = {
            "db": "pubmed",
            "term": search_term,
            "retmax": max_results,
            "retstart": retstart,
        }
        response = requests.get(base_url, query_string)
        response.raise_for_status()
        return response.text

    def fetch_detailed_info(id_batch: list[str]) -> str:
        """Helper method will fetch detailed XML data"""
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        query_string = {
            "db": "pubmed",
            "id": ",".join(id_batch),
            "rettype": "medline",
            "retmode": "xml",
        }
        response = requests.get(fetch_url, query_string)
        response.raise_for_status()
        return response.text

    try:
        # Perform the initial search request
        logging.info("Performing initial search request to PubMed.")
        initial_results = fetch_ids(0)
        root = ET.fromstring(initial_results)
        total_count = int(root.find(".//Count").text)

        # Confirm with user before proceeding
        while True:
            std_in = input(f"Attempt to parse {total_count} articles? (y/n): ").lower()
            if std_in in ["y", "yes"]:
                break
            elif std_in in ["n", "no"]:
                logging.info("User interupted.")
                return None

            print("Please enter 'y' or 'n'.")

        id_list: list[str] = []

        # Collect IDs from the initial batch
        for id_elem in root.findall(".//Id"):
            if id_elem.text:
                id_list.append(id_elem.text)

        # If more results are available, paginate, we need all the IDs
        for start in range(10000, total_count, 10000):
            logging.info(f"Fetching additional results starting at {start}.")
            paginated_results = fetch_ids(start)
            paginated_root = ET.fromstring(paginated_results)
            for id_elem in paginated_root.findall(".//Id"):
                if id_elem.text:
                    id_list.append(id_elem.text)

        if not id_list:
            logging.warning("No article IDs found.")
            return None

        # Fetch detailed information in batches and parse DOIs
        dois: list[str] = []
        batch_size = 300  # Adjust this size as needed to avoid the URL length limit

        for i in range(0, len(id_list), batch_size):
            print(f"Fetching detailed information for batch starting at index {i}.")

            id_batch = id_list[i : i + batch_size]
            logging.info(
                f"Fetching detailed information for batch starting at index {i}."
            )
            detailed_info = fetch_detailed_info(id_batch)
            batch_tree = ET.fromstring(detailed_info)

            # We build up one big list of DOIs and
            # write that to CSV in one go.

            dois.extend(parse_dois_from_tree(batch_tree))

        return dois

    except (requests.RequestException, ET.ParseError) as e:
        raise Exception(e)
        return None


def parse_dois_from_tree(tree: ET.Element) -> list[str]:
    """
    Parses DOIs from an XML element tree.

    Params:
        tree: an XML element tree

    Returns:
        a list of DOIs
    """
    dois: list[str] = []

    for article in tree.findall(".//PubmedArticle"):
        for article_id in article.findall(".//ArticleId"):
            if article_id.attrib.get("IdType") == "doi":
                doi = article_id.text or "N/A"
                dois.append(doi)
                break

    return dois


def write_dois_to_csv(dois: list[str], output_dir: str, filename: str):
    """
    Writes the list of DOIs to a CSV file in the specified directory.

    Params:
        dois: List of DOIs to be written to the file
        output_dir: Directory where the CSV file will be saved
        filename: Name of the CSV file
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    try:
        with open(filepath, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["DOI"])
            for doi in dois:
                writer.writerow([doi])

        logging.info(f"DOIs have been written to {filepath}")
    except Exception as e:
        raise Exception(e)


def main():
    logging.info("Running script: main.py")

    # Define the search parameters
    start_date = "2018/01/01"
    end_date = "2022/12/31"

    # 10,000 is the max allowed value here,
    # if you want more you'll have to paginate.

    max_results = 10000

    try:
        # Attempt to query pubmed for XML data
        dois = query_pubmed(start_date, end_date, max_results)

        if not dois:
            logging.error("No DOIs found.")
            print("No DOIs found.")

        # Attempt to write DOIs to CSV
        output_dir = "output"
        write_dois_to_csv(dois, output_dir, "dois.csv")

        # Okay cool, let's plot a chart

        logging.info("Done.\n")
        print("Done.")

    except Exception as e:
        logging.error(f"An error occured: {e}\n")
        print(e)


if __name__ == "__main__":
    main()
