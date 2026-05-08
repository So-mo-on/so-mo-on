"""
data.py — YOUR PERSONAL CONTENT FILE.
=========================================
This is the main file you'll edit to update your website.
No HTML knowledge needed — just edit the Python variables below!

Tips:
- Strings use regular quotes: "like this"
- Lists use square brackets: ["item1", "item2"]
- Dictionaries use curly braces: {"key": "value"}
"""

# ─────────────────────────────────────────────
# BASIC INFO
# ─────────────────────────────────────────────

NAME = "Fatemeh S. Moghadam"
TAGLINE = "Data science · Network science . Computational neuroscience"
ABOUT = """
Data scientist and computational neuroscience researcher with 4+ years of experience analyzing complex biomedical data. Skilled in machine learning, NLP, network analysis, and statistical modeling, with applications in fMRI, clinical text, and time-series data.
"""

CONTACT = {
    "email": "fatemeh.soleymanimog@ucalgary.ca  ",
    "linkedin": "https://www.linkedin.com/in/fatemeh-so-mo/",   # or "" to hide
    "github": "https://github.com/So-mo-on",         # or "" to hide
    # "twitter": "",                                        # or "" to hide
}


# ─────────────────────────────────────────────
# SKILLS
# ─────────────────────────────────────────────
# Group your skills into categories.
# Add or remove categories freely.

SKILLS = [
    {
        "category": "Programming Languages",
        "skills": ["Python", "R", "SQL", "MATLAB", "C", "C++"],
    },
    {
        "category": "Data Science & Machine Learning",
        "skills": [
            "pandas", "NumPy", "SciPy", "scikit-learn",
            "TensorFlow", "PyTorch", "Keras",
            "statsmodels", "TensorFlow Recommenders"
        ],
    },
    {
        "category": "Network Science",
        "skills": [
            "NetworkX", "Graph Theory",
            "Community Detection",
            "Complex Systems Modeling"
        ],
    },
    {
        "category": "Neuroimaging & Health Data",
        "skills": [
            "fMRIprep", "nilearn", "FSLeyes", "CONN Toolbox",
            "Brain Time-Series Analysis", "Biomarker Identification", "Hormonal Data Analysis",
            "Phenotypic & Demographic Data"]
    },
    {
        "category": "NLP & Text Mining",
        "skills": [
            "NLP Pipelines", "Named Entity Recognition",
            "Text Classification", "BeautifulSoup", "Selenium"
        ],
    },
    {
        "category": "Data Visualization",
        "skills": [
            "Matplotlib", "Seaborn", "PyVis",
            "Tableau", "Streamlit", "Plotly"
        ],
    },
    {
        "category": "HPC & Cloud",
        "skills": [
            "Linux", "SLURM", "MPI",
            "AWS", "Flask"
        ],
    },
    {
        "category": "Version Control",
        "skills": ["Git (GitHub, GitLab)"],
    },
]


# ─────────────────────────────────────────────
# WORK EXPERIENCES
# ─────────────────────────────────────────────
# List from most recent to oldest.

WORK_EXPERIENCES = [
    {
        "title": "Mathematics Specialist",
        "company": "Turing Inc.",
        "period": "Summer 2025 – Present",
        "description": "Authored and evaluated mathematical tasks to support LLM fine-tuning. Designed evaluation rubrics to improve training data quality.",
       "tech": ["LLM Evaluation", "Prompt Engineering", "Statistical Reasoning", "Data Quality", "Python"],
    },
    {
        "title": "Recommendation System Trainee",
        "company": "Opoint",
        "period": "Winter 2022 – Spring 2022",
        "description": "Built a recommendation system to personalize content based on user interaction data. Improved model performance using precision and recall metrics.",
        "tech": ["Python", "scikit-learn", "TensorFlow Recommenders", "pandas", "Collaborative Filtering", "Feature Engineering"],
    },
    {
        "title": "API Developer",
        "company": "Nikpardaz",
        "period": "Spring 2021",
        "description": "Designed and deployed APIs for a language learning app.",
       "tech": ["Python", "Flask"],
    },
]


# ─────────────────────────────────────────────
# PROJECTS
# ─────────────────────────────────────────────

PROJECTS = [
    {
        "title": "fMRI Network Analysis",
        "description": "Large-scale fMRI analysis pipeline studying ovarian hormone effects on brain network topology.",
        "tech": [
            "Python", "fMRIprep", "nilearn", "NetworkX",
            "SciPy", "pandas", "SLURM"
        ],
        "link": "",
        "link_label": "",
    },
    {
        "title": "Scientific Literature Network Explorer",
        "description": "Interactive web app mapping relationships between papers, authors, and topics to help researchers explore academic landscapes.",
        "tech": [
            "Python", "Streamlit", "Flask",
            "PyVis", "Matplotlib", "Data Visualization"
        ],
        "link": "",
        "link_label": "",
    },
    # {
    #     "title": "Medical NLP & Condition Network Modeling",
    #     "description": "Interactive web app mapping relationships between papers, authors, and topics to help researchers explore academic landscapes.",
    #     "tech": [
    #         "Python", "BeautifulSoup", "NetworkX",
    #         "NLP", "scikit-learn"
    #     ],
    #     "link": "",
    #     "link_label": "",
    # },
    {
        "title": "Neural Dynamics During Problem Solving",
        "description": "Analyzed fMRI time-series to study brain dynamics during insight problem solving using Hopfield and Ising models.",
        "tech": [
            "Python", "MATLAB",
            "Time-Series Analysis", "Statistical Physics", "Data Visualization"
        ],
        "link": "",
        "link_label": "",
    },
    {
        "title": "Collective Motion",
        "description": "Simulated the collective behavior of bird flocks and their phase transitions.",
        "tech": [
            "Python",
            "Simulation",
            "Statistical Physics",
            "Data Visualization"
        ],
        "link": "",
        "link_label": "",
    },
]


# ─────────────────────────────────────────────
# PRESENTATIONS
# ─────────────────────────────────────────────

PRESENTATIONS = [
    {
        "title": "Effect of Ovarian Hormone Fluctuations on Brain Network Connectivity",
        "event": "NetSci Conference, Maastricht",
        "year": "2025",
        "link": "",
    },
    {
        "title": "Phase-Specific Variations in Brain Network Connectivity with Ovarian Hormones",
        "event": "APS Northwest Meeting, Calgary",
        "year": "2025",
        "link": "",
    },
    {
        "title": "Phase-Specific Variations in Brain Network Connectivity",
        "event": "UCalgary Computational Neuroscience Research Day",
        "year": "2025",
        "link": "",
    },
    {
        "title": "Brain Network Communicability Across Menstrual Cycle Phases",
        "event": "Hotchkiss Brain Institute Research Day (Poster)",
        "year": "2025",
        "link": "",
    },
    {
        "title": "Brain Network Communicability Across Menstrual Cycle Phases",
        "event": "Complex Networks Conference, Istanbul",
        "year": "2024",
        "link": "",
    },
    {
        "title": "Brain Network Dynamics During Creative Problem Solving",
        "event": "Joint Cognitive Science Symposium (Poster)",
        "year": "2022",
        "link": "",
    },
]


# ─────────────────────────────────────────────
# PAPERS & ESSAYS (Writing Page)
# ─────────────────────────────────────────────

WRITING_INTRO = """
I believe science belongs to everyone — not just academics.
Below are articles and essays I've written to make complex topics
understandable and exciting for teenagers and general audiences.
"""

PAPERS = [
    {
        "title": "Why Black Holes Are Not What You Think",
        "venue": "Teen Science Monthly",
        "year": "2023",
        "description": "A beginner-friendly deep dive into black holes, debunking common myths.",
        "tags": ["Astrophysics", "Teenagers"],
        "link": "https://example.com/black-holes",
    },
    {
        "title": "The Secret Life of Proteins",
        "venue": "Science for All Newsletter",
        "year": "2022",
        "description": "How proteins fold, why it matters, and what it means for medicine.",
        "tags": ["Biology", "Teenagers"],
        "link": "https://example.com/proteins",
    },
    {
        "title": "Data in Everyday Life",
        "venue": "Personal Essay",
        "year": "2022",
        "description": "An essay exploring how data shapes the decisions we make every day.",
        "tags": ["Data Science", "Essay"],
        "link": "",  # no link yet
    },
    {
        "title": "Climate Change Explained Without the Jargon",
        "venue": "Teen Science Monthly",
        "year": "2021",
        "description": "Breaking down the science of climate change for a young audience.",
        "tags": ["Climate", "Teenagers"],
        "link": "https://example.com/climate",
    },
]


# ─────────────────────────────────────────────
# ANALYTICS TOOL PAGE
# ─────────────────────────────────────────────

ANALYTICS_TOOL_TITLE = "symptonet"
ANALYTICS_TOOL_DESCRIPTION = """
This is my Python data analytics function — available for you to try directly in the browser.
Paste comma-separated numbers below and the tool will compute statistics for you.
"""
ANALYTICS_TOOL_INSTRUCTIONS = "Enter comma-separated numbers (e.g. 12, 45, 7, 88, 23)"


SCINET_TOOL_TITLE = "SciNet"
SCINET_TOOL_DESCRIPTION = "Description of your SciNet tool here."

SEMANTIC_SCHOLAR_API_KEY = "UchKWOJtVX7lXiHoQNW1a2794CU4fqet8f6DaFs0"