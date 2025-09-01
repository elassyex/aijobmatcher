import os
import json
import re
from typing import List, Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Improved experience bonus (proportional scaling)
EXPERIENCE_BONUS = {
    "0-1": 0,
    "1-3": 5,
    "3-5": 10,
    "5-7": 15,
    "7+": 20,
}


def _safe_json_extract(s: str) -> Dict[str, Any]:
    """Extract JSON safely from AI response."""
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", s, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in AI output.")
        return json.loads(match.group(0))


class JobMatchAnalyzer:
    """Analyze candidate-job match using Gemini AI."""

    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY is missing in .env file")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def analyze_match(self, user_skills: List[str], job_role: str, experience: str) -> Dict[str, Any]:
        job_role = (job_role or "").strip()
        norm_skills = [s.strip().lower().replace(" ", "-") for s in (user_skills or [])]
        exp_bonus = EXPERIENCE_BONUS.get(experience, 0)

        try:
            return self._analyze_with_gemini(norm_skills, job_role, exp_bonus)
        except Exception as e:
            return self._fallback_analysis(norm_skills, job_role, exp_bonus, error=str(e))

    def _analyze_with_gemini(self, skills: List[str], role: str, exp_bonus: int) -> Dict[str, Any]:
        prompt = f"""
        You are a senior technical recruiter and career coach.
        Analyze the match between the candidate and the job role. 
        Consider synonyms, related technologies, and industry standards.

        Job Role: {role}
        User Skills: {', '.join(skills)}
        Experience Bonus (points): {exp_bonus}

        Provide a precise JSON response with:
        {{
            "inferred_core_skills": string[],  # Skills typically required for this role
            "inferred_preferred_skills": string[],  # Nice-to-have skills
            "matched_core_skills": string[],  # Skills matched from user's list
            "matched_preferred_skills": string[],
            "missing_core_skills": string[],
            "missing_preferred_skills": string[],
            "core_match": number,  # percentage 0-100
            "preferred_match": number,  # percentage 0-100
            "overall_before_experience": number,  # average weighted score
            "recommendations": string[]  # Actionable, practical tips
        }}

        - Ensure percentages are realistic and based on skill alignment.
        - Only return valid JSON. Do not include explanations outside the JSON.
        """

        response = self.model.generate_content(prompt)
        payload = _safe_json_extract(response.text)

        core = float(payload.get("core_match", 0.0))
        preferred = float(payload.get("preferred_match", 0.0))
        overall_before = float(payload.get("overall_before_experience", 0.0))
        overall = min(100.0, overall_before + exp_bonus)
        print(overall)

        return {
            "match_percentage": round(overall, 1),
            "core_match": round(core, 1),
            "preferred_match": round(preferred, 1),
            "matched_skills": list(set(payload.get("matched_core_skills", []) +
                                       payload.get("matched_preferred_skills", []))),
            "missing_core_skills": payload.get("missing_core_skills", []),
            "missing_preferred_skills": payload.get("missing_preferred_skills", []),
            "recommendations": payload.get("recommendations", [])[:6],
            "skill_breakdown": {
                "Core Skills": round(core, 1),
                "Preferred Skills": round(preferred, 1),
                "Experience Bonus": float(exp_bonus)
            },
            "debug_inferred": {
                "inferred_core_skills": payload.get("inferred_core_skills", []),
                "inferred_preferred_skills": payload.get("inferred_preferred_skills", [])
            }
        }

    def _fallback_analysis(self, skills: List[str], role: str, exp_bonus: int, error: str = "") -> Dict[str, Any]:
        # base_score = min(50.0 + len(skills) * 5, 70.0)
        overall = min(100.0 + exp_bonus)

        return {
            "match_percentage": round(overall, 1),
            "core_match": round(min(overall, 100.0), 1),
            "preferred_match": round(min(overall, 100.0), 1),
            "matched_skills": skills,
            "missing_core_skills": [],
            "missing_preferred_skills": [],
            "recommendations": [
                "Add more job-specific technical skills.",
                "Complete a certification relevant to the role.",
                "Build a portfolio project demonstrating your expertise."
            ],
            "skill_breakdown": {
                "Core Skills": round(min(overall * 0.1, 100.0), 1),
                "Preferred Skills": round(min(overall * 0.1, 100.0), 1),
                "Experience Bonus": float(exp_bonus)
            },
            "debug_inferred": {},
            "note": f"Fallback used due to error: {error}" if error else "Fallback used."
        }


# Test example
if __name__ == "__main__":
    analyzer = JobMatchAnalyzer()
