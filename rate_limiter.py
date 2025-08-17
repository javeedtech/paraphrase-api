import time
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, max_requests_per_minute: int = 60):
        self.max_requests_per_minute = max_requests_per_minute
        self.requests: Dict[str, List[float]] = {}
        self.window_size = 60  # 1 minute window
    
    def is_allowed(self, client_id: str) -> bool:
        """
        Check if a request is allowed for the given client
        
        Args:
            client_id: Unique identifier for the client (usually IP address)
            
        Returns:
            True if request is allowed, False if rate limit exceeded
        """
        current_time = time.time()
        
        # Initialize client if not exists
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # Clean old requests outside the window
        self._clean_old_requests(client_id, current_time)
        
        # Check if client has exceeded rate limit
        if len(self.requests[client_id]) >= self.max_requests_per_minute:
            logger.warning(f"Rate limit exceeded for client: {client_id}")
            return False
        
        return True
    
    def record_request(self, client_id: str):
        """
        Record a successful request for the client
        
        Args:
            client_id: Unique identifier for the client
        """
        current_time = time.time()
        
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        self.requests[client_id].append(current_time)
        self._clean_old_requests(client_id, current_time)
    
    def _clean_old_requests(self, client_id: str, current_time: float):
        """Remove requests older than the window size"""
        if client_id in self.requests:
            cutoff_time = current_time - self.window_size
            self.requests[client_id] = [
                req_time for req_time in self.requests[client_id] 
                if req_time > cutoff_time
            ]
    
    def get_remaining_requests(self, client_id: str) -> int:
        """Get number of remaining requests for the client"""
        if client_id not in self.requests:
            return self.max_requests_per_minute
        
        current_time = time.time()
        self._clean_old_requests(client_id, current_time)
        
        return max(0, self.max_requests_per_minute - len(self.requests[client_id]))
    
    def get_reset_time(self, client_id: str) -> float:
        """Get timestamp when rate limit resets for the client"""
        if client_id not in self.requests or not self.requests[client_id]:
            return time.time()
        
        oldest_request = min(self.requests[client_id])
        return oldest_request + self.window_size
