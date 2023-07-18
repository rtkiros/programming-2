from Bio import Entrez
import ssl
import multiprocessing as mp
import time

def fetch_article_information(email, api_key, article_id):
    """
    Fetches article information from PubMed.

    Prints the results and article references.
    """
    # to avoid certificate verification errors
    ssl._create_default_https_context = ssl._create_unverified_context

    # Set the email and API key
    Entrez.email = email
    Entrez.api_key = api_key

    # Query the PubMed database
    file = Entrez.elink(dbfrom="pubmed",
                        db="pmc",
                        LinkName="pubmed_pmc_refs",
                        id=article_id)

    results = Entrez.read(file)
    print(results)

    # Access article references
    references = [f'{link["Id"]}' for link in results[0]["LinkSetDb"][0]["Link"]]
    print(references)

    # Fetch article information
    handle = Entrez.efetch(db="pubmed",
                            id=article_id,
                            retmode="xml")
    print(handle.read())

# Setting up private information
email = 'r.t.kiros@st.hanze.nl'
api_key = '0201e348f8ceaf789e59357c27cc61fdb109'
article_id = '30049270'

fetch_article_information(email, api_key, article_id)


def download_article(pubmed_id, downloading_mode="p"):
    """
    Downloads the article with the given PubMed ID.

    Args:
        pubmed_id (str): PubMed article ID.
        downloading_mode (str, optional): Downloading mode identifier. Defaults to "p".

    Returns:
        not specific returning but the article will be saved in a xml file based on it's pubmed_id
    """
    handle = Entrez.efetch(db='pubmed',
                           id=pubmed_id,
                           retmode='xml',
                           api_key=api_key)
    xml_data = handle.read()
    handle.close()

    # Saving data to an xml file defined by its pubmed_id
    file_name = f'{downloading_mode}_{pubmed_id}.xml'
    with open(file_name, 'wb') as file:
        file.write(xml_data)


def get_references(amount, pubmed_id):
    """
    Retrieves the specified number of references for the given PubMed article ID.

    Args:
        amount (int): Number of references to retrieve.
        pubmed_id (str): PubMed article ID.

    Returns:
        list: List of PubMed IDs for the retrieved references.
    """
    file = Entrez.elink(dbfrom='pubmed',
                        db='pmc',
                        LinkName='pubmed_pmc_refs',
                        id=pubmed_id,
                        api_key=api_key)
    results = Entrez.read(file)
    file.close()
    references = [link['Id'] for link in results[0]['LinkSetDb'][0]['Link']]

    # Getting top n references based on the amount parameter
    return references[:amount]


def print_duration_time(start_time, end_time, execution_desc):
     """
    Prints the duration of an execution step.

    Args:
        start_time (float): Start time of the execution step.
        end_time (float): End time of the execution step.
        execution_desc (str): Description of the execution step.
    """
    print(f'Total time of {execution_desc} is: {end_time - start_time}')


def download_parallel(pubmed_id, amount):
     """
    Downloads articles in parallel using multiprocessing.

    Args:
        pubmed_id (str): PubMed article ID.
        amount (int): Number of articles to download.

    """
    start_time = time.time()
    references = get_references(amount, pubmed_id)
    end_time = time.time()
    print_duration_time(start_time, end_time, "getting references")

    # Creating a pool of workers to download the articles in parallel
    start_time = time.time()
    with mp.Pool() as pool:
        pool.map(download_article, references)
    end_time = time.time()
    print_duration_time(start_time, end_time, "downloading articles in parallel")


def download_sequential(pubmed_id, amount):
    """
    Downloads articles sequentially.

    Args:
        pubmed_id (str): PubMed article ID.
        amount (int): Number of articles to download.
    """
    references = get_references(amount, pubmed_id)

    # Downloading articles in sequential mode
    start_time = time.time()
    for reference in references:
        start_time_sub = time.time()
        download_article(reference, "s")
        end_time_sub = time.time()
        print_duration_time(start_time_sub, end_time_sub, f"downloading {reference}")
    end_time = time.time()
    print_duration_time(start_time, end_time, "downloading articles in series")


if __name__ == '__main__':
    # Call download functions
    pubmed_id = '29635200'  
    amount = 10  
    download_parallel(pubmed_id, amount)
    download_sequential(pubmed_id, amount)