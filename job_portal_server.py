import json
import os
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent

RESUME = {
    "name": "Maneesh Tiwari",
    "email": "er.maneeshtiwari@gmail.com",
    "experience": [
        {"title": "Full Stack Developer", "company": "Virtual Employee Pvt. Ltd", "period": "January 2020 - Present"},
        {"title": "Sr. Web Developer", "company": "V2web", "period": "August 2014"},
        {"title": "Sr. Web Developer", "company": "Cannoneye Web Solution", "period": "October 2013"},
        {"title": "Jr. Web Developer", "company": "Malviya Technologies", "period": "December 2012"},
    ],
    "education": "B.Tech - HMFAMIET",
    "skills": [
        "React", "React.js", "Node.js", "PHP", "Laravel", "Vue.js", "MongoDB", "MySQL",
        "AWS", "Express.js", "JavaScript", "jQuery", "HTML", "HTML5", "CSS", "CSS3",
        "Bootstrap", "Redux Toolkit", "REST", "CI/CD", "Git", "WordPress", "WooCommerce",
        "PrestaShop", "CodeIgniter", "Stripe", "OpenAI", "Gemini", "Python", "APIs", "Bitbucket"
    ],
    "preferred_titles": ["Senior Full Stack Developer", "PHP Developer"],
    "min_salary": "$1,500",
    "willing_to_relocate": True,
    "years_experience": 10
}

TODAY = datetime.now().strftime("%Y-%m-%d")
YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

JOBS = [
    {
        "id": "JOBSEARCH_01",
        "title": "Senior Full Stack Developer – React & Node",
        "company": "TechNova Labs",
        "location": "Remote",
        "posted": TODAY,
        "type": "Full-time",
        "salary": "$110,000 - $140,000/year",
        "url": "https://to.indeed.com/aakp8t7yfwkx",
        "description": "We are seeking a Senior Full Stack Developer with 6+ years of experience in React.js, Node.js, Express.js, and MongoDB. You will architect and build scalable SaaS products, work with REST APIs, manage AWS deployments, and mentor junior engineers. Required: React, Node.js, MongoDB, AWS, Git, CI/CD pipelines, Redux Toolkit. Bonus: Vue.js, Docker, TypeScript."
    },
    {
        "id": "JOBSEARCH_02",
        "title": "Senior PHP Laravel Developer",
        "company": "CloudStack Solutions",
        "location": "Remote",
        "posted": TODAY,
        "type": "Full-time",
        "salary": "$80,000 - $100,000/year",
        "url": "https://to.indeed.com/aatxym4dhlv2",
        "description": "CloudStack is hiring a Senior PHP Laravel Developer with 5+ years of Laravel, CodeIgniter, and MySQL experience. You will build and maintain enterprise-grade applications. Skills required: PHP, Laravel, CodeIgniter, MySQL, REST APIs, jQuery, Bootstrap, Git. Stripe payment integration experience is a strong plus."
    },
    {
        "id": "JOBSEARCH_03",
        "title": "Full Stack Engineer – Vue.js & Node.js",
        "company": "Nexus Digital",
        "location": "Remote",
        "posted": YESTERDAY,
        "type": "Full-time",
        "salary": "$95,000 - $125,000/year",
        "url": "https://to.indeed.com/aadssrfljlcv",
        "description": "Nexus Digital is looking for a Full Stack Engineer to join our growing team. Must have strong Vue.js, Node.js, Express.js, and MongoDB skills. Experience with AWS S3, REST APIs, and CI/CD pipelines required. WooCommerce and PrestaShop experience is a big plus. We value engineers who can work independently and take ownership."
    },
    {
        "id": "JOBSEARCH_04",
        "title": "Senior Full Stack Developer – E-Commerce",
        "company": "ShopEngine",
        "location": "Remote",
        "posted": YESTERDAY,
        "type": "Full-time",
        "salary": "$100,000 - $130,000/year",
        "url": "https://to.indeed.com/aakg996klpbb",
        "description": "ShopEngine builds e-commerce platforms for thousands of merchants. We need a Senior Full Stack Developer with deep WooCommerce, WordPress, PrestaShop, and PHP experience. React.js or Vue.js is required for our headless frontends. Stripe and payment gateway integration experience mandatory. MySQL, REST APIs, Git required."
    },
    {
        "id": "JOBSEARCH_13",
        "title": "Senior Software Engineer – Full Stack",
        "company": "Kerner Norland",
        "location": "Remote",
        "posted": "2026-05-21",
        "type": "Permanent",
        "salary": "$120,000 - $155,000/year",
        "url": "https://to.indeed.com/aakp8t7yfwkx",
        "description": "Senior Full Stack Software Engineer with 7+ years of experience. Stack: React, Node.js, Express.js, MongoDB, AWS. You will design scalable microservices, build REST APIs, manage CI/CD pipelines, and mentor junior developers. Must know Redux Toolkit, Git, Bitbucket. Python and OpenAI API integration experience is a bonus."
    },
    {
        "id": "JOBSEARCH_14",
        "title": "Senior Full Stack Engineer",
        "company": "CSC Generation",
        "location": "Remote",
        "posted": "2026-02-28",
        "type": "Full-time",
        "salary": "$105,000 - $135,000/year",
        "url": "https://to.indeed.com/aatxym4dhlv2",
        "description": "CSC Generation is looking for a Senior Full Stack Engineer to join our commerce platform team. Proficiency in React, Node.js, MongoDB, and AWS required. Stripe and WooCommerce integration experience strongly preferred. Must be comfortable with Redux Toolkit, REST APIs, CI/CD, and agile workflows."
    },
    {
        "id": "JOBSEARCH_15",
        "title": "Sr. Software Engineer – Full Stack (PHP/React)",
        "company": "Mimeo Inc.",
        "location": "Remote",
        "posted": "2026-02-27",
        "type": "Full-time",
        "salary": "$120,000 - $150,000/year",
        "url": "https://to.indeed.com/aadssrfljlcv",
        "description": "Mimeo is hiring a Sr. Software Engineer with skills in JavaScript, React.js, PHP, Laravel, and MySQL. Experience with jQuery, WordPress, and Bootstrap is preferred. You will work on document management and print-on-demand systems. REST API design, Git, and Agile experience required."
    },
    {
        "id": "JOBSEARCH_18",
        "title": "Senior Full Stack Developer (Node.js)",
        "company": "ENO8",
        "location": "Remote",
        "posted": "2026-03-04",
        "type": "Full-time",
        "salary": "$100,000 - $130,000/year",
        "url": "https://to.indeed.com/aakg996klpbb",
        "description": "ENO8 needs a Senior Full Stack Developer expert in Node.js, React, Vue.js, and MongoDB. AWS S3, CI/CD pipelines, and Git are required. WooCommerce and PrestaShop knowledge is a strong plus. You will lead feature development and work directly with clients."
    },
    {
        "id": "JOBSEARCH_21",
        "title": "Senior Software Developer – Full-Time Remote",
        "company": "Smart Working Solutions",
        "location": "Remote",
        "posted": "2026-03-04",
        "type": "Full-time",
        "salary": "$90,000 - $120,000/year",
        "url": "https://to.indeed.com/aafw67khtq7j",
        "description": "8+ years of full-stack development required. Core skills: PHP, Laravel, CodeIgniter, React, MySQL, REST APIs, Git. Bootstrap and jQuery for frontend. Python scripting experience is a bonus. You will work on enterprise solutions for US-based clients."
    },
    {
        "id": "JOBSEARCH_19",
        "title": "Sr. Full Stack Engineer – Contract",
        "company": "Red Thread Innovations",
        "location": "Remote",
        "posted": "2026-01-07",
        "type": "Contract",
        "salary": "$60/hour",
        "url": "https://to.indeed.com/aa47b9tyzxtg",
        "description": "3-month contract for a Sr. Full Stack Engineer. Must have solid React.js, Node.js, Express.js, and MySQL or MongoDB experience. PHP and WordPress knowledge is a bonus. AWS experience preferred. You will help build a healthcare SaaS platform from scratch."
    },
]


def calculate_match(job_description):
    skills = RESUME["skills"]
    jd_lower = job_description.lower()
    matched = [s for s in skills if s.lower() in jd_lower]
    missing = [s for s in skills if s.lower() not in jd_lower]
    score = round(len(matched) / len(skills) * 100) if skills else 0
    return {
        "score": score,
        "matched_skills": matched[:12],
        "missing_skills": missing[:8],
        "total_skills": len(skills)
    }


def generate_cover_letter_ai(job_title, company, job_description):
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return {"success": False, "error": "ANTHROPIC_API_KEY not set. Set it as an environment variable to enable AI cover letter generation."}
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        resume_summary = (
            f"Name: {RESUME['name']}\n"
            f"Experience: 10+ years Full Stack Development\n"
            f"Recent Role: Full Stack Developer at Virtual Employee Pvt. Ltd (2020–Present)\n"
            f"Skills: {', '.join(RESUME['skills'][:15])}\n"
            f"Education: B.Tech\n"
            f"Open to relocate: Yes"
        )
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=900,
            messages=[{
                "role": "user",
                "content": (
                    f"Write a professional, compelling cover letter for this job application.\n\n"
                    f"Position: {job_title}\nCompany: {company}\n"
                    f"Job Description: {job_description[:600]}\n\n"
                    f"Candidate Resume:\n{resume_summary}\n\n"
                    f"Requirements: 3 paragraphs, under 260 words, professional tone, "
                    f"highlight matching skills, show enthusiasm for the role. "
                    f"Start with 'Dear Hiring Manager,' and end with 'Sincerely, Maneesh Tiwari'."
                )
            }]
        )
        return {"success": True, "cover_letter": message.content[0].text}
    except Exception as e:
        return {"success": False, "error": str(e)}


def filter_jobs(search="", hours=None, job_type=""):
    results = JOBS[:]
    if search:
        sl = search.lower()
        results = [j for j in results if
                   sl in j["title"].lower() or
                   sl in j["company"].lower() or
                   sl in j["description"].lower()]
    if hours:
        cutoff = datetime.now() - timedelta(hours=int(hours))
        filtered = []
        for j in results:
            try:
                jd = datetime.strptime(j["posted"], "%Y-%m-%d")
                if jd >= cutoff:
                    filtered.append(j)
            except Exception:
                pass
        results = filtered
    if job_type:
        results = [j for j in results if job_type.lower() in j["type"].lower()]
    return results


class JobPortalHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path in ("/", "/job_portal.html"):
            self._serve_file("job_portal.html", "text/html")
        elif path == "/job_portal.css":
            self._serve_file("job_portal.css", "text/css")
        elif path == "/api/jobs":
            jobs = filter_jobs(
                search=qs.get("q", [""])[0],
                hours=qs.get("hours", [""])[0] or None,
                job_type=qs.get("type", [""])[0],
            )
            self._send_json({"jobs": jobs, "total": len(jobs)})
        elif path == "/api/resume":
            self._send_json(RESUME)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}

        if parsed.path == "/api/match":
            self._send_json(calculate_match(body.get("job_description", "")))
        elif parsed.path == "/api/cover-letter":
            self._send_json(generate_cover_letter_ai(
                body.get("job_title", ""),
                body.get("company", ""),
                body.get("job_description", ""),
            ))
        else:
            self.send_response(404)
            self.end_headers()

    def _serve_file(self, filename, content_type):
        try:
            content = (ROOT / filename).read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", f"{content_type}; charset=utf-8")
            self._cors_headers()
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def _send_json(self, data):
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), JobPortalHandler)
    print(f"Job Portal AI running at http://127.0.0.1:{port}")
    server.serve_forever()
