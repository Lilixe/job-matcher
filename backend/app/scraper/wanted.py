import requests
from .skill_extract import flatten_text

HEADERS = {"User-Agent": "Mozilla/5.0"}


def scrape_wanted_jobs(limit: int = 20) -> list[dict]:
    url = "https://www.wanted.co.kr/api/v4/jobs"

    params = {
        "country": "kr",
        "job_sort": "job.latest_order",
        "limit": limit,
        "offset": 0,
        "job_category_tag": "518"
    }

    r = requests.get(url, headers=HEADERS, params=params, timeout=10)
    r.raise_for_status()

    data = r.json()

    jobs = []
    for job in data.get("data", []):
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

    return jobs


def fetch_wanted_details(job_id: int) -> tuple[str, list[str]]:
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