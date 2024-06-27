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


def query_pubmed(start_date: str, end_date: str) -> Optional[list[str]]:
    """
    Will query the pubmed database using a specified search criteria.

    Heavily inpired by example 3
    https://www.ncbi.nlm.nih.gov/books/NBK25498/#_chapter3_Application_3_Retrieving_large_

    Note that PubMed will not allow eFetch queries exceeding 10,000 articles. To query
    more than 10,000 values, look to eDirect command line utility.

    Params:
        start_date: begin search window here
        end_date: end search window here

    Returns:
        an XML element tree.
    """
    # Define query here
    search_term = f'("extracellular vesicles"[MeSH Terms] OR ("extracellular"[All Fields] AND "vesicles"[All Fields]) OR "extracellular vesicles"[All Fields] OR ("extracellular"[All Fields] AND "vesicle"[All Fields]) OR "extracellular vesicle"[All Fields]) AND {start_date}:{end_date}[Date - Publication] AND "English"[Language]'

    # Base url and fetch url
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    def fetch_detailed_info(web_env: str, query_key: str, retstart: int) -> str:
        """
        Helper method will fetch detailed XML data

        Params:
            query_key: the query key representing search criteria
            retstart: tells the database what index to start fetching from
            web_env: a hash representing an eSearch session, UID values are cached
            on a 'history' server, web_env references the session so we can fetch
            the relevant articles
        """
        query_string = {
            "db": "pubmed",
            "query_key": query_key,
            "WebEnv": web_env,
            "retstart": retstart,
            "retmax": 500,
            "rettype": "medline",
            "retmode": "xml",
        }
        response = requests.get(fetch_url, query_string)
        response.raise_for_status()
        return response.text

    try:
        # Perform the initial search request
        logging.info("Performing initial search request to PubMed.")

        query_string = {
            "db": "pubmed",
            "usehistory": "y",
            "term": search_term,
        }
        response = requests.get(base_url, query_string)
        response.raise_for_status()
        root = ET.fromstring(response.text)

        # Unpack the eSearch results
        total_count = int(root.find(".//Count").text or "0")
        web_env = root.find(".//WebEnv").text or "NA"
        query_key = root.find(".//QueryKey").text or "NA"

        logging.info(
            f"Total articles: {total_count}, WebEnv: {web_env}, QueryKey: {query_key}"
        )

        if total_count == 0:
            logging.warning("No articles found.")
            return None

        # Confirm with user before proceeding
        while True:
            std_in = input(f"Attempt to parse {total_count} articles? (y/n): ").lower()
            if std_in in ["y", "yes"]:
                break
            elif std_in in ["n", "no"]:
                logging.info("User interrupted.")
                return None
            print("Please enter 'y' or 'n'.")

        dois: list[str] = []

        # Fetch detailed information in batches
        for start in range(0, total_count, 500):
            logging.info(f"Fetching additional results starting at index {start}.")
            print(f"Fetching additional results starting at index {start}.")

            detailed_info = fetch_detailed_info(web_env, query_key, start)
            batch_tree = ET.fromstring(detailed_info)

            # Parse DOIs from XML data
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

    try:
        # Attempt to query pubmed for XML data
        dois = query_pubmed(start_date, end_date)

        if not dois:
            logging.error("No DOIs found.")
            print("No DOIs found.")
            return

        # Attempt to write DOIs to CSV
        output_dir = "output"
        write_dois_to_csv(dois, output_dir, "dois.csv")

        logging.info("Done.")
        print("Done.")

    except Exception as e:
        logging.error(f"An error occured: {e}")
        print(e)


if __name__ == "__main__":
    main()
