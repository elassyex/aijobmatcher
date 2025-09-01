# Job Match Analyzer (AI-Powered)

This is a **Django-based web application** that analyzes a candidate's skills and experience against a given job role using an AI model (e.g., Google Gemini API).  
It returns a **match percentage**, **matching skills**, **missing skills**, and **recommendations** to help candidates understand how well they fit the role.

---

## **Features**
- 🔍 **AI-Powered Job Matching** — Analyze skills dynamically using Google Gemini API.  
- ⚡ **Instant Results** — Sends requests via AJAX without page reload.  
- 📊 **Detailed Feedback** — Match percentage, matched skills, and missing skills.  
- 🎨 **Simple UI** — Easy-to-use form interface with responsive design.  
- 🔒 **Secure** — API keys managed via `.env` for safety.

---

## **Tech Stack**
- **Backend**: Django (Python 3.9+)  
- **Frontend**: HTML, CSS, JavaScript (Fetch API for AJAX requests)  
- **Database**: SQLite (default), can switch to PostgreSQL or MySQL  
- **AI API**: Google Gemini API  

---

## **Setup Instructions**

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/job-match-analyzer.git
cd job-match-analyzer
```

### 2️⃣ Create and activate a virtual environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Add your API key to `.env`
Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_google_ai_studio_key_here
```

### 5️⃣ Apply database migrations
```bash
python manage.py migrate
```

### 6️⃣ Run the development server
```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** in your browser.

---

## **Project Structure**
```
job_match_analyzer/
│
├── analyzer/                # Main Django app
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   │   └── index.html       # Main frontend page
│   ├── static/              # Static assets (CSS, JS, images)
│   ├── ai_analyzer.py       # Core AI logic for job matching
│   ├── models.py            # Database models
│   ├── views.py             # Django views and API endpoints
│   └── urls.py              # App-specific routes
│
├── job_match_analyzer/      # Project configuration
│   └── settings.py          # Settings (reads API key from .env)
│
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── README.md                # Documentation
```

---

## **Example Request**
```json
{
  "success": true,
  "result": {
    "match_percentage": 82.5,
    "matching_skills": ["Python", "Django"],
    "missing_skills": ["Docker", "Celery"],
    "recommendations": "Learn Docker and Celery for better performance."
  }
}
```

---

## **Environment Variables**
| Variable | Description |
|-----------|-------------|
| `GOOGLE_API_KEY` | Your Google AI Studio API Key |

---

## **Deployment**
For production deployment:
- Use **PostgreSQL** for a robust database.  
- Run with **Gunicorn + Nginx** or **Django’s ASGI** setup.  
- Set `DEBUG=False` in `settings.py`.

---

## **To-Do**
- [ ] Improve AI prompt engineering for higher accuracy.  
- [ ] Add user authentication and profile saving.  
- [ ] Build a dashboard for historical analysis results.  
- [ ] Write automated tests for models and API calls.

---

## **License**
This project is licensed under the MIT License.  
Feel free to modify and distribute.

---

## **Author**
**Mohamed Elassy**  
- GitHub: [@your-username](https://github.com/your-username)  
- Email: your-email@example.com
