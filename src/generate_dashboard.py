import json
import os
from datetime import datetime

def generate_html(report_data, output_path):
    """Generates a premium HTML dashboard from the drift report data."""
    
    timestamp = report_data.get("timestamp", datetime.now().isoformat())
    features = report_data.get("features", {})
    
    # Header logic for global status
    drift_detected = any(f["status"] == "Drift Detected" for f in features.values())
    status_class = "danger" if drift_detected else "success"
    status_text = "DRIFT DETECTED" if drift_detected else "STABLE"

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ML Data Drift Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-primary: #38bdf8;
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }}

        body {{
            background-color: var(--bg-color);
            color: var(--text-primary);
            padding: 2rem;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 3rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .title-group h1 {{
            font-size: 2rem;
            font-weight: 700;
            letter-spacing: -0.025em;
        }}

        .title-group p {{
            color: var(--text-secondary);
            margin-top: 0.5rem;
        }}

        .global-status {{
            padding: 0.75rem 1.5rem;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            backdrop-filter: blur(8px);
        }}

        .status-danger {{
            background: rgba(239, 68, 68, 0.2);
            color: var(--danger);
            border: 1px solid rgba(239, 68, 68, 0.3);
        }}

        .status-success {{
            background: rgba(16, 185, 129, 0.2);
            color: var(--success);
            border: 1px solid rgba(16, 185, 129, 0.3);
        }}

        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 1.5rem;
        }}

        .card {{
            background: var(--card-bg);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 1rem;
            padding: 1.5rem;
            transition: transform 0.2s ease, border-color 0.2s ease;
            backdrop-filter: blur(12px);
        }}

        .card:hover {{
            transform: translateY(-4px);
            border-color: rgba(56, 189, 248, 0.3);
        }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }}

        .feature-name {{
            font-size: 1.125rem;
            font-weight: 600;
        }}

        .badge {{
            padding: 0.25rem 0.75rem;
            border-radius: 0.5rem;
            font-size: 0.75rem;
            font-weight: 600;
        }}

        .badge-stable {{
            background: rgba(16, 185, 129, 0.1);
            color: var(--success);
        }}

        .badge-drift {{
            background: rgba(239, 68, 68, 0.1);
            color: var(--danger);
        }}

        .metric-row {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.75rem;
            font-size: 0.875rem;
        }}

        .metric-label {{
            color: var(--text-secondary);
        }}

        .metric-value {{
            font-weight: 500;
        }}

        .progress-container {{
            margin-top: 1.5rem;
        }}

        .progress-bar {{
            height: 6px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
            margin-top: 0.5rem;
            overflow: hidden;
        }}

        .progress-fill {{
            height: 100%;
            border-radius: 3px;
        }}

        .fill-stable {{ background: var(--success); }}
        .fill-drift {{ background: var(--danger); }}

        footer {{
            margin-top: 4rem;
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.875rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="title-group">
                <h1>Titanic Data Monitoring</h1>
                <p>Generated at: {timestamp}</p>
            </div>
            <div class="global-status status-{status_class}">
                {status_text}
            </div>
        </header>

        <div class="dashboard-grid">
    """

    for feature, data in features.items():
        is_drift = data["status"] == "Drift Detected"
        badge_class = "badge-drift" if is_drift else "badge-stable"
        fill_class = "fill-drift" if is_drift else "fill-stable"
        
        # Calculate ratio for progress bar (cap at 100%)
        ratio = (data["diff"] / data["threshold"]) * 100
        display_ratio = min(ratio, 100)

        html_content += f"""
            <div class="card">
                <div class="card-header">
                    <span class="feature-name">{feature}</span>
                    <span class="badge {badge_class}">{data["status"]}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Reference Mean</span>
                    <span class="metric-value">{data["ref_mean"]:.3f}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Current Mean</span>
                    <span class="metric-value">{data["current_mean"]:.3f}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Difference</span>
                    <span class="metric-value">{data["diff"]:.3f}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Threshold (Std)</span>
                    <span class="metric-value">{data["threshold"]:.3f}</span>
                </div>
                <div class="progress-container">
                    <div class="metric-row">
                        <span class="metric-label">Drift Impact</span>
                        <span class="metric-value">{ratio:.1f}%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill {fill_class}" style="width: {display_ratio}%"></div>
                    </div>
                </div>
            </div>
        """

    html_content += """
        </div>
        <footer>
            Titanic MLOps Pipeline &bull; Automated Monitoring System
        </footer>
    </div>
</body>
</html>
    """
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Dashboard generated: {output_path}")

if __name__ == "__main__":
    import sys
    report_file = "data/monitoring/latest_report.json"
    output_file = "data/monitoring/monitoring_dashboard.html"
    
    if os.path.exists(report_file):
        with open(report_file, "r") as f:
            data = json.load(f)
        generate_html(data, output_file)
    else:
        print(f"Error: {report_file} not found.")
