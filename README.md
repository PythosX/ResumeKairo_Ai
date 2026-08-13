# ResumeKairo

ResumeKairo is a dark, anime-inspired SaaS resume builder and analyzer built with Flask, HTML, CSS and JavaScript.

## Features

- 20 resume template styles
- Live A4 resume preview
- Photo upload
- Personal details, skills, experience, education and achievements
- Resume analysis dashboard
- ATS-style score
- Job-match scoring
- Keyword extraction
- Skill-gap feedback
- Experience, education, formatting and achievement analysis
- Rewrite suggestions
- Cover-letter generation endpoint
- Resume upload endpoint for PDF/DOC/DOCX/TXT
- Responsive mobile UI
- Animated gradient SaaS design
- Render-ready Flask deployment
- GitHub-friendly project structure

## Project structure

```text
ResumeKairo/
├── app.py
├── requirements.txt
├── render.yaml
├── .gitignore
├── .env.example
├── README.md
├── templates/
├── static/
└── uploads/
```

## Local setup

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Deployment

Push the repository to GitHub and connect the repository to Render. Render can use `render.yaml` automatically.

## AI integration

The included API routes are intentionally provider-neutral. Add your chosen AI provider on the server side and keep credentials in Render environment variables. Never put private API keys in frontend JavaScript.

## License

Use and customize this starter project for your own portfolio or product.
