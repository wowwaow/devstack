"""
AI Agent Stack - Event System
"""

from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional, Set
import asyncio
import threading
import queue
import uuid

class EventHandler:
    """Handler for system events"""
    
    def __init__(self, callback: Callable, event_filter: Optional[Dict] = None):
        self.id = str(uuid.uuid4())
        self.callback = callback
        self.event_filter = event_filter or {}
        
    def matches(self, event_data: Dict) -> bool:
        """Check if event matches this handler's filter"""
        if not self.event_filter:
            return True
            
        return all(
            event_data.get(key) == value
            for key, value in self.event_filter.items()
        )

class SystemEventBus:
    """Central event bus for system-wide communication"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SystemEventBus, cls).__new__(cls)
                    cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the event bus"""
        self._handlers = defaultdict(set)  # event_type -> Set[EventHandler]
        self._event_queue = queue.Queue()
        self._start_event_processor()
        
    def _start_event_processor(self):
        """Start the event processing thread"""
        self._processor_thread = threading.Thread(
            target=self._process_events,
            daemon=True
        )
        self._processor_thread.start()
        
    def _process_events(self):
        """Main event processing loop"""
        while True:
            try:
                event_type, event_data = self._event_queue.get()
                self._dispatch_event(event_type, event_data)
                self._event_queue.task_done()
            except Exception as e:
                from agent_stack.core.logging import SystemLogger
                SystemLogger.error(
                    f"Error processing event: {str(e)}",
                    event_type=event_type,
                    event_data=event_data
                )
    
    def _dispatch_event(self, event_type: str, event_data: Dict):
        """Dispatch event to registered handlers"""
        handlers = self._handlers.get(event_type, set())
        
        for handler in handlers:
            if handler.matches(event_data):
                try:
                    handler.callback(event_type, event_data)
                except Exception as e:
                    from agent_stack.core.logging import SystemLogger
                    SystemLogger.error(
                        f"Error in event handler: {str(e)}",
                        handler_id=handler.id,
                        event_type=event_type,
                        event_data=event_data
                    )
    
    @classmethod
    def subscribe(cls, event_type: str, callback: Callable, event_filter: Optional[Dict] = None) -> str:
        """Subscribe to events of a specific type"""
        instance = cls()
        handler = EventHandler(callback, event_filter)
        instance._handlers[event_type].add(handler)
        return handler.id
    
    @classmethod
    def unsubscribe(cls, event_type: str, handler_id: str):
        """Unsubscribe from events"""
        instance = cls()
        handlers = instance._handlers.get(event_type, set())
        handlers = {h for h in handlers if h.id != handler_id}
        instance._handlers[event_type] = handlers
    
    @classmethod
    def emit(cls, event_type: str, event_data: Dict):
        """Emit an event"""
        instance = cls()
        instance._event_queue.put((event_type, event_data))
        
        # Log event
        from agent_stack.core.logging import SystemLogger
        SystemLogger.debug(
            f"Event emitted: {event_type}",
            event_type=event_type,
            event_data=event_data
        )


class AsyncEventBus:
    """Asynchronous event bus for async operations"""
    
    _instance = None
    _lock = asyncio.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AsyncEventBus, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the async event bus"""
        self._handlers = defaultdict(set)
        self._queue = asyncio.Queue()
        
    async def _process_events(self):
        """Process events asynchronously"""
        while True:
            try:
                event_type, event_data = await self._queue.get()
                await self._dispatch_event(event_type, event_data)
                self._queue.task_done()
            except Exception as e:
                from agent_stack.core.logging import SystemLogger
                SystemLogger.error(
                    f"Error processing async event: {str(e)}",
                    event_type=event_type,
                    event_data=event_data
                )
    
    async def _dispatch_event(self, event_type: str, event_data: Dict):
        """Dispatch event to async handlers"""
        handlers = self._handlers.get(event_type, set())
        
        for handler in handlers:
            if handler.matches(event_data):
                try:
                    await handler.callback(event_type, event_data)
                except Exception as e:
                    from agent_stack.core.logging import SystemLogger
                    SystemLogger.error(
                        f"Error in async event handler: {str(e)}",
                        handler_id=handler.id,
                        event_type=event_type,
                        event_data=event_data
                    )
    
    @classmethod
    async def subscribe(cls, event_type: str, callback: Callable, event_filter: Optional[Dict] = None) -> str:
        """Subscribe to async events"""
        instance = cls()
        async with instance._lock:
            handler = EventHandler(callback, event_filter)
            instance._handlers[event_type].add(handler)
            return handler.id
    
    @classmethod
    async def unsubscribe(cls, event_type: str, handler_id: str):
        """Unsubscribe from async events"""
        instance = cls()
        async with instance._lock:
            handlers = instance._handlers.get(event_type, set())
            handlers = {h for h in handlers if h.id != handler_id}
            instance._handlers[event_type] = handlers
    
    @classmethod
    async def emit(cls, event_type: str, event_data: Dict):
        """Emit an async event"""
        instance = cls()
        await instance._queue.put((event_type, event_data))
        
        # Log event
        from agent_stack.core.logging import SystemLogger
        SystemLogger.debug(
            f"Async event emitted: {event_type}",
            event_type=event_type,
            event_data=event_data
        )


# Standard system events
class SystemEvents:
    """Standard system event types"""
    
    # Agent lifecycle events
    AGENT_REGISTERED = "agent_registered"
    AGENT_DEREGISTERED = "agent_deregistered"
    AGENT_STATUS_CHANGED = "agent_status_changed"
    AGENT_HEARTBEAT = "agent_heartbeat"
    AGENT_TIMEOUT = "agent_timeout"
    
    # Task events
    TASK_CREATED = "task_created"
    TASK_ASSIGNED = "task_assigned"
    TASK_STARTED = "task_started"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    TASK_REASSIGNED = "task_reassigned"
    
    # Resource events
    RESOURCE_ALLOCATED = "resource_allocated"
    RESOURCE_RELEASED = "resource_released"
    RESOURCE_CONFLICT = "resource_conflict"
    
    # System events
    SYSTEM_STARTUP = "system_startup"
    SYSTEM_SHUTDOWN = "system_shutdown"
    SYSTEM_ERROR = "system_error"
    SYSTEM_WARNING = "system_warning"
    
    # Objective events
    OBJECTIVE_CREATED = "objective_created"
    OBJECTIVE_COMPLETED = "objective_completed"
    OBJECTIVE_PROMOTED = "objective_promoted"
    
    # Monitoring events
    MONITORING_ALERT = "monitoring_alert"
    PERFORMANCE_THRESHOLD = "performance_threshold"
    RESOURCE_THRESHOLD = "resource_threshold"


# Event utilities
def event_decorator(event_type: str):
    """Decorator to emit events around function calls"""
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Emit pre-event
            SystemEventBus.emit(
                f"{event_type}_started",
                {
                    "function": func.__name__,
                    "args": args,
                    "kwargs": kwargs
                }
            )
            
            try:
                result = func(*args, **kwargs)
                
                # Emit success event
                SystemEventBus.emit(
                    f"{event_type}_completed",
                    {
                        "function": func.__name__,
                        "result": result
                    }
                )
                
                return result
                
            except Exception as e:
                # Emit failure event
                SystemEventBus.emit(
                    f"{event_type}_failed",
                    {
                        "function": func.__name__,
                        "error": str(e)
                    }
                )
                raise
                
        return wrapper
    return decorator


async def async_event_decorator(event_type: str):
    """Decorator to emit async events around async function calls"""
    
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Emit pre-event
            await AsyncEventBus.emit(
                f"{event_type}_started",
                {
                    "function": func.__name__,
                    "args": args,
                    "kwargs": kwargs
                }
            )
            
            try:
                result = await func(*args, **kwargs)
                
                # Emit success event
                await AsyncEventBus.emit(
                    f"{event_type}_completed",
                    {
                        "function": func.__name__,
                        "result": result
                    }
                )
                
                return result
                
            except Exception as e:
                # Emit failure event
                await AsyncEventBus.emit(
                    f"{event_type}_failed",
                    {
                        "function": func.__name__,
                        "error": str(e)
                    }
                )
                raise
                
        return wrapper
    return decorator
