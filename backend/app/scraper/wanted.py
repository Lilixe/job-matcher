import requests
from .skill_extract import flatten_text

HEADERS = {"User-Agent": "Mozilla/5.0"}


def scrape_wanted_jobs(limit: int = 100) -> list[dict]:
    """
    Scrape job listings from Wanted.co.kr for software development positions.
    
    Fetches recent job postings filtered by the software development category (tag 518).
    
    Args:
        limit (int, optional): Maximum number of job listings to retrieve. Defaults to 30.
    
    Returns:
        list[dict]: List of job dictionaries with keys:
            - id (int): Unique job identifier on Wanted
            - title (str): Job position title
            - company (str): Company name
            - url (str): Direct link to the job posting
    
    Raises:
        requests.HTTPError: If the API request fails.
        requests.Timeout: If the request exceeds 10 seconds.
    
    Example:
        >>> jobs = scrape_wanted_jobs(limit=5)
        >>> print(jobs[0]['title'])
    """
    url = "https://www.wanted.co.kr/api/v4/jobs"
    jobs = []
    offset = 0
    page_limit = 50 
    
    while len(jobs) < limit:
        params = {
            "country": "kr",
            "job_sort": "job.latest_order",
            "limit": page_limit,
            "offset": offset,
            "job_category_tag": "518"
        }

        r = requests.get(url, headers=HEADERS, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        page_jobs = data.get("data", [])
        if not page_jobs:
            break

        for job in page_jobs:
            category_tags = job.get("category_tags", [])
            if not any(t.get("parent_id") == 518 for t in category_tags):
                continue

            job_id = job.get("id")

            jobs.append({
                "id": job_id,
                "title": job.get("position", "Unknown"),
                "company": job.get("company", {}).get("name", "Unknown"),
                "url": f"https://www.wanted.co.kr/wd/{job_id}"
            })

            if len(jobs) >= limit:
                break

        offset += page_limit

    return jobs


def fetch_wanted_details(job_id: int) -> tuple[str, list[str]]:
    """
    Fetch detailed information and skills for a specific job posting.
    
    Retrieves the full job description and extracts skill tags from a Wanted job listing.
    
    Args:
        job_id (int): The unique identifier of the job on Wanted.co.kr.
    
    Returns:
        tuple[str, list[str]]: A tuple containing:
            - description (str): Flattened job description text
            - skill_tags (list[str]): List of required skills in lowercase
    
    Raises:
        requests.HTTPError: If the API request fails.
        requests.Timeout: If the request exceeds 10 seconds.
    
    Example:
        >>> description, skills = fetch_wanted_details(123456)
        >>> print(skills)
        ['python', 'fastapi', 'sql']
    """
    url = f"https://www.wanted.co.kr/api/v4/jobs/{job_id}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": f"https://www.wanted.co.kr/wd/{job_id}",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()

    data = r.json()
    job = data.get("job", {})

    # raw detail (string/dict)
    detail = job.get("detail", "")
    description = flatten_text(detail)

    tags = job.get("skill_tags", [])
    skill_tags = [t["title"].lower() for t in tags if isinstance(t, dict) and "title" in t]

    return description, skill_tags