import os
import json
import re

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=GROQ_API_KEY
) if GROQ_API_KEY else None

def ai_analyze_resume(resume, job_description=""):

    if not client:
        raise RuntimeError("GROQ_API_KEY is not configured.")

    prompt = f"""
You are an expert ATS resume reviewer and professional career coach.

Analyze this resume:

{json.dumps(resume, ensure_ascii=False, indent=2)}

Target job description:

{job_description or "No job description provided."}

Return ONLY valid JSON using this structure:

{{
  "overall_score": 0,
  "ats_score": 0,
  "job_match_score": 0,
  "summary": "",
  "keyword_extraction": [],
  "matched_keywords": [],
  "missing_keywords": [],
  "skill_gap_analysis": [],
  "experience_analysis": {{
    "score": 0,
    "problems": [],
    "improvements": []
  }},
  "education_analysis": {{
    "score": 0,
    "problems": [],
    "improvements": []
  }},
  "formatting_analysis": {{
    "score": 0,
    "problems": [],
    "improvements": []
  }},
  "achievement_analysis": {{
    "score": 0,
    "problems": [],
    "improvements": []
  }},
  "rewrite_suggestions": [],
  "priority_fixes": []
}}

Rules:

1. Scores must be 0-100.
2. Never invent experience.
3. Never invent education.
4. Never invent skills.
5. Identify missing information.
6. Prefer measurable achievements.
7. Analyze ATS readability.
8. Compare against the job description when provided.
9. Return JSON only.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are an ATS resume analysis engine. Return valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=3000
    )

    result = response.choices[0].message.content

    return json.loads(result)

@app.post("/api/analyze")
def analyze():

    try:

        data = request.get_json(silent=True) or {}

        resume = data.get("resume", {})
        job_description = data.get("jobDescription", "")

        if not resume:
            return jsonify({
                "error": "Resume data is missing."
            }), 400

        result = ai_analyze_resume(
            resume,
            job_description
        )

        return jsonify(result)

    except json.JSONDecodeError:

        return jsonify({
            "error": "AI returned invalid data. Please retry."
        }), 502

    except Exception as e:

        print("AI ERROR:", str(e))

        return jsonify({
            "error": "AI analysis failed. Please retry."
        }), 500
