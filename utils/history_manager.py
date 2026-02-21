import json
import os
from datetime import datetime
from typing import List, Dict, Any

HISTORY_FILE = "report_history.json"

def save_report(report_data: Dict[str, Any]) -> bool:
    """Save a report to history"""
    try:
        history = load_history()
        
        # Convert datetime to string
        report_copy = report_data.copy()
        if isinstance(report_copy['timestamp'], datetime):
            report_copy['timestamp'] = report_copy['timestamp'].isoformat()
        
        # Ensure all fields are present
        required_fields = ['age', 'gender', 'symptoms', 'type', 'report', 'doctor_type', 'timestamp']
        for field in required_fields:
            if field not in report_copy:
                report_copy[field] = ""
        
        history.append(report_copy)
        
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving report: {e}")
        return False

def load_history() -> List[Dict[str, Any]]:
    """Load report history"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
            
            # Convert timestamps back to datetime
            for report in history:
                if 'timestamp' in report and isinstance(report['timestamp'], str):
                    try:
                        report['timestamp'] = datetime.fromisoformat(report['timestamp'])
                    except:
                        report['timestamp'] = datetime.now()
            
            # Sort by newest first
            history.sort(key=lambda x: x.get('timestamp', datetime.now()), reverse=True)
            return history
        except:
            return []
    return []

def get_all_reports() -> List[Dict[str, Any]]:
    """Get all reports"""
    return load_history()

def clear_all_reports() -> bool:
    """Clear all history"""
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        return True
    except:
        return False