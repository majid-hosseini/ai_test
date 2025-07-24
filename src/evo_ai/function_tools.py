"""
Function tools for the Evo AI Agent following Google ADK specification.
"""

import json
import logging
import re
import os
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime



from .llm_utils import (
    get_list_of_objects_from_api, 
    get_object_versions_info_from_api, 
    get_objects_info_from_api, 
    generate_llm_response, 
    get_object_id, 
    download_table_data_from_api,
    extract_object_and_attribute,
    create_dataframe_from_fake_data,
    generate_simple_chart,
    create_error_figure,
    save_chart_file
)
from .rag_utils import init_workspace_rag_engine

# Configure logging to both console and file
logger = logging.getLogger(__name__)

# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Configure file handler
file_handler = logging.FileHandler(logs_dir / "evo_ai.log")
file_handler.setLevel(logging.INFO)

# Configure console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

# Initialize the RAG engine
gcp_resource_id = "workspace_Thalanga demo complete_f4cfac01-21ef-4f3b-8c0c-26b97fa7303e"
rag_engine = init_workspace_rag_engine(gcp_resource_id)


async def download_assay_data(object_name: str, collections_attribute: Optional[str] = None) -> List[float]:
    """
    Call this function when the table data of a collections attribute of an object is requested; such as:
    - download the gold assay of thalanga_local_drillholes_dt
    - download the ALT1_INTENSITY of thalanga_local_drillholes_dt
    - Download the gold, silver and formation of thalanga_local_drillholes_e_sm

    Args:
        object_name (str): The name of the object.
        collections_attribute (Optional[str]): The user's requested collections attribute.
            - Examples: copper, gold, silver, etc.

    Returns:
        List[float]: A list of float values representing the assay data.
    """
    
    logger.info(f"Downloading assay data for object: {object_name}, attribute: {collections_attribute}")
    
    api_response = await download_table_data_from_api(object_name, collections_attribute)
    
    logger.info(f"Successfully downloaded assay data with {len(api_response)} values")
    
    return api_response


def generate_chart(user_prompt: str) -> Dict[str, Any]:
    """
    Generate a chart plot for the data to be displayed in the app. For any request relating to chart or plot such as:
    - plot the gold assay of thalanga_local_drillholes_dt
    - plot the histogram of gold
    - cap the value of the plot to a maximum of 5
    - change the number of bins in the plot to 20
    - create a scatter plot of gold vs copper
    - show a box plot of silver values

    Args:
        user_prompt (str): The user's request for generating a chart.

    Returns:
        Dict[str, Any]: A dictionary containing chart details and file paths (JSON-serializable).
    """
    logger.info(f"Generating chart for user prompt: {user_prompt}")
    
    try:
        # Extract object name and attribute from user prompt
        object_name, attribute_name = extract_object_and_attribute(user_prompt)
        
        # Get data from our structured fake data
        df = create_dataframe_from_fake_data(object_name, attribute_name, user_prompt)
        
        logger.info(f"Created dataframe with shape: {df.shape}")
        logger.info(f"Dataframe columns: {list(df.columns)}")
        
        # Generate the chart using secure VertexAI code execution
        plotly_figure = generate_simple_chart(df, user_prompt, attribute_name)

        # Save the chart file (PNG only)
        png_filename = save_chart_file(plotly_figure, user_prompt)
        
        # Prepare chart information (all JSON-serializable)
        chart_info = {
            "chart_type": "plotly.graph_objects.Figure",
            "data_shape": list(df.shape),
            "columns_used": list(df.columns),
            "user_request": user_prompt,
            "object_name": object_name,
            "attribute_name": attribute_name,
            "png_file": png_filename,
            "data_points": len(df),
            "success": True
        }
        
        logger.info(f"Successfully generated and saved chart: {chart_info}")
        
        return {
            "chart_info": chart_info,
            "success": True,
            "message": f"Chart generated successfully for {object_name}.{attribute_name}! File saved: {png_filename}",
            "png_path": png_filename,
            "data_points": len(df),
            "columns_count": len(df.columns)
        }
        
    except Exception as e:
        logger.error(f"Error generating chart: {e}")
        return {
            "chart_info": None,
            "success": False,
            "error": str(e),
            "message": f"Error generating chart: {str(e)}",
            "png_path": None,
            "data_points": 0,
            "columns_count": 0
        }



async def get_list_of_objects() -> List[str]:
    """
    Get the list of all available objects in the workspace, only including the latest version of each object,
    their creation dates, and the users who created the objects. Also to answer questions like:
    - What are the objects in the workspace?
    - How many downhole collection objects do I have?
    - What are the names of the downhole collection objects?
    
    Returns:
        List[str]: A list of objects in the workspace with their metadata.
    """
    
    logger.info("Getting list of objects from workspace")
    
    # Call the placeholder API function
    api_response = await get_list_of_objects_from_api(all_versions=False)
    
    logger.info(f"Retrieved {len(api_response)} objects from workspace (fake data)")
    
    return api_response


async def get_list_of_objects_all_versions() -> List[str]:
    """
    Get the list of all available objects in the workspace, including details on the number of versions each object has,
    their creation dates, and the users who created the objects or their versions.
    
    Returns:
        List[str]: A list of objects in the workspace with all versions and their metadata.
    """
    
    logger.info("Getting list of objects with all versions from workspace")
    
    # Call the placeholder API function
    api_response = await get_list_of_objects_from_api(all_versions=True)
    
    logger.info(f"Retrieved {len(api_response)} objects with all versions from workspace (fake data)")
    
    return api_response


async def get_objects_info(object_names: List[str]) -> List[Dict[str, Any]]:
    """
    Call this function whenever the user requests to describe one or more objects or tell me about them or compare objects.
    Get detailed information (assays, bounding box, dimensions) for one or more objects in the workspace, including what assays 
    (metals or elements) are available and attributes such as bounding box, collections, any specific metal or element, location, 
    distances, dimensions (length, width, depth), as well as holes and intervals.
    This function should be called whenever the user requests information about one or more objects.
    
    Args:
        object_names (List[str]): List of object names to get detailed information for.
        
    Returns:
        List[Dict[str, Any]]: Detailed information about the requested objects.
    """
    
    logger.info(f"Getting detailed information for objects: {object_names}")
    
    # Call the placeholder API function
    api_response = await get_objects_info_from_api(object_names)
    
    logger.info(f"Retrieved detailed information for {len(api_response)} objects (fake data)")
    
    return api_response


async def get_object_versions_info(object_names: List[str]) -> List[Dict[str, Any]]:
    """
    Get detailed version information for one or more objects in the workspace, including version history, 
    changes made in each version, file sizes, data quality metrics, and validation status.
    This function should be called when the user requests information about object versions, version history,
    or wants to compare different versions of objects.
    
    Args:
        object_names (List[str]): List of object names to get version information for.
        
    Returns:
        List[Dict[str, Any]]: Detailed version information for the requested objects.
    """
    
    logger.info(f"Getting version information for objects: {object_names}")
    
    # Call the placeholder API function
    api_response = await get_object_versions_info_from_api(object_names)
    
    logger.info(f"Retrieved version information for {len(api_response)} objects (fake data)")
    
    return api_response


async def get_rag_info(query: str) -> str:
    """
    This function is triggered when the user wants to know more about the **geological context** of an object or a term.
    It retrieves additional domain-specific information to clarify vague or generic requests.
    This function serves as a fallback option and should be called whenever none of the above functions are relevant to the user's query.

    This function is triggered when the user input lacks specificity or if none of the other tools in the tools list
    can adequately address the query. It helps seek relevant context to interpret the user's request accurately.

    ### Example User Inputs:
    - What is the definition of **downhole-collection**? What does Data origin: Drill core logging refer to? What does Method of Measurement: Visual inspection and description mean?
    - Can you explain what a **pointset** is in this context?
    - What does **assay interval** mean?

    Args:
        query (str): The user query requiring clarification or additional context.

    Returns:
        str: The response from the domain-specific information API.
    """
    
    logger.info(f"Getting RAG information for query: {query}")

    if not rag_engine.has_corpus():
        return "Workspace has no associated corpus."
    
    retrieved_context = rag_engine.query(query)

    conditional_RAG_prompt = f"""
    Your task is to answer a question.
    I will provide you with a question and, if available, results from a knowledge retrieval system. 

    The 'Retrieval Results' section below contains a series of text excerpts retrieved from various documents. Each excerpt is formatted as follows:

    ---
    Document: [Name of the Document]
    Content: [Relevant text excerpt from the document]
    ---

    Always provide the name of the document from which you source your information in your answer. 


    **Question:** {query}

    **Instructions:**

    1.  **Analyze the Retrieval Results:** First, examine the 'Retrieval Results' section below.
    2.  **Use Retrieval Results If Available:** **Always** prioritize using information 'Retrieval Results' to formulate your response. Again, always provide the name of the document if its information is used.
    3.  **Use Your Own Knowledge if no Retrieval Results:** **Crucially, if the 'Retrieval Results' section is empty or states 'No results found', you MUST use your own internal knowledge to answer the question.** Do not simply say you cannot answer.
    4.  **Utilize both supplied and internal knowledge:** You are permitted to utilize internal knowledge in your response, ONLY if retrieved information is insufficient.
    5.  **Acknowledge Knowledge Gaps:** If neither the retrieval results nor your own knowledge provides a sufficient answer, only then state that you cannot provide a response.

    **Retrieval Results:**
    {retrieved_context}
    """

    api_response = generate_llm_response(conditional_RAG_prompt)

    logger.info("Retrieved RAG information successfully")

    return api_response 