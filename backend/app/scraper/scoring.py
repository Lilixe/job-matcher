# MY_SKILLS = [
#     # Programming Languages
#     "python", "java", "c", "c++", "c#", "javascript", "scala",

#     # Web / Backend Frameworks
#     "fastapi",

#     # Mobile / App
#     "flutter",

#     # Databases
#     "sql", "mysql", "postgresql", "sqlite",

#     # Data / ML
#     "pandas", "numpy", "scikit-learn", "sklearn",
#     "tensorflow", "pytorch", "keras",
#     "machine learning", "deep learning", "nlp", "computer vision",
#     "opencv", "huggingface", "transformer", "llm", "vector database",

#     # Cloud / DevOps
#     "aws",

#     # Tools / OS
#     "linux", "bash", "git", "github", "gitlab",

#     # Game / Graphics (your resume relevant)
#     "unity", "unreal", "opengl",
#     "shader", "3d", "game engine",

#     # Networking / API
#     "rest", "rest api", "graphql",

#     # Misc / Software Engineering keywords
#     "testing", "pytest", "unit testing",
#     "agile", "scrum"
# ]

# HIGH_WEIGHT = {
#     "python", "java", "c++", "c#", "javascript", "typescript",
#     "sql", "fastapi", "django", "flask",
#     "docker", "kubernetes", "aws", "gcp",
#     "pytorch", "tensorflow", "machine learning", "deep learning",
#     "nlp", "computer vision"
# }

# LOW_WEIGHT = {
#     "jira", "confluence", "scrum", "agile", "testing", "unit testing"
# }


def normalize_skills(skills):
    """Normalize a job or user skill list for comparison.

    Args:
        skills (str | Iterable[str] | None): A comma-separated string or an iterable
            of skill names.

    Returns:
        list[str]: A normalized list of skills in lowercase with whitespace stripped.
            If no skills are provided, returns an empty list.
    """
    if not skills:
        return []

    if isinstance(skills, str):
        return [s.strip().lower() for s in skills.split(",") if s.strip()]

    return [s.strip().lower() for s in skills]


def compute_score(job_skills, user_skills) -> float:
    """Compute a match score between job skills and user skills.

    The score is the percentage of job skills that are found in the user skills.
    Both inputs are normalized before comparison.

    Args:
        job_skills (str | Iterable[str] | None): The required skills for the job.
        user_skills (str | Iterable[str] | None): The user's skills.

    Returns:
        float: The percentage of job skills matched by the user skills, rounded
            to two decimals. Returns 0.0 if the job skill list is empty.
    """
    job_list = normalize_skills(job_skills)
    user_list = normalize_skills(user_skills)

    job_set = set(job_list)
    user_set = set(user_list)

    if not job_set:
        return 0.0

    match = job_set.intersection(user_set)
    return round((len(match) / len(job_set)) * 100, 2)