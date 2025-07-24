"""
Code Execution Agent using Google GenAI SDK for secure Python code execution.

This module provides a VertexAI Code Executor that uses Google's Gemini API
with code execution capabilities to run Python code in a secure, sandboxed environment.

## Setup Instructions:

1. Install dependencies:
   pip install google-cloud-aiplatform google-genai python-dotenv

2. Set up authentication:
   gcloud auth application-default login

3. Create a .env file in the src/evo_ai/ directory with:
   PROJECT_ID=your-actual-project-id
   LOCATION=us-central1

4. Enable required APIs in your Google Cloud project:
   - Vertex AI API
   - Generative AI API

## Usage:

    from evo_ai.code_execution_agent import execute_code
    
    result = execute_code('print("Hello, World!")')
    if result['success']:
        print(result['output'])
    else:
        print(result['error'])

## Features:

- Secure Python code execution using Gemini's sandboxed environment
- Built-in safety validation to block potentially dangerous operations
- Automatic error handling and timeout management
- Support for complex Python operations and libraries

## Security:

The code execution environment is sandboxed by Google Cloud and includes
pre-installed libraries like NumPy, Pandas, Matplotlib, etc. However,
basic safety validation is still performed to block obviously dangerous operations.
"""

import json
import logging
import os
import time
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from dotenv import load_dotenv

try:
    from google import genai
    from google.genai.types import Tool, ToolCodeExecution, GenerateContentConfig
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False
    print("Warning: Google Cloud AI Platform not installed. Install with: pip install google-cloud-aiplatform google-genai")

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Get environment variables
PROJECT_ID = os.getenv("PROJECT_ID", "your-project-id")
LOCATION = os.getenv("LOCATION", "us-central1")

# Configure logging
logger = logging.getLogger(__name__)

class VertexAiCodeExecutor:
    """
    A secure Python code executor using Google GenAI SDK.
    Provides sandboxed execution environment for Python code using Gemini's code execution tool.
    """
    
    def __init__(self, project_id: Optional[str] = None, location: str = "us-central1"):
        """
        Initialize the VertexAI Code Executor.
        
        Args:
            project_id: Google Cloud Project ID. If None, will use PROJECT_ID from .env file.
            location: Google Cloud location for Vertex AI services. If None, will use LOCATION from .env file.
        """
        self.project_id = project_id or PROJECT_ID
        self.location = location if location != "us-central1" else LOCATION
        self.initialized = False
        
        if not VERTEX_AI_AVAILABLE:
            logger.error("Google Cloud AI Platform is not available. Cannot initialize VertexAiCodeExecutor.")
            return
            
        try:
            # Validate project_id
            if not self.project_id or self.project_id == "your-project-id":
                logger.warning("No valid project_id provided. Using default 'your-project-id'. Please set PROJECT_ID in .env file or pass project_id parameter.")
            
            # Set environment variables for Vertex AI
            os.environ['GOOGLE_CLOUD_PROJECT'] = self.project_id
            os.environ['GOOGLE_CLOUD_LOCATION'] = self.location
            os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'
            
            # Initialize the GenAI client
            self.client = genai.Client()
            self.model_id = "gemini-2.0-flash-001"
            
            # Create code execution tool
            self.code_execution_tool = Tool(
                code_execution=ToolCodeExecution()
            )
            
            self.initialized = True
            logger.info(f"VertexAI Code Executor initialized for project: {self.project_id}, location: {self.location}")
        except Exception as e:
            logger.error(f"Failed to initialize VertexAI: {e}")
            self.initialized = False

    def execute_python_code(self, code: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Execute Python code using Google GenAI SDK with code execution tool.
        
        Args:
            code: Python code string to execute
            timeout: Maximum execution time in seconds (note: Gemini has a built-in 30s limit)
            
        Returns:
            Dictionary containing execution results, output, and any errors
        """
        if not self.initialized:
            return {
                "success": False,
                "error": "VertexAI Code Executor not properly initialized. Please install google-cloud-aiplatform and configure authentication.",
                "output": "",
                "execution_time": 0
            }
        
        start_time = time.time()
        
        try:
            logger.info("Executing Python code using Google GenAI Code Execution")
            logger.info(f"Code to execute:\n{'-'*50}\n{code}\n{'-'*50}")
            
            # Create a prompt that instructs the model to execute the code
            prompt = f"""Please execute the following Python code and return the results:

```python
{code}
```

Make sure to execute the code and show the output."""

            # Generate content with code execution tool
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=GenerateContentConfig(
                    tools=[self.code_execution_tool],
                    temperature=0.0,
                )
            )
            
            execution_time = time.time() - start_time
            
            # Extract results from the response
            output_text = ""
            execution_results = []
            code_executed = []
            
            for candidate in response.candidates:
                for part in candidate.content.parts:
                    if hasattr(part, 'text') and part.text:
                        output_text += part.text + "\n"
                    elif hasattr(part, 'executable_code') and part.executable_code:
                        code_executed.append({
                            "language": part.executable_code.language,
                            "code": part.executable_code.code
                        })
                    elif hasattr(part, 'code_execution_result') and part.code_execution_result:
                        execution_results.append({
                            "outcome": part.code_execution_result.outcome,
                            "output": part.code_execution_result.output
                        })
            
            # Combine all outputs
            combined_output = output_text
            if execution_results:
                for result in execution_results:
                    if result.get("output"):
                        combined_output += result["output"] + "\n"
            
            # Check if code execution was successful
            # Success can be determined by:
            # 1. Having execution_results with OUTCOME_OK
            # 2. Having output content without execution_results (indicates successful execution)
            success = False
            
            if execution_results:
                # Check if any execution result has OUTCOME_OK
                success = any(
                    str(result.get("outcome")).endswith("OUTCOME_OK") 
                    for result in execution_results
                )
            elif output_text or combined_output:
                # If no execution_results but we have output, consider it successful
                # unless the output contains obvious error indicators
                error_indicators = ["error:", "exception:", "traceback", "failed"]
                has_errors = any(indicator in combined_output.lower() for indicator in error_indicators)
                success = not has_errors
            
            return {
                "success": success,
                "error": "" if success else "Code execution failed or produced errors",
                "output": combined_output.strip(),
                "execution_time": execution_time,
                "code_executed": code,
                "generated_code": code_executed,
                "execution_results": execution_results
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Code execution failed: {str(e)}"
            logger.error(error_msg)
            
            return {
                "success": False,
                "error": error_msg,
                "output": "",
                "execution_time": execution_time,
                "code_executed": code
            }

    def validate_code_safety(self, code: str) -> Tuple[bool, str]:
        """
        Validate if the code is safe to execute.
        Note: Gemini's code execution environment is already sandboxed,
        but we can still do basic validation.
        
        Args:
            code: Python code to validate
            
        Returns:
            Tuple of (is_safe, reason)
        """
        # List of potentially dangerous operations
        dangerous_patterns = [
            '__import__',
            'compile(',
            'exec(',
            'eval(',
        ]
        
        code_lower = code.lower()
        
        for pattern in dangerous_patterns:
            if pattern in code_lower:
                return False, f"Potentially unsafe operation detected: {pattern}"
        
        return True, "Code appears safe for execution"


def execute_code(code: str, project_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Main function to execute Python code using Google GenAI Code Execution.
    
    Args:
        code: Python code string to execute
        project_id: Optional Google Cloud Project ID. If None, will use PROJECT_ID from .env file.
        
    Returns:
        Dictionary containing execution results
    """
    # Use global PROJECT_ID if no project_id provided
    effective_project_id = project_id or PROJECT_ID
    executor = VertexAiCodeExecutor(project_id=effective_project_id)
    
    # Validate code safety first
    is_safe, safety_reason = executor.validate_code_safety(code)
    
    if not is_safe:
        logger.warning(f"Code execution blocked: {safety_reason}")
        return {
            "success": False,
            "error": f"Code execution blocked for safety: {safety_reason}",
            "output": "",
            "execution_time": 0
        }
    
    return executor.execute_python_code(code)


def create_sample_test_code() -> str:
    """
    Create a sample Python code for testing the code executor.
    
    Returns:
        Sample Python code string
    """
    sample_code = """
# Sample Python code for testing VertexAI Code Executor

# Basic calculations
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print("Numbers:", numbers)

# Calculate some statistics
total = sum(numbers)
count = len(numbers)
average = total / count

print(f"Total: {total}")
print(f"Count: {count}")
print(f"Average: {average}")

# Mathematical operations (using built-in functions)
square_root = 25 ** 0.5
print(f"Square root of 25: {square_root}")

# List comprehension
squares = [x**2 for x in numbers]
print(f"Squares: {squares}")

# String operations
message = "Hello from VertexAI Code Executor!"
print(message)
print(f"Message length: {len(message)}")
print(f"Uppercase: {message.upper()}")

# Simple algorithm - find prime numbers
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

primes = [x for x in range(2, 20) if is_prime(x)]
print(f"Prime numbers up to 20: {primes}")

print("Code execution completed successfully!")
"""
    return sample_code


if __name__ == "__main__":
    # Test the code executor with sample code
    print("Testing VertexAI Code Executor")
    print("=" * 50)
    
    # Create sample code
    test_code = create_sample_test_code()
    print("Sample test code:")
    print(test_code)
    print("=" * 50)
    
    # Execute the code
    result = execute_code(test_code)
    
    print("Execution Results:")
    print(f"Success: {result['success']}")
    print(f"Execution Time: {result['execution_time']:.2f} seconds")
    
    if result['success']:
        print("Output:")
        print(result['output'])
    else:
        print("Error:")
        print(result['error']) 