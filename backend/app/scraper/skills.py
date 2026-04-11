SKILLS = [
    # Programming Languages
    "python", "java", "c", "c++", "c#", "javascript", "typescript",
    "go", "golang", "rust", "kotlin", "swift", "php", "ruby", "scala",

    # Web / Backend Frameworks
    "fastapi", "flask", "django",
    "spring", "spring boot", "node", "node.js", "express",
    "asp.net", ".net",

    # Frontend Frameworks
    "react", "vue", "angular", "next.js", "nuxt",
    "svelte",

    # Mobile / App
    "flutter", "dart", "react native", "android", "ios",

    # Databases
    "sql", "mysql", "postgresql", "sqlite",
    "mongodb", "redis", "elasticsearch",

    # Data / ML
    "pandas", "numpy", "scikit-learn", "sklearn",
    "tensorflow", "pytorch", "keras",
    "machine learning", "deep learning", "nlp", "computer vision",
    "opencv", "huggingface", "transformer", "llm",
    "rag", "vector database", "faiss",

    # Data Engineering / Big Data
    "spark", "pyspark", "hadoop", "kafka", "airflow", "etl",

    # Cloud / DevOps
    "aws", "gcp", "google cloud", "azure",
    "docker", "kubernetes", "terraform",
    "ci/cd", "github actions", "jenkins",

    # Tools / OS
    "linux", "bash", "git", "github", "gitlab",
    "jira", "confluence",

    # Game / Graphics (your resume relevant)
    "unity", "unreal", "opengl", "vulkan",
    "shader", "3d", "game engine",

    # Networking / API
    "rest", "rest api", "graphql",
    "microservices", "msa",

    # Misc / Software Engineering keywords
    "oop", "design patterns",
    "testing", "pytest", "unit testing",
    "agile", "scrum"
]

SKILL_PATTERNS = {
    # --- Programming Languages ---
    "python": [r"\bpython\b", r"파이썬"],
    "java": [r"\bjava\b", r"자바"],
    "c": [r"\bc\b", r"\bc language\b"],
    "c++": [r"\bc\+\+\b", r"cpp", r"\bc plus plus\b"],
    "c#": [r"\bc#\b", r"\bcsharp\b", r"\bc sharp\b"],
    "javascript": [r"\bjavascript\b", r"\bjs\b", r"자바스크립트"],
    "typescript": [r"\btypescript\b", r"\bts\b"],
    "go": [r"\bgo\b", r"\bgolang\b"],
    "rust": [r"\brust\b"],
    "kotlin": [r"\bkotlin\b"],
    "swift": [r"\bswift\b"],
    "php": [r"\bphp\b"],
    "ruby": [r"\bruby\b"],
    "scala": [r"\bscala\b"],

    # --- Backend / Web Frameworks ---
    "fastapi": [r"\bfastapi\b"],
    "flask": [r"\bflask\b"],
    "django": [r"\bdjango\b"],
    "spring": [r"\bspring\b", r"\bspring framework\b"],
    "spring boot": [r"\bspring boot\b", r"\bspringboot\b"],
    "node.js": [r"\bnode\.?js\b", r"\bnodejs\b"],
    "express": [r"\bexpress\b", r"\bexpress\.js\b"],
    ".net": [r"\.net\b", r"\bdotnet\b"],
    "asp.net": [r"\basp\.net\b", r"\baspx\b"],

    # --- Frontend ---
    "react": [r"\breact\b", r"\breact\.js\b"],
    "vue": [r"\bvue\b", r"\bvue\.js\b"],
    "angular": [r"\bangular\b"],
    "next.js": [r"\bnext\.?js\b", r"\bnextjs\b"],
    "nuxt": [r"\bnuxt\b", r"\bnuxt\.js\b"],
    "svelte": [r"\bsvelte\b"],

    # --- Mobile ---
    "flutter": [r"\bflutter\b"],
    "dart": [r"\bdart\b"],
    "react native": [r"\breact native\b"],
    "android": [r"\bandroid\b"],
    "ios": [r"\bios\b"],

    # --- Databases ---
    "sql": [r"\bsql\b"],
    "mysql": [r"\bmysql\b"],
    "postgresql": [r"\bpostgresql\b", r"\bpostgres\b"],
    "sqlite": [r"\bsqlite\b"],
    "mongodb": [r"\bmongodb\b", r"\bmongo\b"],
    "redis": [r"\bredis\b"],
    "elasticsearch": [r"\belasticsearch\b", r"\bes\b"],

    # --- Data / ML ---
    "pandas": [r"\bpandas\b"],
    "numpy": [r"\bnumpy\b"],
    "scikit-learn": [r"\bscikit[- ]learn\b", r"\bsklearn\b"],
    "tensorflow": [r"\btensorflow\b"],
    "pytorch": [r"\bpytorch\b", r"\btorch\b"],
    "keras": [r"\bkeras\b"],
    "machine learning": [r"\bmachine learning\b", r"\bml\b", r"머신러닝"],
    "deep learning": [r"\bdeep learning\b", r"\bdl\b", r"딥러닝"],
    "nlp": [r"\bnlp\b", r"\bnatural language processing\b", r"자연어"],
    "computer vision": [r"\bcomputer vision\b", r"\bcv\b", r"컴퓨터 비전"],
    "opencv": [r"\bopencv\b"],
    "huggingface": [r"\bhugging\s?face\b", r"\bhuggingface\b"],
    "transformer": [r"\btransformer\b", r"\btransformers\b"],
    "llm": [r"\bllm\b", r"\blarge language model\b", r"대규모 언어 모델"],
    "rag": [r"\brag\b", r"\bretrieval augmented generation\b"],
    "vector database": [r"\bvector database\b", r"\bvector db\b"],
    "faiss": [r"\bfaiss\b"],

    # --- Data Engineering ---
    "spark": [r"\bspark\b", r"\bapache spark\b"],
    "pyspark": [r"\bpyspark\b"],
    "hadoop": [r"\bhadoop\b"],
    "kafka": [r"\bkafka\b"],
    "airflow": [r"\bairflow\b"],
    "etl": [r"\betl\b"],

    # --- Cloud / DevOps ---
    "aws": [r"\baws\b", r"\bamazon web services\b"],
    "gcp": [r"\bgcp\b", r"\bgoogle cloud\b", r"\bgoogle cloud platform\b"],
    "azure": [r"\bazure\b"],
    "docker": [r"\bdocker\b", r"도커"],
    "kubernetes": [r"\bkubernetes\b", r"\bk8s\b"],
    "terraform": [r"\bterraform\b"],
    "ci/cd": [r"\bci/cd\b", r"\bcicd\b"],
    "github actions": [r"\bgithub actions\b"],
    "jenkins": [r"\bjenkins\b"],

    # --- Tools / OS ---
    "linux": [r"\blinux\b", r"리눅스"],
    "bash": [r"\bbash\b"],
    "git": [r"\bgit\b"],
    "github": [r"\bgithub\b"],
    "gitlab": [r"\bgitlab\b"],
    "jira": [r"\bjira\b"],
    "confluence": [r"\bconfluence\b"],

    # --- Game / Graphics ---
    "unity": [r"\bunity\b"],
    "unreal": [r"\bunreal\b", r"\bunreal engine\b"],
    "opengl": [r"\bopengl\b"],
    "vulkan": [r"\bvulkan\b"],
    "shader": [r"\bshader\b", r"\bshaders\b", r"\bglsl\b", r"\bhlsl\b"],
    "3d": [r"\b3d\b"],
    "game engine": [r"\bgame engine\b"],

    # --- Networking / APIs ---
    "rest api": [r"\brest api\b", r"\brestful\b"],
    "graphql": [r"\bgraphql\b"],
    "microservices": [r"\bmicroservices\b", r"\bmicroservice\b"],
    "msa": [r"\bmsa\b"],

    # --- Software Engineering ---
    "oop": [r"\boop\b", r"\bobject[- ]oriented\b"],
    "design patterns": [r"\bdesign patterns\b"],
    "testing": [r"\btesting\b"],
    "pytest": [r"\bpytest\b"],
    "unit testing": [r"\bunit testing\b"],
    "agile": [r"\bagile\b"],
    "scrum": [r"\bscrum\b"],
}