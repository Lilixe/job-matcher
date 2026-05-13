import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .skill_extract import flatten_text

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

BASE_URL = "https://www.saramin.co.kr"


def scrape_saramin_jobs(limit: int = 50, keyword: str = "개발자") -> list[dict]:
    """
    Scrape job listings from Saramin.

    Args:
        limit (int): Maximum number of jobs to return
        keyword (str): Search keyword (default: 개발자)

    Returns:
        list[dict]: List of job dictionaries with keys:
            - id (str)
            - title (str)
            - company (str)
            - url (str)
    """
    jobs = []
    page = 1
    page_size = 50

    while len(jobs) < limit:
        params = {
            "searchType": "search",
            "searchword": keyword,
            "recruitPage": page,
            "recruitSort": "relation",
            "recruitPageCount": page_size,
        }

        r = requests.get(f"{BASE_URL}/zf_user/search/recruit", headers=HEADERS, params=params, timeout=10)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        cards = soup.select("div.item_recruit")
        if not cards:
            break

        for card in cards:
            link = card.select_one("h2.job_tit a")
            company_el = card.select_one("div.area_corp strong.corp_name a")

            if not link:
                continue

            title = link.get_text(strip=True)
            company = company_el.get_text(strip=True) if company_el else "Unknown"

            href = link.get("href", "")
            full_url = urljoin(BASE_URL, href) # type: ignore

            # extract job id from url (rec_idx=xxxxx)
            job_id = None
            if "rec_idx=" in href: # type: ignore
                job_id = href.split("rec_idx=")[-1].split("&")[0] # type: ignore

            if not job_id:
                continue

            jobs.append({
                "id": job_id,
                "title": title,
                "company": company,
                "url": full_url
            })

            if len(jobs) >= limit:
                break

        page += 1

    return jobs


def fetch_saramin_details(job_id: str) -> str:
    """
    Fetch job description from Saramin job posting.

    Args:
        job_id (str): Saramin job rec_idx

    Returns:
        str: Flattened job description
    """
    url = f"{BASE_URL}/zf_user/jobs/relay/view?rec_idx={job_id}"

    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    desc_div = soup.select_one("div.user_content")
    if not desc_div:
        desc_div = soup.select_one("div.wrap_jv_cont")

    description = desc_div.get_text(separator="\n", strip=True) if desc_div else ""
    return flatten_text(description)