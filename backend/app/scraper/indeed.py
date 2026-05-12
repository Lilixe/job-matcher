import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

HEADERS = {"User-Agent": "Mozilla/5.0"}

BASE_URL = "https://kr.indeed.com"


def scrape_indeed_jobs(query: str = "software", limit: int = 100) -> list[dict]:
    """
    Scrape job listings from Indeed Korea.

    Args:
        query (str): Search keyword (e.g. "backend", "python", "data engineer")
        limit (int): Maximum number of jobs to return

    Returns:
        list[dict]: List of job dictionaries with keys:
            - jobkey (str)
            - title (str)
            - company (str)
            - location (str)
            - url (str)
    """
    jobs = []
    start = 0
    page_size = 10  # Indeed uses pagination with start=0,10,20,...

    while len(jobs) < limit:
        params = {
            "q": query,
            "l": "대한민국",
            "start": start
        }

        r = requests.get(f"{BASE_URL}/jobs", headers=HEADERS, params=params, timeout=10)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        job_cards = soup.select("a.tapItem")
        if not job_cards:
            break

        for card in job_cards:
            jobkey = card.get("data-jk")
            if not jobkey:
                continue

            title = card.select_one("h2.jobTitle span")
            company = card.select_one("span.companyName")
            location = card.select_one("div.companyLocation")

            title_text = title.get_text(strip=True) if title else "Unknown"
            company_text = company.get_text(strip=True) if company else "Unknown"
            location_text = location.get_text(strip=True) if location else "Unknown"

            job_url = urljoin(BASE_URL, f"/viewjob?jk={jobkey}")

            jobs.append({
                "jobkey": jobkey,
                "title": title_text,
                "company": company_text,
                "location": location_text,
                "url": job_url
            })

            if len(jobs) >= limit:
                break

        start += page_size

    return jobs


def fetch_indeed_details(jobkey: str) -> str :
    """
    Fetch job description + extract skills from an Indeed job page.

    Args:
        jobkey (str): Indeed job key (jk)

    Returns:
        tuple[str, list[str]]:
            - description (str)
            - skill_tags (list[str])
    """
    url = f"{BASE_URL}/viewjob?jk={jobkey}"

    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    desc_div = soup.select_one("#jobDescriptionText")
    description = desc_div.get_text(separator="\n", strip=True) if desc_div else ""

    # VERY BASIC skill extraction (replace with your own NLP/skill_extract module)

    return description
