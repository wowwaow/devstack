"""
AI Agent Stack - Logging System
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

class SystemLogger:
    """Centralized logging system for AI Agent Stack"""
    
    _instance = None
    _loggers = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SystemLogger, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the logging system"""
        self.base_log_path = Path("logs")
        self.system_log_path = self.base_log_path / "system_logs"
        self.work_log_path = self.base_log_path / "work_logs"
        
        # Ensure log directories exist
        self.system_log_path.mkdir(parents=True, exist_ok=True)
        self.work_log_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize different log types
        self._setup_system_logger()
        self._setup_agent_logger()
        self._setup_task_logger()
        self._setup_error_logger()
        
    def _setup_system_logger(self):
        """Setup the main system logger"""
        logger = logging.getLogger("system")
        logger.setLevel(logging.INFO)
        
        # File handler for system logs
        system_handler = logging.FileHandler(
            self.system_log_path / "system.log"
        )
        system_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s"
            )
        )
        logger.addHandler(system_handler)
        
        # JSON handler for structured logging
        json_handler = logging.FileHandler(
            self.system_log_path / "system.json"
        )
        json_handler.setFormatter(
            JsonFormatter()
        )
        logger.addHandler(json_handler)
        
        self._loggers["system"] = logger
        
    def _setup_agent_logger(self):
        """Setup the agent activity logger"""
        logger = logging.getLogger("agent")
        logger.setLevel(logging.INFO)
        
        # File handler for agent logs
        agent_handler = logging.FileHandler(
            self.system_log_path / "agent_activity.log"
        )
        agent_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [AGENT:%(agent_id)s] %(message)s"
            )
        )
        logger.addHandler(agent_handler)
        
        # JSON handler for structured logging
        json_handler = logging.FileHandler(
            self.system_log_path / "agent_activity.json"
        )
        json_handler.setFormatter(
            JsonFormatter()
        )
        logger.addHandler(json_handler)
        
        self._loggers["agent"] = logger
        
    def _setup_task_logger(self):
        """Setup the task execution logger"""
        logger = logging.getLogger("task")
        logger.setLevel(logging.INFO)
        
        # File handler for task logs
        task_handler = logging.FileHandler(
            self.work_log_path / "task_execution.log"
        )
        task_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [TASK:%(task_id)s] %(message)s"
            )
        )
        logger.addHandler(task_handler)
        
        # JSON handler for structured logging
        json_handler = logging.FileHandler(
            self.work_log_path / "task_execution.json"
        )
        json_handler.setFormatter(
            JsonFormatter()
        )
        logger.addHandler(json_handler)
        
        self._loggers["task"] = logger
        
    def _setup_error_logger(self):
        """Setup the error logger"""
        logger = logging.getLogger("error")
        logger.setLevel(logging.ERROR)
        
        # File handler for error logs
        error_handler = logging.FileHandler(
            self.system_log_path / "errors.log"
        )
        error_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s\nContext: %(context)s\n"
            )
        )
        logger.addHandler(error_handler)
        
        # JSON handler for structured logging
        json_handler = logging.FileHandler(
            self.system_log_path / "errors.json"
        )
        json_handler.setFormatter(
            JsonFormatter()
        )
        logger.addHandler(json_handler)
        
        self._loggers["error"] = logger
    
    @classmethod
    def system_log(cls, level: str, message: str, **kwargs):
        """Log a system message"""
        instance = cls()
        logger = instance._loggers["system"]
        
        log_func = getattr(logger, level.lower())
        log_func(message, extra=kwargs)
        
    @classmethod
    def agent_log(cls, agent_id: str, message: str, level: str = "info", **kwargs):
        """Log an agent activity"""
        instance = cls()
        logger = instance._loggers["agent"]
        
        kwargs["agent_id"] = agent_id
        log_func = getattr(logger, level.lower())
        log_func(message, extra=kwargs)
        
    @classmethod
    def task_log(cls, task_id: str, message: str, level: str = "info", **kwargs):
        """Log a task execution message"""
        instance = cls()
        logger = instance._loggers["task"]
        
        kwargs["task_id"] = task_id
        log_func = getattr(logger, level.lower())
        log_func(message, extra=kwargs)
        
    @classmethod
    def error_log(cls, error: Exception, context: Dict[str, Any], **kwargs):
        """Log an error with context"""
        instance = cls()
        logger = instance._loggers["error"]
        
        kwargs["context"] = json.dumps(context, default=str)
        logger.error(str(error), extra=kwargs)
        
    @classmethod
    def debug(cls, message: str, **kwargs):
        """Log a debug message"""
        cls.system_log("debug", message, **kwargs)
        
    @classmethod
    def info(cls, message: str, **kwargs):
        """Log an info message"""
        cls.system_log("info", message, **kwargs)
        
    @classmethod
    def warning(cls, message: str, **kwargs):
        """Log a warning message"""
        cls.system_log("warning", message, **kwargs)
        
    @classmethod
    def error(cls, message: str, **kwargs):
        """Log an error message"""
        cls.system_log("error", message, **kwargs)
        
    @classmethod
    def critical(cls, message: str, **kwargs):
        """Log a critical message"""
        cls.system_log("critical", message, **kwargs)


class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format the log record as JSON"""
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name
        }
        
        # Add extra fields from record
        if hasattr(record, "agent_id"):
            log_data["agent_id"] = record.agent_id
        if hasattr(record, "task_id"):
            log_data["task_id"] = record.task_id
        if hasattr(record, "context"):
            log_data["context"] = record.context
            
        # Add any additional fields from record.__dict__
        for key, value in record.__dict__.items():
            if key not in ["timestamp", "level", "message", "logger", "agent_id", "task_id", "context"] and \
               not key.startswith("_") and \
               isinstance(value, (str, int, float, bool, list, dict)):
                log_data[key] = value
                
        return json.dumps(log_data, default=str)


class LogRotator:
    """Handle log rotation and archival"""
    
    @classmethod
    def rotate_logs(cls, max_size_mb: int = 100, max_files: int = 5):
        """Rotate logs based on size"""
        instance = SystemLogger()
        
        for log_dir in [instance.system_log_path, instance.work_log_path]:
            for log_file in log_dir.glob("*.log"):
                cls._rotate_file(log_file, max_size_mb, max_files)
                
    @classmethod
    def _rotate_file(cls, file_path: Path, max_size_mb: int, max_files: int):
        """Rotate a single log file"""
        if not file_path.exists():
            return
            
        # Check if file exceeds max size
        if file_path.stat().st_size > max_size_mb * 1024 * 1024:
            # Remove oldest rotation if it exists
            oldest = file_path.with_suffix(f".log.{max_files}")
            if oldest.exists():
                oldest.unlink()
                
            # Rotate existing backups
            for i in range(max_files - 1, 0, -1):
                current = file_path.with_suffix(f".log.{i}")
                if current.exists():
                    current.rename(file_path.with_suffix(f".log.{i+1}"))
                    
            # Rotate current log
            file_path.rename(file_path.with_suffix(".log.1"))
            
            # Create new empty log file
            file_path.touch()


class LogAnalyzer:
    """Analyze log files for patterns and issues"""
    
    @classmethod
    def analyze_errors(cls, time_window_minutes: Optional[int] = None) -> Dict:
        """Analyze error logs for patterns"""
        instance = SystemLogger()
        error_log = instance.system_log_path / "errors.json"
        
        if not error_log.exists():
            return {}
            
        error_patterns = {}
        current_time = datetime.now()
        
        with open(error_log) as f:
            for line in f:
                try:
                    log_entry = json.loads(line)
                    
                    # Apply time window filter if specified
                    if time_window_minutes:
                        log_time = datetime.fromisoformat(log_entry["timestamp"])
                        if (current_time - log_time).total_seconds() / 60 > time_window_minutes:
                            continue
                            
                    # Group errors by type
                    error_type = log_entry.get("error_type", "unknown")
                    if error_type not in error_patterns:
                        error_patterns[error_type] = {
                            "count": 0,
                            "examples": []
                        }
                        
                    error_patterns[error_type]["count"] += 1
                    if len(error_patterns[error_type]["examples"]) < 3:
                        error_patterns[error_type]["examples"].append(log_entry)
                        
                except json.JSONDecodeError:
                    continue
                    
        return error_patterns
    
    @classmethod
    def analyze_agent_activity(cls, agent_id: Optional[str] = None) -> Dict:
        """Analyze agent activity patterns"""
        instance = SystemLogger()
        agent_log = instance.system_log_path / "agent_activity.json"
        
        if not agent_log.exists():
            return {}
            
        activity_patterns = {}
        
        with open(agent_log) as f:
            for line in f:
                try:
                    log_entry = json.loads(line)
                    
                    # Filter by agent if specified
                    if agent_id and log_entry.get("agent_id") != agent_id:
                        continue
                        
                    # Group by activity type
                    activity_type = log_entry.get("activity_type", "unknown")
                    if activity_type not in activity_patterns:
                        activity_patterns[activity_type] = {
                            "count": 0,
                            "latest": None
                        }
                        
                    activity_patterns[activity_type]["count"] += 1
                    activity_patterns[activity_type]["latest"] = log_entry
                    
                except json.JSONDecodeError:
                    continue
                    
        return activity_patterns
