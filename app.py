"""
Ashish Kumar - Portfolio Website
Flask application serving a multi-page data-professional portfolio.
"""
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os

app = Flask(__name__)
app.secret_key = "ashish-portfolio-secret-key"

# When exported as a static site (GitHub Pages), the Flask contact route won't
# exist, so the form posts to Formspree instead. Set FORMSPREE_ENDPOINT to your
# own Formspree form URL (https://formspree.io -> create form -> copy the URL).
# When FREEZE=1 (used by freeze.py), the form uses this endpoint.
FORMSPREE_ENDPOINT = os.environ.get("FORMSPREE_ENDPOINT", "https://formspree.io/f/your-form-id")
IS_STATIC_BUILD = os.environ.get("FREEZE") == "1"

# ---------------------------------------------------------------------------
# Site-wide data (single source of truth, sourced from resume + GitHub)
# ---------------------------------------------------------------------------
PROFILE = {
    "name": "Ashish Kumar",
    "roles": ["Data Engineer", "Data Analyst", "Python Developer"],
    "tagline": "Turning data into meaningful insights and building scalable solutions for a better tomorrow.",
    "location": "Delhi & Noida, India",
    "email": "beashishrj@gmail.com",
    "phone": "+91 8707418744",
    "github": "https://github.com/ashishkumarrajpoot89",
    "linkedin": "https://www.linkedin.com/in/ashishkumarrajpoot89",
    "photo": "img/profile.jpg",
    "resume_file": "resume.pdf",
    "summary": (
        "Data Engineer with hands-on experience building Python-based ETL/ELT pipelines, SQL workflows, "
        "data-quality validation, and API integrations for a government student-admission platform. "
        "Delivered a rank-and-preference-based seat allocation engine processing 1M+ student records using "
        "Python, SQL, Apache Airflow, MySQL, ClickHouse, FastAPI, and SQLAlchemy, cutting manual processing "
        "time by an estimated 50%+. Skilled in data modeling, workflow orchestration, and schema validation. "
        "Currently upskilling in Agentic AI and LLM application development (RAG, MCP, LangGraph) to transition "
        "into AI-focused data engineering roles."
    ),
}

STATS = [
    {"value": "1M+", "label": "Records Processed"},
    {"value": "50%+", "label": "Manual Time Saved"},
    {"value": "15+", "label": "Projects on GitHub"},
    {"value": "100%", "label": "Passion for Data"},
]

TRAITS = [
    {"icon": "🧩", "title": "Problem Solver"},
    {"icon": "📚", "title": "Continuous Learner"},
    {"icon": "🤝", "title": "Team Player"},
    {"icon": "🚀", "title": "Passionate about Data"},
]

# Skills strictly from the resume. Each has a simple-icons slug + brand color where a
# logo exists; entries without a real logo (e.g. ETL, Schema Validation) use `slug: None`
# and render as a text tile. Logos: https://cdn.simpleicons.org/<slug>/<color>
SKILLS = {
    "Programming & Data Engineering": [
        {"name": "Python", "slug": "python", "color": "3776AB"},
        {"name": "SQL", "slug": "postgresql", "color": "4169E1"},
        {"name": "ETL / ELT", "slug": None, "color": None},
        {"name": "Data Pipelines", "slug": None, "color": None},
        {"name": "Data Integration", "slug": None, "color": None},
        {"name": "Data Modeling", "slug": None, "color": None},
        {"name": "Data Warehousing", "slug": None, "color": None},
        {"name": "Data Lake", "slug": None, "color": None},
        {"name": "Data Lakehouse", "slug": None, "color": None},
        {"name": "Batch Processing", "slug": None, "color": None},
        {"name": "Stream Processing", "slug": None, "color": None},
        {"name": "Schema Validation", "slug": None, "color": None},
        {"name": "Schema Evolution", "slug": None, "color": None},
        {"name": "Data Quality", "slug": None, "color": None},
        {"name": "Multiprocessing", "slug": None, "color": None},
    ],
    "Big Data & Distributed Processing": [
        {"name": "Apache Hadoop", "slug": "apachehadoop", "color": "66CCFF"},
        {"name": "HDFS", "slug": None, "color": None},
        {"name": "YARN", "slug": None, "color": None},
        {"name": "Apache Hive", "slug": "apachehive", "color": "FDEE21"},
        {"name": "Apache Spark", "slug": "apachespark", "color": "E25A1C"},
        {"name": "PySpark", "slug": "apachespark", "color": "E25A1C"},
        {"name": "Databricks", "slug": "databricks", "color": "FF3621"},
    ],
    "Data Transformation & Orchestration": [
        {"name": "dbt", "slug": "dbt", "color": "FF694B"},
        {"name": "Apache Airflow", "slug": "apacheairflow", "color": "017CEE"},
    ],
    "Databases & Data Warehousing": [
        {"name": "MySQL", "slug": "mysql", "color": "4479A1"},
        {"name": "PostgreSQL", "slug": "postgresql", "color": "4169E1"},
        {"name": "ClickHouse", "slug": "clickhouse", "color": "FFCC01"},
        {"name": "SQLite", "slug": "sqlite", "color": "003B57"},
        {"name": "Amazon Redshift", "slug": "amazonredshift", "color": "8C4FFF"},
        {"name": "Snowflake", "slug": "snowflake", "color": "29B5E8"},
        {"name": "BigQuery", "slug": "googlebigquery", "color": "669DF6"},
    ],
    "Streaming & CDC": [
        {"name": "Apache Kafka", "slug": "apachekafka", "color": "231F20"},
        {"name": "Amazon Kinesis", "slug": None, "color": None},
        {"name": "AWS DMS", "slug": None, "color": None},
        {"name": "Debezium", "slug": None, "color": None},
        {"name": "Change Data Capture", "slug": None, "color": None},
    ],
    "Cloud (AWS)": [
        {"name": "Amazon S3", "slug": None, "color": None},
        {"name": "AWS Glue", "slug": None, "color": None},
        {"name": "Amazon Redshift", "slug": "amazonredshift", "color": "8C4FFF"},
        {"name": "Amazon Athena", "slug": None, "color": None},
        {"name": "Amazon EMR", "slug": None, "color": None},
        {"name": "AWS Lambda", "slug": "awslambda", "color": "FF9900"},
        {"name": "AWS IAM", "slug": None, "color": None},
        {"name": "AWS DMS", "slug": None, "color": None},
        {"name": "Amazon Kinesis", "slug": None, "color": None},
    ],
    "Cloud Platforms": [
        {"name": "AWS", "slug": "amazonwebservices", "color": "FF9900"},
        {"name": "GCP (familiar)", "slug": "googlecloud", "color": "4285F4"},
        {"name": "Azure (familiar)", "slug": None, "color": None},
    ],
    "Data Lakehouse & Storage": [
        {"name": "Delta Lake", "slug": None, "color": None},
        {"name": "Apache Iceberg", "slug": "apacheiceberg", "color": "1C1C1C"},
        {"name": "Parquet", "slug": "apacheparquet", "color": "50ABF1"},
    ],
    "APIs & Development": [
        {"name": "FastAPI", "slug": "fastapi", "color": "009688"},
        {"name": "REST APIs", "slug": None, "color": None},
        {"name": "Strapi", "slug": "strapi", "color": "4945FF"},
        {"name": "Directus", "slug": "directus", "color": "263238"},
        {"name": "Streamlit", "slug": "streamlit", "color": "FF4B4B"},
    ],
    "Data & Analytics": [
        {"name": "Pandas", "slug": "pandas", "color": "150458"},
        {"name": "NumPy", "slug": "numpy", "color": "013243"},
        {"name": "SciPy", "slug": "scipy", "color": "8CAAE6"},
        {"name": "scikit-learn", "slug": "scikitlearn", "color": "F7931E"},
        {"name": "Data Cleaning", "slug": None, "color": None},
        {"name": "Data Preprocessing", "slug": None, "color": None},
    ],
    "BI & Visualization": [
        {"name": "Power BI", "slug": "powerbi", "color": "F2C811"},
        {"name": "Apache Superset", "slug": "apachesuperset", "color": "20A6C9"},
        {"name": "Matplotlib", "slug": None, "color": None},
        {"name": "Seaborn", "slug": None, "color": None},
    ],
    "DevOps & Tools": [
        {"name": "Docker", "slug": "docker", "color": "2496ED"},
        {"name": "Git", "slug": "git", "color": "F05032"},
        {"name": "GitHub", "slug": "github", "color": "FFFFFF"},
        {"name": "DataGrip", "slug": "datagrip", "color": "22D88F"},
        {"name": "VS Code", "slug": "visualstudiocode", "color": "007ACC"},
        {"name": "Jupyter", "slug": "jupyter", "color": "F37626"},
        {"name": "Excel", "slug": "microsoftexcel", "color": "217346"},
        {"name": "Google Sheets", "slug": "googlesheets", "color": "34A853"},
    ],
}

# The 6 PINNED repos shown on the GitHub profile Overview, with their real descriptions.
# `scene` picks a CSS/SVG illustration: dashboard | pipeline | house.
GITHUB = PROFILE["github"]
PROJECTS = [
    {
        "slug": "adventure-works",
        "title": "Adventure Works Sales Analytics",
        "tags": ["Data Analytics", "Power BI"],
        "accent": "#FF4103",
        "scene": "dashboard",
        "short": "End-to-end sales analytics pipeline using Python, MySQL and Power BI.",
        "description": (
            "Developed a complete data analytics pipeline using Python and SQL for Adventure Works, enhancing "
            "data accuracy and management. Tech Stack: Python, MySQL, Power BI."
        ),
        "stack": ["Python", "MySQL", "Power BI"],
        "github": GITHUB + "/Adventure_works_",
        "sections": {
            "Overview": "End-to-end sales analytics pipeline enhancing data accuracy and management.",
            "Tech Stack": "Python, MySQL and Power BI.",
            "Highlights": "Data cleaning and transformation, SQL loading, and interactive dashboards.",
        },
        "features": [
            "Complete Python + SQL analytics pipeline",
            "Improved data accuracy and management",
            "Interactive Power BI dashboards for reporting",
        ],
    },
    {
        "slug": "sales-demand-forecast",
        "title": "Sales Demand Forecast",
        "tags": ["Machine Learning", "Pipeline"],
        "accent": "#ff6a3d",
        "scene": "house",
        "short": "Full ML pipeline to forecast product sales demand end to end.",
        "description": (
            "A full-fledged machine learning pipeline to forecast product sales demand. It includes data "
            "ingestion, validation, transformation, model training, evaluation, logging, and deployment."
        ),
        "stack": ["Python", "scikit-learn", "Pandas"],
        "github": GITHUB + "/Sales-Demand-Forecast",
        "sections": {
            "Overview": "End-to-end ML pipeline for product sales demand forecasting.",
            "Tech Stack": "Python and scikit-learn.",
            "Highlights": "Ingestion, validation, transformation, training, evaluation, logging and deployment.",
        },
        "features": [
            "Data ingestion, validation and transformation",
            "Model training, evaluation and logging",
            "Deployment-ready pipeline",
        ],
    },
    {
        "slug": "insurance-fraud-detection",
        "title": "Insurance Fraud Detection",
        "tags": ["Machine Learning", "Pipeline"],
        "accent": "#d6350a",
        "scene": "pipeline",
        "short": "End-to-end ML pipeline to detect fraudulent insurance claims.",
        "description": (
            "A complete end-to-end machine learning pipeline to detect fraudulent insurance claims using "
            "historical data. This project automates the entire process from data ingestion and validation to "
            "model training and evaluation."
        ),
        "stack": ["Python", "scikit-learn", "Pandas"],
        "github": GITHUB + "/Insurance-Fraud-detection",
        "sections": {
            "Overview": "Detects fraudulent insurance claims from historical data.",
            "Tech Stack": "Python and scikit-learn.",
            "Highlights": "Automated ingestion, validation, training and evaluation.",
        },
        "features": [
            "Automated data ingestion and validation",
            "Fraud classification model",
            "End-to-end automated pipeline",
        ],
    },
    {
        "slug": "olympics-analysis",
        "title": "Olympics Analysis",
        "tags": ["Data Analytics", "Streamlit"],
        "accent": "#ff8a5c",
        "scene": "dashboard",
        "short": "Interactive Streamlit app analyzing 120 years of Olympic history.",
        "description": (
            "Developed an interactive web application using Streamlit to analyze 120 years of Olympic history "
            "with dynamic visualizations. Created country-specific and athlete-wise performance statistics to "
            "explore trends over time."
        ),
        "stack": ["Python", "Streamlit", "Pandas"],
        "github": GITHUB + "/Olympics-Analysis-",
        "sections": {
            "Overview": "Interactive analysis of 120 years of Olympic history.",
            "Tech Stack": "Python and Streamlit.",
            "Highlights": "Country-specific and athlete-wise performance statistics with dynamic visualizations.",
        },
        "features": [
            "120 years of Olympic data analyzed",
            "Country and athlete-wise statistics",
            "Dynamic visualizations in Streamlit",
        ],
    },
    {
        "slug": "movie-ratings-analysis",
        "title": "Movie Ratings & Genre Analysis",
        "tags": ["Data Analytics", "Streamlit"],
        "accent": "#FF4103",
        "scene": "dashboard",
        "short": "Streamlit dashboard exploring trends in movie ratings and genres.",
        "description": (
            "A Python-based data analysis project that explores trends in movie ratings and genres. Using a "
            "Streamlit dashboard, it provides insights into popular genres, audience preferences, and rating "
            "patterns."
        ),
        "stack": ["Python", "Streamlit", "Pandas"],
        "github": GITHUB + "/Movie_Ratings_and_Genre_Analysis",
        "sections": {
            "Overview": "Explores trends in movie ratings and genres.",
            "Tech Stack": "Python and Streamlit.",
            "Highlights": "Popular genres, audience preferences and rating patterns.",
        },
        "features": [
            "Genre popularity analysis",
            "Audience preference insights",
            "Interactive Streamlit dashboard",
        ],
    },
    {
        "slug": "fake-news-detector",
        "title": "Fake News Detector (GPT-2)",
        "tags": ["NLP", "Machine Learning"],
        "accent": "#ff6a3d",
        "scene": "pipeline",
        "short": "Identifies human-written vs GPT-2 generated text.",
        "description": (
            "This project focuses on identifying whether a given piece of text is human-written or generated "
            "by GPT-2 models of various sizes. Using the official GPT-2 Output Dataset released by OpenAI, it "
            "analyzes and classifies the text."
        ),
        "stack": ["Python", "NLP", "scikit-learn"],
        "github": GITHUB + "/Fake-News-Detector-Using-ChatCPT-2",
        "sections": {
            "Overview": "Classifies whether text is human-written or GPT-2 generated.",
            "Tech Stack": "Python and NLP.",
            "Highlights": "Uses the official OpenAI GPT-2 Output Dataset across model sizes.",
        },
        "features": [
            "Human vs GPT-2 text classification",
            "Built on OpenAI's GPT-2 Output Dataset",
            "NLP feature analysis",
        ],
    },
]

EXPERIENCE = [
    {
        "period": "June 2026 - Present",
        "role": "Junior Software Developer",
        "org": "Samarth eGov (Ministry of Education, GoI)",
        "points": [
            "Developed and maintained a rank-and-preference-based seat allocation engine processing 1M+ student records.",
            "Engineered merit-ranking logic with multi-level tie-breaking across 2M+ applicant records.",
            "Built and orchestrated Python ETL pipelines with Apache Airflow, cutting manual processing time by ~50%+.",
            "Integrated Strapi and Directus APIs and built internal FastAPI endpoints for reporting.",
        ],
    },
    {
        "period": "March 2026 - June 2026",
        "role": "Data Science Intern",
        "org": "Samarth eGov (Ministry of Education, GoI)",
        "points": [
            "Built foundational data-engineering components for a state-level student admission system.",
            "Contributed to seat allocation, merit-ranking logic and MySQL data-extraction workflows.",
            "Developed Apache Airflow DAGs and schema-validation checks.",
        ],
    },
]

EDUCATION = [
    {
        "degree": "B.Tech, Computer Science and Engineering",
        "school": "Bundelkhand University, Jhansi, Uttar Pradesh",
        "period": "August 2019 - June 2023",
    },
]

# The resume lists no certifications, but has a "Currently Learning" section — real content.
LEARNING = [
    "LangChain & LangGraph",
    "OpenAI Agents SDK, MCP & A2A",
    "RAG & Agentic RAG",
    "Context & Prompt Engineering",
    "Vector Databases & FAISS",
    "Guardrails, LangSmith & Langfuse",
    "Docker, GitHub Actions & Nginx",
    "OpenAI, Anthropic, Gemini, Groq, Ollama",
]

# No real blog content exists, so the blog section is omitted to avoid fabricating posts.


@app.context_processor
def inject_globals():
    # On the single-page home, anchor links are bare "#section".
    # On other pages (e.g. project detail) they become "/#section" to go home first.
    nav_base = "" if request.path == "/" else url_for("home")
    # Static build posts the contact form to Formspree; Flask build uses its route.
    contact_action = FORMSPREE_ENDPOINT if IS_STATIC_BUILD else url_for("contact_submit")
    # Static build links Download straight to the PDF; Flask build uses its route.
    if IS_STATIC_BUILD:
        resume_download_url = url_for("static", filename=PROFILE["resume_file"])
    else:
        resume_download_url = url_for("resume_download")
    return {
        "profile": PROFILE,
        "current_year": 2026,
        "nav_base": nav_base,
        "contact_action": contact_action,
        "resume_download_url": resume_download_url,
    }


@app.route("/")
def home():
    """Single-page portfolio: all sections stacked on one scrollable page."""
    return render_template(
        "index.html",
        stats=STATS,
        traits=TRAITS,
        skills=SKILLS,
        projects=PROJECTS,
        experience=EXPERIENCE,
        education=EDUCATION,
        learning=LEARNING,
    )


# --- Backward-compatible routes: redirect old page URLs to the matching anchor ---
@app.route("/about")
def about():
    return redirect(url_for("home") + "#about")


@app.route("/skills")
def skills():
    return redirect(url_for("home") + "#skills")


@app.route("/projects")
def projects():
    return redirect(url_for("home") + "#projects")


@app.route("/experience")
def experience():
    return redirect(url_for("home") + "#experience")


@app.route("/education")
def education():
    return redirect(url_for("home") + "#education")


@app.route("/resume")
def resume():
    return redirect(url_for("home") + "#resume")


@app.route("/contact")
def contact():
    return redirect(url_for("home") + "#contact")


# --- Project detail keeps its own page for the deep view ---
@app.route("/projects/<slug>")
def project_detail(slug):
    project = next((p for p in PROJECTS if p["slug"] == slug), None)
    if project is None:
        return render_template("404.html"), 404
    return render_template("project_detail.html", project=project, active="projects")


@app.route("/resume/download")
def resume_download():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        PROFILE["resume_file"],
        as_attachment=True,
    )


@app.route("/contact/submit", methods=["POST"])
def contact_submit():
    name = request.form.get("name", "").strip()
    # In a real deployment this would send an email or store the message.
    flash(f"Thanks {name or 'there'}! Your message has been received.", "success")
    return redirect(url_for("home") + "#contact")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    # Local dev runs on port 5000 with debug on. Hosting platforms set $PORT and
    # run the app via gunicorn (see Procfile), so this block is dev-only.
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
