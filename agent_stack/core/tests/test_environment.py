#!/usr/bin/env python3

import os
import json
import time
from pathlib import Path

class WarpEnvironment:
    """Test class demonstrating Warp environment usage"""
    
    def __init__(self):
        self.validate_environment()
        
    def validate_environment(self):
        """Validate required environment variables"""
        required_vars = [
            'WARP_HOST_DIR',
            'WARP_SYSTEM_DIR',
            'SYSTEM_DIR',
            'SYSTEM_LOGS_DIR',
            'AGENT_STATUS_DIR'
        ]
        
        missing = [var for var in required_vars if not os.environ.get(var)]
        if missing:
            raise EnvironmentError(f"Missing required environment variables: {missing}")
            
    def test_directory_access(self):
        """Test access to key system directories"""
        directories = {
            'System Logs': os.environ['SYSTEM_LOGS_DIR'],
            'Agent Status': os.environ['AGENT_STATUS_DIR'],
            'Task Pool': os.environ['TASK_POOL_DIR'],
            'Current Objective': os.environ['CURRENT_OBJECTIVE_DIR']
        }
        
        results = {}
        for name, path in directories.items():
            dir_path = Path(path)
            results[name] = {
                'exists': dir_path.exists(),
                'is_dir': dir_path.is_dir(),
                'writable': os.access(path, os.W_OK),
                'readable': os.access(path, os.R_OK)
            }
        return results
        
    def test_file_operations(self):
        """Test file operations using environment paths"""
        test_file = os.path.join(os.environ['SYSTEM_LOGS_DIR'], 'environment_test.log')
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            # Write test
            with open(test_file, 'w') as f:
                f.write(f"Environment test at {timestamp}\n")
            
            # Read test
            with open(test_file, 'r') as f:
                content = f.read().strip()
            
            return {
                'success': True,
                'message': 'File operations successful',
                'content': content
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
            
    def test_agent_status(self):
        """Test agent status file operations"""
        agent_id = f"test_agent_{int(time.time())}"
        status_file = os.path.join(os.environ['AGENT_STATUS_DIR'], f"{agent_id}.json")
        
        status_data = {
            'agent_id': agent_id,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'TESTING',
            'environment_valid': True
        }
        
        try:
            # Write status
            with open(status_file, 'w') as f:
                json.dump(status_data, f, indent=2)
            
            # Read status
            with open(status_file, 'r') as f:
                read_data = json.load(f)
            
            # Cleanup
            os.remove(status_file)
            
            return {
                'success': True,
                'message': 'Agent status operations successful',
                'data': read_data
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }

def run_tests():
    """Run all environment tests"""
    try:
        env = WarpEnvironment()
        
        results = {
            'environment_validation': 'PASS',
            'directory_access': env.test_directory_access(),
            'file_operations': env.test_file_operations(),
            'agent_status': env.test_agent_status()
        }
        
        print("\n=== Warp Environment Test Results ===\n")
        print(json.dumps(results, indent=2))
        print("\nAll tests completed successfully!")
        
    except Exception as e:
        print(f"\nTest failed: {str(e)}")
        raise

if __name__ == '__main__':
    run_tests()
