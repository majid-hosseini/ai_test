import asyncio
import dataclasses
import logging
import os
import re
import time
import requests
from pathlib import Path
import vertexai
from dotenv import load_dotenv
from .utils import with_logging

from .workspace_rag.rag_engine import RAGEngine

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Get environment variables
PROJECT_ID = os.getenv("PROJECT_ID", "your-project-id")
LOCATION = os.getenv("LOCATION", "us-central1")

vertexai.init(project=PROJECT_ID, location=LOCATION)

DEFAULT_RESOURCE_ID = 'workspace__all'

@with_logging
def init_workspace_rag_engine(gcp_resource_id: str):
    try:
        rag_engine = RAGEngine(gcp_resource_id)
        if rag_engine.has_corpus():
            logging.info(f"Initialized RAG engine {gcp_resource_id}")
        else:
            rag_engine = RAGEngine(DEFAULT_RESOURCE_ID)
            if rag_engine.has_corpus():
                logging.info(f"Initialized default RAG engine {DEFAULT_RESOURCE_ID}")

        return rag_engine
    except Exception as e:
        logging.error(f"Failed to initialize RAG engine: {e}", exc_info=True)
        return None