# Ashish Kumar — Portfolio Website

A dark-themed data-professional portfolio built with **Python + Flask**, matching the 12-page design.

## Pages
Home (hero + stats), About, Skills & Tools, Projects (+ project detail), Experience, Education & Certifications, Resume, Blog, Contact, and a custom 404 ("Lost in Data Space").

## Run it locally

```bash
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000

## Add your real photo and resume

The site works out of the box with a placeholder image. To use your own:

1. Save your photo as: `static/img/profile.jpg`
2. Save your resume as: `static/resume.pdf`

No code changes needed — the templates already point to these paths, and the download button + PDF preview will work once `resume.pdf` is present.

## Where to edit content

All text (summary, skills, projects, experience, education, certifications, blog posts, social links) lives in the data dictionaries at the top of **`app.py`** — edit there and the whole site updates.

## Structure

```
portfolio/
├── app.py                 # Flask app + all site content
├── requirements.txt
├── templates/             # Jinja2 templates (one per page + base layout)
└── static/
    ├── css/style.css      # Dark theme, gradients, responsive
    ├── js/main.js         # Nav toggle, skills filter, scroll reveal
    ├── img/               # profile.jpg goes here
    └── resume.pdf         # your resume goes here
```
