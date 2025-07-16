from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

project_data = {
  
}

@app.route('/')
def home():
    """Serve the main HTML page"""
    return jsonify({
        "message": "SkillPilot API is running!",
        "endpoints": {
            "projects": "/api/projects (POST)",
            "all_projects": "/api/all-projects (GET)",
            "technologies": "/api/technologies (GET)",
            "stats": "/api/stats (GET)",
            "health": "/health (GET)"
        }
    })

@app.route('/api/projects', methods=['POST', 'OPTIONS'])
def get_projects():
    """
    Get project suggestions based on tech stack
    Expects: {"tech_stack": ["python", "javascript", "html"]}
    Returns: {"easy": [...], "moderate": [...], "difficult": [...]}
    """
    if request.method == 'OPTIONS':
  
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        tech_stack = [tech.lower().strip() for tech in data.get('tech_stack', [])]
        
        if not tech_stack:
            return jsonify({"error": "Tech stack is required"}), 400
        
        result = {}
        
        for difficulty in ['easy', 'moderate', 'difficult']:
            matching_projects = []
            
            for project in project_data[difficulty]:
             
                if any(tech in project['tech'] for tech in tech_stack):
                    matching_tech = [tech for tech in project['tech'] if tech in tech_stack]
                    
                    project_copy = project.copy()
                    project_copy['matching_tech'] = matching_tech
                    matching_projects.append(project_copy)
            
            result[difficulty] = matching_projects
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/all-projects', methods=['GET'])
def get_all_projects():
    """
    Get all projects without filtering
    Returns: {"easy": [...], "moderate": [...], "difficult": [...]}
    """
    return jsonify(project_data)

@app.route('/api/technologies', methods=['GET'])
def get_technologies():
    """
    Get list of all available technologies
    Returns: {"technologies": ["python", "javascript", ...]}
    """
    all_tech = set()
    
    for difficulty in project_data:
        for project in project_data[difficulty]:
            all_tech.update(project['tech'])
    
    return jsonify({"technologies": sorted(list(all_tech))})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Get statistics about available projects
    Returns: {"total_projects": 28, "by_difficulty": {...}, "technologies_count": 6}
    """
    stats = {
        "total_projects": sum(len(projects) for projects in project_data.values()),
        "by_difficulty": {
            difficulty: len(projects) 
            for difficulty, projects in project_data.items()
        }
    }
    
    all_tech = set()
    for difficulty in project_data:
        for project in project_data[difficulty]:
            all_tech.update(project['tech'])
    
    stats["technologies_count"] = len(all_tech)
    stats["available_technologies"] = sorted(list(all_tech))
    
    return jsonify(stats)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Project Ideas API is running"})

if __name__ == '__main__':
    print("🚀 SkillPilot API Starting...")
    print("📡 API will be available at: http://localhost:5000")
    print("🔧 Available endpoints:")
    print("   GET  /                 - API info")
    print("   POST /api/projects     - Get project suggestions")
    print("   GET  /api/all-projects - Get all projects")
    print("   GET  /api/technologies - Get all technologies")
    print("   GET  /api/stats        - Get API statistics")
    print("   GET  /health           - Health check")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5002)
