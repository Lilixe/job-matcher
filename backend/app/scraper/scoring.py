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


def compute_score(job_skills: list[str], user_skills: list[str]) -> float:
    """
    Calculate the job match score based on skill overlap.
    
    Computes the percentage of job required skills that match with user skills.
    The score represents what fraction of the job's required skills the user possesses.
    
    Args:
        job_skills (list[str]): List of skills required for the job.
        user_skills (list[str]): List of skills the user possesses.
    
    Returns:
        float: Match score as a percentage (0.0 - 100.0). Returns 0.0 if job_skills is empty.
    
    Example:
        >>> compute_score(["python", "fastapi", "sql"], ["python", "sql"])
        66.67
    """
    job_set = set(job_skills)
    user_set = set(user_skills)

    if not job_set:
        return 0.0

    match = job_set.intersection(user_set)
    return round((len(match) / len(job_set)) * 100, 2)
