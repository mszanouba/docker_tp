from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

# Base de données en mémoire
tasks = []
task_counter = 0

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Récupérer toutes les tâches"""
    return jsonify({
        'success': True,
        'tasks': tasks,
        'total': len(tasks),
        'completed': sum(1 for t in tasks if t['completed']),
        'pending': sum(1 for t in tasks if not t['completed'])
    })

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Créer une nouvelle tâche"""
    global task_counter
    
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({
            'success': False,
            'error': 'Le texte de la tâche est requis'
        }), 400
    
    task_counter += 1
    task = {
        'id': task_counter,
        'text': data['text'],
        'priority': data.get('priority', 'Moyenne'),
        'completed': False,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'time': datetime.now().strftime("%H:%M")
    }
    
    tasks.append(task)
    
    return jsonify({
        'success': True,
        'task': task,
        'message': 'Tâche créée avec succès'
    }), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Mettre à jour une tâche"""
    data = request.get_json()
    
    for task in tasks:
        if task['id'] == task_id:
            if 'text' in data:
                task['text'] = data['text']
            if 'priority' in data:
                task['priority'] = data['priority']
            if 'completed' in data:
                task['completed'] = data['completed']
            
            return jsonify({
                'success': True,
                'task': task,
                'message': 'Tâche mise à jour'
            })
    
    return jsonify({
        'success': False,
        'error': 'Tâche non trouvée'
    }), 404

@app.route('/api/tasks/<int:task_id>/toggle', methods=['PATCH'])
def toggle_task(task_id):
    """Basculer l'état d'une tâche"""
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            return jsonify({
                'success': True,
                'task': task,
                'message': 'État de la tâche modifié'
            })
    
    return jsonify({
        'success': False,
        'error': 'Tâche non trouvée'
    }), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Supprimer une tâche"""
    global tasks
    
    initial_length = len(tasks)
    tasks = [t for t in tasks if t['id'] != task_id]
    
    if len(tasks) < initial_length:
        return jsonify({
            'success': True,
            'message': 'Tâche supprimée'
        })
    
    return jsonify({
        'success': False,
        'error': 'Tâche non trouvée'
    }), 404

@app.route('/api/tasks/stats', methods=['GET'])
def get_stats():
    """Obtenir les statistiques"""
    priority_count = {
        'Haute': sum(1 for t in tasks if t['priority'] == 'Haute'),
        'Moyenne': sum(1 for t in tasks if t['priority'] == 'Moyenne'),
        'Basse': sum(1 for t in tasks if t['priority'] == 'Basse')
    }
    
    return jsonify({
        'success': True,
        'stats': {
            'total': len(tasks),
            'completed': sum(1 for t in tasks if t['completed']),
            'pending': sum(1 for t in tasks if not t['completed']),
            'by_priority': priority_count
        }
    })

@app.route('/api/tasks/clear', methods=['DELETE'])
def clear_all_tasks():
    """Supprimer toutes les tâches"""
    global tasks, task_counter
    tasks = []
    task_counter = 0
    
    return jsonify({
        'success': True,
        'message': 'Toutes les tâches ont été supprimées'
    })

if __name__ == '__main__':
    print("🚀 API démarrée sur http://localhost:5000")
    print("📋 Endpoints disponibles:")
    print("   GET    /api/tasks          - Liste des tâches")
    print("   POST   /api/tasks          - Créer une tâche")
    print("   PUT    /api/tasks/<id>     - Modifier une tâche")
    print("   PATCH  /api/tasks/<id>/toggle - Basculer l'état")
    print("   DELETE /api/tasks/<id>     - Supprimer une tâche")
    print("   GET    /api/tasks/stats    - Statistiques")
    print("   DELETE /api/tasks/clear    - Tout supprimer")
    app.run(debug=True, port=5000)