import os, re, json, uuid
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
UPLOAD_DIR = os.path.join(app.root_path, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED = {"pdf", "doc", "docx", "txt"}

@app.route("/")
def index(): return render_template("index.html")

@app.route("/builder")
def builder(): return render_template("builder.html")

@app.route("/analysis")
def analysis(): return render_template("analysis.html")

@app.route("/preview")
def preview(): return render_template("preview.html")

@app.post("/api/upload")
def upload():
    f = request.files.get("resume")
    if not f or not f.filename:
        return jsonify(error="Please select a resume file."), 400
    ext = f.filename.rsplit(".",1)[-1].lower() if "." in f.filename else ""
    if ext not in ALLOWED:
        return jsonify(error="Supported files: PDF, DOC, DOCX, TXT."), 400
    name = secure_filename(f.filename)
    token = f"{uuid.uuid4().hex}_{name}"
    path = os.path.join(UPLOAD_DIR, token)
    f.save(path)
    return jsonify(ok=True, filename=name, file_id=token,
                   message="File uploaded. Connect your AI/parser service to extract content.")

@app.post("/api/analyze")
def analyze():
    data = request.get_json(silent=True) or {}
    resume = data.get("resume", {})
    job = data.get("jobDescription", "")
    text = json.dumps(resume).lower()
    points = 45
    checks = {
        "contact": bool(resume.get("email") and resume.get("name")),
        "summary": bool(resume.get("summary")),
        "skills": bool(resume.get("skills")),
        "experience": bool(resume.get("experience")),
        "education": bool(resume.get("education")),
        "achievements": bool(resume.get("achievements"))
    }
    points += sum(8 for v in checks.values() if v)
    ats = min(points, 98)
    keywords = [x.strip() for x in str(resume.get("skills","")).split(",") if x.strip()]
    job_words = set(re.findall(r"[a-zA-Z][a-zA-Z+#.-]{2,}", job.lower()))
    matched = [k for k in keywords if k.lower() in job_words]
    job_score = min(95, 45 + len(matched)*7) if job else min(92, ats+3)
    return jsonify(
        overall=ats, ats_score=ats, job_match=job_score,
        keywords=keywords[:20], matched_keywords=matched[:20],
        skill_gap=["Add job-specific skills from the target description."] if job and not matched
                  else ["Prioritize measurable, role-specific skills."],
        experience="Use Action + Task + Result bullets and quantify impact.",
        education="Keep degree, institution and graduation year clearly labeled.",
        formatting="Use standard headings, readable typography and ATS-safe structure.",
        achievements="Add numbers such as %, revenue, users, time saved or scale.",
        rewrites=["Replace duty-based bullets with measurable outcomes.",
                  "Tailor the summary to the target role.",
                  "Mirror important keywords from the job description."]
    )

@app.post("/api/cover-letter")
def cover_letter():
    data=request.get_json(silent=True) or {}
    r=data.get("resume",{})
    role=r.get("title") or "the position"
    company=data.get("company") or "your organization"
    return jsonify(text=f"""Dear Hiring Manager,

I am excited to apply for {role} at {company}. My background, skills, and experience align well with the requirements of the role. I bring a results-focused approach and enjoy turning challenging problems into practical outcomes.

I would welcome the opportunity to discuss how my experience can contribute to your team.

Sincerely,
{r.get("name") or "Your Name"}""")

@app.get("/health")
def health(): return jsonify(status="ok")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)), debug=True)
