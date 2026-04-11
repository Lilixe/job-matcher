MY_SKILLS = [
    # Programming Languages
    "python", "java", "c", "c++", "c#", "javascript", "scala",

    # Web / Backend Frameworks
    "fastapi",

    # Mobile / App
    "flutter",

    # Databases
    "sql", "mysql", "postgresql", "sqlite",

    # Data / ML
    "pandas", "numpy", "scikit-learn", "sklearn",
    "tensorflow", "pytorch", "keras",
    "machine learning", "deep learning", "nlp", "computer vision",
    "opencv", "huggingface", "transformer", "llm", "vector database",

    # Cloud / DevOps
    "aws",

    # Tools / OS
    "linux", "bash", "git", "github", "gitlab",

    # Game / Graphics (your resume relevant)
    "unity", "unreal", "opengl",
    "shader", "3d", "game engine",

    # Networking / API
    "rest", "rest api", "graphql",

    # Misc / Software Engineering keywords
    "testing", "pytest", "unit testing",
    "agile", "scrum"
]

HIGH_WEIGHT = {
    "python", "java", "c++", "c#", "javascript", "typescript",
    "sql", "fastapi", "django", "flask",
    "docker", "kubernetes", "aws", "gcp",
    "pytorch", "tensorflow", "machine learning", "deep learning",
    "nlp", "computer vision"
}

LOW_WEIGHT = {
    "jira", "confluence", "scrum", "agile", "testing", "unit testing"
}


def compute_score(job_skills: list[str]) -> float:
    if not job_skills:
        return 0.0

    total_weight = 0
    matched_weight = 0

    for sk in job_skills:
        sk = sk.lower()

        if sk in HIGH_WEIGHT:
            w = 3
        elif sk in LOW_WEIGHT:
            w = 1
        else:
            w = 2

        total_weight += w
        if sk in MY_SKILLS:
            matched_weight += w
    
    score = (matched_weight / total_weight) * 100

    # penalty if too few skills detected
    if len(job_skills) < 4:
        score *= 0.5

    return score