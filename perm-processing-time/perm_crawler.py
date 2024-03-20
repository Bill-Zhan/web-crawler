"""
Script to web crawl perm processing time
"""

import requests
from bs4 import BeautifulSoup

def crawl_processing_time() -> str:
    # URL of the page to scrape
    url = "https://flag.dol.gov/processingtimes"

    # Sending a GET request to the website
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the content of the request with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for the "PERM Processing Times" section by searching for the specific <strong> tag
        perm_section = soup.find('strong', text="PERM Processing Times")
        
        if perm_section:
            # Find the closest table following the identified section
            perm_table = perm_section.find_parent('table')
            if perm_table:
                # Find the row with "Analyst Review"
                analyst_review_row = perm_table.find('td', text="Analyst Review")
                if analyst_review_row:
                    # The date is in the next <td>
                    date_td = analyst_review_row.find_next_sibling('td')
                    if date_td:
                        extracted_data = date_td.text.strip()
                        return extracted_data
                    else:
                        return "Date for Analyst Review not found."
                else:
                    return "Analyst Review row not found."
            else:
                return "PERM Processing Times table not found."
        else:
            return "PERM Processing Times section not found."
    else:
        return f"Failed to retrieve data, status code: {response.status_code}"