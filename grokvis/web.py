"""
Web dashboard functionality for GrokVIS.
Provides a Flask-based web interface for monitoring and control.
"""
import logging
from flask import Flask, render_template_string

# Import from core module
from grokvis.core import scheduler

# Flask app setup
app = Flask(__name__)

@app.route('/')
def dashboard():
    """Render the GROK-VIS dashboard."""
    try:
        # Fetch scheduled jobs
        jobs = scheduler.get_jobs()
        scheduled_tasks = [(job.next_run_time.strftime('%Y-%m-%d %H:%M'), job.args[0]) for job in jobs]

        # Fetch recent commands
        try:
            with open("command_log.txt", "r") as f:
                commands = f.readlines()[-10:]  # Last 10 commands
        except FileNotFoundError:
            commands = ["No commands logged yet"]

        html = """
        <!DOCTYPE html>
        <html>
            <head>
                <title>GROK-VIS Dashboard</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 20px;
                        background-color: #f5f5f5;
                    }
                    h1 {
                        color: #333;
                        border-bottom: 2px solid #ddd;
                        padding-bottom: 10px;
                    }
                    h2 {
                        color: #555;
                        margin-top: 20px;
                    }
                    ul {
                        background-color: white;
                        border-radius: 5px;
                        padding: 15px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }
                    li {
                        margin-bottom: 8px;
                        padding: 5px;
                        border-bottom: 1px solid #eee;
                    }
                    .container {
                        max-width: 800px;
                        margin: 0 auto;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>GROK-VIS Control Panel</h1>
                    <h2>Scheduled Tasks</h2>
                    <ul>
                        {% if tasks %}
                            {% for time, task in tasks %}
                                <li>{{ time }} - {{ task }}</li>
                            {% endfor %}
                        {% else %}
                            <li>No scheduled tasks</li>
                        {% endif %}
                    </ul>
                    <h2>Recent Commands</h2>
                    <ul>
                        {% for cmd in commands %}
                            <li>{{ cmd }}</li>
                        {% endfor %}
                    </ul>
                </div>
            </body>
        </html>
        """
        return render_template_string(html, tasks=scheduled_tasks, commands=commands)
    except Exception as e:
        logging.error(f"Dashboard Error: {e}")
        return "Error loading dashboard."

@app.route('/health')
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "version": "1.0.0"}

@app.route('/stats')
def system_stats():
    """Display system statistics."""
    try:
        import psutil
        import pynvml
        
        # CPU stats
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # GPU stats
        try:
            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            gpu_util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            gpu_percent = gpu_util.gpu
            gpu_memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
            gpu_memory_percent = (gpu_memory.used / gpu_memory.total) * 100
        except:
            gpu_percent = "N/A"
            gpu_memory_percent = "N/A"
        
        html = """
        <!DOCTYPE html>
        <html>
            <head>
                <title>GROK-VIS System Stats</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 20px;
                        background-color: #f5f5f5;
                    }
                    h1 {
                        color: #333;
                        border-bottom: 2px solid #ddd;
                        padding-bottom: 10px;
                    }
                    .container {
                        max-width: 800px;
                        margin: 0 auto;
                    }
                    .stat-box {
                        background-color: white;
                        border-radius: 5px;
                        padding: 15px;
                        margin-bottom: 15px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }
                    .stat-title {
                        font-weight: bold;
                        margin-bottom: 5px;
                    }
                    .progress-bar {
                        height: 20px;
                        background-color: #e0e0e0;
                        border-radius: 10px;
                        margin-top: 5px;
                    }
                    .progress-fill {
                        height: 100%;
                        background-color: #4CAF50;
                        border-radius: 10px;
                        text-align: center;
                        line-height: 20px;
                        color: white;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>System Statistics</h1>
                    
                    <div class="stat-box">
                        <div class="stat-title">CPU Usage</div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {{ cpu_percent }}%">
                                {{ cpu_percent }}%
                            </div>
                        </div>
                    </div>
                    
                    <div class="stat-box">
                        <div class="stat-title">Memory Usage</div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {{ memory_percent }}%">
                                {{ memory_percent }}%
                            </div>
                        </div>
                    </div>
                    
                    <div class="stat-box">
                        <div class="stat-title">GPU Usage</div>
                        {% if gpu_percent != "N/A" %}
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {{ gpu_percent }}%">
                                {{ gpu_percent }}%
                            </div>
                        </div>
                        {% else %}
                        <p>No GPU detected or NVIDIA GPU required</p>
                        {% endif %}
                    </div>
                    
                    <div class="stat-box">
                        <div class="stat-title">GPU Memory</div>
                        {% if gpu_memory_percent != "N/A" %}
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {{ gpu_memory_percent }}%">
                                {{ gpu_memory_percent|round(1) }}%
                            </div>
                        </div>
                        {% else %}
                        <p>No GPU detected or NVIDIA GPU required</p>
                        {% endif %}
                    </div>
                </div>
            </body>
        </html>
        """
        return render_template_string(
            html, 
            cpu_percent=cpu_percent, 
            memory_percent=memory_percent,
            gpu_percent=gpu_percent,
            gpu_memory_percent=gpu_memory_percent
        )
    except Exception as e:
        logging.error(f"Stats Error: {e}")
        return "Error loading system statistics."