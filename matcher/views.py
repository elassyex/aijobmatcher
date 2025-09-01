from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json,os
from .ai_analyzer import JobMatchAnalyzer

@csrf_exempt
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def analyze_job_match(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_skills = data.get('skills', [])
            job_role = data.get('job_role', '')
            experience = data.get('experience', '0-1')
            from dotenv import load_dotenv
            load_dotenv()
            GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
            print(GOOGLE_API_KEY)
            analyzer = JobMatchAnalyzer()
            result = analyzer.analyze_match(user_skills, job_role, experience)
            print(job_role)
            print("LLM Result:", result)  # Debug output
            return JsonResponse({'success': True, 'result': result})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})