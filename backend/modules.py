from datetime import datetime
from bson import ObjectId

class SystemMetrics:
    def __init__(self, host_name, cpu_usage, memory_usage, disk_usage, timestamp=None):
        self.host_name = host_name
        self.cpu_usage = cpu_usage
        self.memory_usage = memory_usage
        self.disk_usage = disk_usage
        self.timestamp = timestamp or datetime.utcnow()

    def to_dict(self):
        return {
            "host_name": self.host_name,
            "cpu_usage": self.cpu_usage,
            "memory_usage": self.memory_usage,
            "disk_usage": self.disk_usage,
            "timestamp": self.timestamp
        }

class Alert:
    def __init__(self, title, message, severity, source, timestamp=None):
        self.title = title
        self.message = message
        self.severity = severity  # "info", "warning", "critical"
        self.source = source
        self.timestamp = timestamp or datetime.utcnow()
        self.acknowledged = False

    def to_dict(self):
        return {
            "title": self.title,
            "message": self.message,
            "severity": self.severity,
            "source": self.source,
            "timestamp": self.timestamp,
            "acknowledged": self.acknowledged
        }

class User:
    def __init__(self, username, email, password_hash, role="user"):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role  # "admin", "user"
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at
        }