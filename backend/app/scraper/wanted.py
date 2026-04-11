import requests
import re

HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_wanted_jobs(limit: int = 20) -> list[dict]:
    url = "https://www.wanted.co.kr/api/v4/jobs"

    params = {
        "country": "kr",
        "job_sort": "job.latest_order",
        "limit": limit,
        "offset": 0,

        # Software Engineering category tag
        "job_category_tag": "518"  
    }

    r = requests.get(url, headers=HEADERS, params=params, timeout=10)
    r.raise_for_status()

    data = r.json()
    #print("TOP LEVEL KEYS:", data.keys())
    #print("JOB KEYS:", data.get("job", {}).keys())
    #print("JOB RAW:", data.get("job", {}))
    #raise Exception("job")

    jobs = []
    for job in data.get("data", []):
        category_tags = job.get("category_tags", [])
        if not any(t.get("parent_id") == 518 for t in category_tags):
            continue
        
        job_id = job.get("id")
        
        print("TITLE:", job.get("position"))
        print("CATEGORY TAGS:", job.get("category_tags"))
        print("SKILL TAGS:", job.get("skill_tags"))
        print("----------")

        jobs.append({
            "id": job_id,
            "title": job.get("position", "Unknown"),
            "company": job.get("company", {}).get("name", "Unknown"),
            "url": f"https://www.wanted.co.kr/wd/{job_id}"
        })

    return jobs


import requests
import re

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

    # ---- DESCRIPTION ----
    detail = job.get("detail", "")
    parts = []

    if isinstance(detail, dict):
        for v in detail.values():
            if isinstance(v, str):
                parts.append(v)

    elif isinstance(detail, str):
        parts.append(detail)

    description = " ".join(parts)

    description = re.sub(r"<[^>]+>", " ", description)
    description = re.sub(r"\s+", " ", description).strip()

    # ---- SKILL TAGS ----
    tags = job.get("skill_tags", [])
    skill_tags = [t["title"].lower() for t in tags if isinstance(t, dict) and "title" in t]

    return description, skill_tags