"""
LLM utility functions for the Evo AI Agent.
Contains placeholder API functions that return fake data for testing.
"""

import logging
import os
from pathlib import Path
import vertexai
from google import genai
from google.genai import types
from typing import Any, Dict, List, Tuple, Optional
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from .fake_data import FAKE_OBJECT_VERSIONS_INFO, FAKE_OBJECTS_ALL_VERSIONS, FAKE_OBJECTS_DATABASE, FAKE_OBJECTS_LIST
from .code_execution_agent import execute_code

logger = logging.getLogger(__name__)

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Get environment variables
PROJECT_ID = os.getenv("PROJECT_ID", "your-project-id")
LOCATION = os.getenv("LOCATION", "us-central1")

# Set Google Cloud project information and initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)


def clean_dataframe_for_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the DataFrame by:
    - Replacing inf and -inf with NaN
    - Removing rows with any NaN
    - Filtering out any non-numeric columns
    - Removing rows where numeric columns have placeholder values (e.g., '-', 'n/a', 'missing', etc.)
    - Filtering out rows with negative numbers in numeric columns
    """
    placeholder_values = {"-", "--", "n/a", "N/A", "na", "NA", "missing", "Missing", "null", "Null"}

    # Replace common placeholders with NaN
    df_cleaned = df.replace(list(placeholder_values), np.nan)

    # Replace inf with NaN
    df_cleaned = df_cleaned.replace([np.inf, -np.inf], np.nan)

    # Drop rows with any NaNs
    df_cleaned = df_cleaned.dropna()

    # Keep only numeric columns
    numeric_df = df_cleaned.select_dtypes(include=[np.number])

    # Filter out rows with negative numbers
    numeric_df = numeric_df[(numeric_df >= 0).all(axis=1)]

    return numeric_df


def execute_code_with_dataframe(code: str, df: pd.DataFrame) -> Dict[str, Any]:
    """
    Execute Python code with access to a dataframe using VertexAI Code Executor.
    This function creates a modified execution environment that includes the dataframe.
    
    Args:
        code: Python code to execute
        df: Pandas DataFrame to make available in the execution context
        
    Returns:
        Dictionary containing execution results
    """
    # Prepare code that includes the dataframe
    # Convert dataframe to a format that can be embedded in code
    df_json = df.to_json(orient='records')
    
    # Create code that reconstructs the dataframe and then executes the user code
    full_code = f"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Reconstruct the dataframe
import json
df_data = {df_json}
df = pd.DataFrame(df_data)

# Execute the user's code
{code}
"""
    
    # Use the execute_code function
    return execute_code(full_code)


def generate_plot_widget(df_input: pd.DataFrame, prompt: str, chart_type: str = "histogram") -> go.Figure:
    """
    Generates a Plotly figure based on LLM-generated code using secure code execution.

    Args:
        df_input (pd.DataFrame): Input dataframe to use in the plot.
        prompt (str): User-provided natural language description of desired chart.
        chart_type (str): Optional chart type hint (default: "histogram").

    Returns:
        go.Figure: Generated Plotly figure.
    """

    # Clean the dataframe first to know what columns will be available
    cleaned_df = clean_dataframe_for_analysis(df_input)
    available_columns = list(cleaned_df.columns)
    
    logger.info(f"Original dataframe columns: {list(df_input.columns)}")
    logger.info(f"Cleaned dataframe columns: {available_columns}")
    
    # Prepare the prompt to guide the LLM with actual available columns
    conditional_prompt = (
        f"You are a helpful Python assistant that generates Plotly figures using `plotly.express`.\n\n"
        f"User chart type: {chart_type}\n"
        f"User prompt: '{prompt}'\n\n"
        f"The available DataFrame columns after cleaning are: {available_columns}\n"
        "IMPORTANT: Only use columns from the list above. Do not reference any other columns like 'sample_id' as they have been removed during data cleaning.\n\n"
        "Use your understanding of the context and semantics to intelligently map user-described variables "
        "to actual column names in the DataFrame. For example, interpret 'gold' as a reference to a column like 'gold' "
        "if available. Do not invent or assume columns beyond those provided.\n\n"
        "Generate complete Python code that:\n"
        "1. Creates a Plotly figure using the DataFrame variable named `df`\n"
        "2. Saves the figure as both PNG and HTML files in 'generated_charts/' directory\n"
        "3. Prints the file paths and chart information\n\n"
        "IMPORTANT: When binning any column using `pd.cut(...)`, you must convert the resulting intervals "
        "to strings using `.astype(str)`. This ensures labels (e.g., '(100.0, 200.0]') are visible in the legend or axes, and avoids serialization issues with Plotly.\n\n"
        "Use `clip` for modifying values (not filtering) and retain all data in the plot.\n\n"
        "Example structure:\n"
        "```python\n"
        "import os\n"
        "from datetime import datetime\n"
        "\n"
        "# Create output directory\n"
        "os.makedirs('generated_charts', exist_ok=True)\n"
        "\n"
        "# Generate timestamp for unique filenames\n"
        "timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')\n"
        "\n"
        "# Create the chart\n"
        "fig = px.histogram(df, x='column_name', title='My Chart')\n"
        "\n"
        "# Save files\n"
        "png_file = f'generated_charts/chart_{timestamp}.png'\n"
        "html_file = f'generated_charts/chart_{timestamp}.html'\n"
        "fig.write_image(png_file, width=800, height=600)\n"
        "fig.write_html(html_file)\n"
        "\n"
        "print(f'Chart saved as PNG: {png_file}')\n"
        "print(f'Chart saved as HTML: {html_file}')\n"
        "```\n\n"
        "Generate the complete code without markdown formatting."
    )

    # Get LLM-generated code
    llm_code = generate_llm_response(conditional_prompt)

    # Print the LLM-generated code for debugging
    print("--------------------------------")
    print("Generated code from LLM:")
    print(llm_code)

    # Clean up Markdown formatting
    if "```" in llm_code:
        llm_code = llm_code.split("```")[1]
        if llm_code.startswith("python"):
            llm_code = llm_code[len("python") :].strip()
    llm_code = llm_code.strip()

    logger.info("LLM Generated code for plot generation:")
    logger.info(llm_code)

    try:
        # Execute the cleaned code with dataframe using secure VertexAI Code Executor
        result = execute_code_with_dataframe(llm_code, cleaned_df)
        
        if result['success']:
            logger.info("Code executed successfully via VertexAI Code Executor")
            logger.info(f"Execution output: {result['output']}")
            
            # Parse the output to find saved file paths
            output_lines = result['output'].split('\n')
            png_file = None
            html_file = None
            
            for line in output_lines:
                if 'Chart saved as PNG:' in line:
                    png_file = line.split('Chart saved as PNG:')[-1].strip()
                elif 'Chart saved as HTML:' in line:
                    html_file = line.split('Chart saved as HTML:')[-1].strip()
            
            # Return a figure indicating success with file paths
            fig = go.Figure()
            success_text = "Chart generated successfully via secure code execution!<br>"
            if png_file:
                success_text += f"PNG file: {png_file}<br>"
            if html_file:
                success_text += f"HTML file: {html_file}<br>"
            success_text += f"Data points: {len(cleaned_df)}"
            
            fig.add_annotation(
                text=success_text,
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=14, color="green")
            )
            fig.update_layout(
                title="Chart Generation Successful",
                xaxis=dict(showgrid=False, showticklabels=False),
                yaxis=dict(showgrid=False, showticklabels=False),
                width=800, height=600
            )
            return fig
            
        else:
            # Log the error and raise an exception with detailed information
            logger.error(f"VertexAI Code Executor failed: {result['error']}")
            raise RuntimeError(f"VertexAI Code Executor failed: {result['error']}")

    except Exception as e:
        logger.error(f"Error in plot generation: {e}")
        raise e


def chart_plot(df: pd.DataFrame, user_prompt: str) -> go.Figure:
    """
    Main chart plotting function that generates a Plotly figure from a DataFrame and user prompt.
    
    Args:
        df (pd.DataFrame): The dataframe containing the data to plot.
        user_prompt (str): The user's request for generating a chart.
        
    Returns:
        go.Figure: A Plotly figure object.
    """
    
    logger.info(f"Generating chart for prompt: {user_prompt}")
    
    if df is None or df.empty:
        logger.warning("No dataframe provided or dataframe is empty")
        fig = go.Figure()
        fig.add_annotation(text="No data available for plotting", xref="paper", yref="paper",
                         x=0.5, y=0.5, showarrow=False)
        return fig
    
    try:
        # Generate the plot using the LLM-powered function
        plot_widget = generate_plot_widget(df, user_prompt)
        
        if not isinstance(plot_widget, go.Figure):
            raise TypeError(f"The generated plot_widget is not a valid Plotly figure. Got: {type(plot_widget)}")
        
        return plot_widget
        
    except Exception as e:
        logger.error(f"Error in chart_plot: {e}")
        raise e


def display_chart_info(chart_result: Dict[str, Any]) -> str:
    """
    Display information about a generated chart in a readable format.
    
    Args:
        chart_result (Dict[str, Any]): Result from generate_chart function.
        
    Returns:
        str: Formatted chart information.
    """
    
    if not chart_result.get("success", False):
        return f"❌ Chart generation failed: {chart_result.get('error', 'Unknown error')}"
    
    chart_info = chart_result.get("chart_info", {})
    
    info_text = f"""
📊 **Chart Generated Successfully!**

🔍 **Request**: {chart_info.get('user_request', 'N/A')}
📈 **Chart Type**: {chart_info.get('chart_type', 'N/A')}
📊 **Data Shape**: {chart_info.get('data_shape', 'N/A')}
🏷️ **Columns Used**: {', '.join(chart_info.get('columns_used', []))}

📁 **Files Saved**:
"""
    
    files_saved = chart_info.get('files_saved', [])
    for file_path in files_saved:
        file_type = "HTML" if file_path.endswith('.html') else "PNG" if file_path.endswith('.png') else "Unknown"
        info_text += f"  • {file_type}: {file_path}\n"
    
    return info_text.strip()


def get_chart_summary(chart_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract key information from chart result for logging or API responses.
    
    Args:
        chart_result (Dict[str, Any]): Result from generate_chart function.
        
    Returns:
        Dict[str, Any]: Summarized chart information.
    """
    
    if not chart_result.get("success", False):
        return {
            "success": False,
            "error": chart_result.get("error"),
            "files_created": 0
        }
    
    chart_info = chart_result.get("chart_info", {})
    
    return {
        "success": True,
        "request": chart_info.get("user_request"),
        "data_points": chart_info.get("data_shape", [0, 0])[0],
        "columns_count": len(chart_info.get("columns_used", [])),
        "files_created": len(chart_info.get("files_saved", [])),
        "html_available": any(f.endswith('.html') for f in chart_info.get("files_saved", [])),
        "png_available": any(f.endswith('.png') for f in chart_info.get("files_saved", [])),
        "file_paths": chart_info.get("files_saved", [])
    }


def create_fake_dataframe(attribute_name: Optional[str] = None) -> pd.DataFrame:
    """
    Creates a fake DataFrame with realistic geological assay data for testing chart functionality.
    
    Args:
        attribute_name (Optional[str]): The attribute name to create data for (e.g., "gold", "copper").
        
    Returns:
        pd.DataFrame: A fake dataframe with realistic geological data.
    """
    
    import random
    random.seed(42)  # Consistent fake data
    
    n_samples = 100
    
    # Base DataFrame structure
    data = {
        'sample_id': [f'SAMPLE_{i:03d}' for i in range(1, n_samples + 1)],
        'depth_from': [round(random.uniform(0, 200), 1) for _ in range(n_samples)],
        'depth_to': [round(random.uniform(200, 400), 1) for _ in range(n_samples)]
    }
    
    # Add attribute-specific data
    if attribute_name and attribute_name.lower() in ["gold", "au"]:
        data['AU_PPM_LAB'] = [round(random.uniform(0.01, 10.0), 3) for _ in range(n_samples)]
        data['AU_PPM_FIELD'] = [val * random.uniform(0.8, 1.2) for val in data['AU_PPM_LAB']]
    elif attribute_name and attribute_name.lower() in ["copper", "cu"]:
        data['CU_PCT_LAB'] = [round(random.uniform(0.1, 5.0), 2) for _ in range(n_samples)]
        data['CU_PCT_FIELD'] = [val * random.uniform(0.9, 1.1) for val in data['CU_PCT_LAB']]
    elif attribute_name and attribute_name.lower() in ["silver", "ag"]:
        data['AG_PPM_LAB'] = [round(random.uniform(0.5, 50.0), 2) for _ in range(n_samples)]
        data['AG_PPM_FIELD'] = [val * random.uniform(0.85, 1.15) for val in data['AG_PPM_LAB']]
    else:
        # Generic multi-element data
        data['AU_PPM_LAB'] = [round(random.uniform(0.01, 10.0), 3) for _ in range(n_samples)]
        data['CU_PCT_LAB'] = [round(random.uniform(0.1, 5.0), 2) for _ in range(n_samples)]
        data['AG_PPM_LAB'] = [round(random.uniform(0.5, 50.0), 2) for _ in range(n_samples)]
        data['ZN_PCT_LAB'] = [round(random.uniform(0.05, 3.0), 2) for _ in range(n_samples)]
        data['PB_PCT_LAB'] = [round(random.uniform(0.01, 2.0), 2) for _ in range(n_samples)]
    
    # Add some geological context
    formations = ['Formation_A', 'Formation_B', 'Formation_C', 'Formation_D']
    data['formation'] = [random.choice(formations) for _ in range(n_samples)]
    
    rock_types = ['Granite', 'Basalt', 'Limestone', 'Sandstone', 'Shale']
    data['rock_type'] = [random.choice(rock_types) for _ in range(n_samples)]
    
    return pd.DataFrame(data)


# Chart generation helper functions moved from function_tools.py
def extract_object_and_attribute(user_prompt: str) -> Tuple[str, str]:
    """Extract object name and attribute from user prompt."""
    from .fake_data import FAKE_TABLE_DATA
    
    # Common patterns to look for object names
    prompt_lower = user_prompt.lower()
    
    # Look for object names in the prompt
    object_name = None
    for obj_name in FAKE_TABLE_DATA.keys():
        if obj_name.lower() in prompt_lower:
            object_name = obj_name
            break
    
    # Default to first available object if none found
    if not object_name:
        object_name = list(FAKE_TABLE_DATA.keys())[0]
    
    # Look for attribute names
    attribute_name = None
    if object_name in FAKE_TABLE_DATA:
        for attr_name in FAKE_TABLE_DATA[object_name].keys():
            if attr_name.lower() in prompt_lower:
                attribute_name = attr_name
                break
        
        # Check for common aliases
        if not attribute_name:
            aliases = {"au": "gold", "ag": "silver", "cu": "copper", "pb": "lead", "zn": "zinc", "fe": "iron"}
            for alias, real_attr in aliases.items():
                if alias in prompt_lower and real_attr in FAKE_TABLE_DATA[object_name]:
                    attribute_name = real_attr
                    break
    
    # Default to first available attribute if none found
    if not attribute_name and object_name in FAKE_TABLE_DATA:
        attribute_name = list(FAKE_TABLE_DATA[object_name].keys())[0]
    
    return object_name, attribute_name


def create_dataframe_from_fake_data(object_name: str, attribute_name: str, user_prompt: str) -> pd.DataFrame:
    """Create a DataFrame from our structured fake data."""
    from .fake_data import FAKE_TABLE_DATA
    
    if object_name not in FAKE_TABLE_DATA:
        object_name = list(FAKE_TABLE_DATA.keys())[0]
    
    object_data = FAKE_TABLE_DATA[object_name]
    
    # Determine which attributes to include
    prompt_lower = user_prompt.lower()
    
    # Multi-attribute analysis (scatter plots, correlations, etc.)
    if any(word in prompt_lower for word in ["vs", "versus", "against", "correlation", "scatter"]):
        # Include multiple attributes for comparison charts
        df_data = {}
        for attr, values in object_data.items():
            df_data[attr] = values
    else:
        # Single attribute analysis
        if attribute_name in object_data:
            df_data = {attribute_name: object_data[attribute_name]}
        else:
            # Fallback to first attribute
            first_attr = list(object_data.keys())[0]
            df_data = {first_attr: object_data[first_attr]}
    
    # Add sample IDs for reference
    df_data['sample_id'] = [f'SAMPLE_{i+1:03d}' for i in range(len(list(df_data.values())[0]))]
    
    return pd.DataFrame(df_data)


def generate_simple_chart(df: pd.DataFrame, user_prompt: str, attribute_name: str) -> go.Figure:
    """
    Generate a chart based on user prompt using LLM-generated code executed safely.
    Uses the secure code execution environment instead of local exec().
    """
    
    # Prepare the LLM prompt to generate complete chart creation code
    conditional_prompt = (
        f"You are a helpful Python assistant that generates Plotly figures for geological data analysis.\n\n"
        f"User prompt: '{user_prompt}'\n\n"
        f"The available DataFrame columns are: {list(df.columns)}\n"
        f"Primary attribute focus: '{attribute_name}'\n\n"
        "GEOLOGICAL DATA CONTEXT:\n"
        "- This is geological assay data with attributes like gold, silver, copper, zinc, etc.\n"
        "- Values represent concentrations, grades, or measurements\n"
        "- Use appropriate units and scaling for geological data visualization\n"
        "- Consider log scales for highly variable data like precious metal concentrations\n\n"
        "DATA PROVIDED:\n"
        f"The DataFrame has {len(df)} rows and {len(df.columns)} columns.\n"
        f"Columns: {list(df.columns)}\n\n"
        "TASK:\n"
        "Generate complete Python code that:\n"
        "1. Creates a Plotly figure based on the user request\n"
        "2. Saves the figure as both PNG and HTML files\n"
        "3. Prints the file paths of saved charts\n"
        "4. Prints a summary of the chart created\n\n"
        "IMPORTANT GUIDELINES:\n"
        "1. The DataFrame is already loaded as 'df' in the environment\n"
        "2. All required libraries (pandas as pd, plotly.express as px, plotly.graph_objects as go, numpy as np) are available\n"
        "3. When binning any column using `pd.cut(...)`, convert resulting intervals to strings using `.astype(str)`\n"
        "4. Use `clip` for modifying values (not filtering) and retain all data in the plot\n"
        "5. For geological data, consider using appropriate color scales (viridis, plasma, etc.)\n"
        "6. Add meaningful titles and axis labels that include units when relevant\n"
        "7. For histograms, use appropriate bin counts (10-30 bins typically work well)\n"
        "8. Always verify the data has values before plotting - check df.shape and df.describe() if needed\n"
        "9. Create the 'generated_charts' directory if it doesn't exist\n"
        "10. Use timestamp in filenames to avoid conflicts\n\n"
        "CHART TYPE SELECTION:\n"
        "- Analyze the user prompt to determine the most appropriate chart type\n"
        "- Choose the visualization that best represents the requested analysis\n"
        "- Always include a descriptive title that mentions the geological context\n\n"
        "EXAMPLE OUTPUT STRUCTURE:\n"
        "```python\n"
        "import os\n"
        "from datetime import datetime\n"
        "\n"
        "# Create output directory\n"
        "os.makedirs('generated_charts', exist_ok=True)\n"
        "\n"
        "# Generate timestamp for unique filenames\n"
        "timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')\n"
        "\n"
        "# Create the chart (example for histogram)\n"
        "fig = px.histogram(df, x='column_name', nbins=20, title='Your Chart Title')\n"
        "fig.update_layout(xaxis_title='X Label (units)', yaxis_title='Y Label')\n"
        "\n"
        "# Save as PNG and HTML\n"
        "png_file = f'generated_charts/chart_{timestamp}.png'\n"
        "html_file = f'generated_charts/chart_{timestamp}.html'\n"
        "\n"
        "fig.write_image(png_file, width=800, height=600)\n"
        "fig.write_html(html_file)\n"
        "\n"
        "print(f'Chart saved as PNG: {png_file}')\n"
        "print(f'Chart saved as HTML: {html_file}')\n"
        "print(f'Chart type: histogram')\n"
        "print(f'Data points: {len(df)}')\n"
        "```\n\n"
        "Generate the complete code without any markdown formatting - just the Python code."
    )

    # Get LLM-generated code
    llm_code = generate_llm_response(conditional_prompt)

    # Clean up any markdown formatting
    if "```" in llm_code:
        code_blocks = llm_code.split("```")
        for i, block in enumerate(code_blocks):
            if block.strip().startswith("python"):
                llm_code = block[6:].strip()
                break
            elif i > 0 and block.strip():
                llm_code = block.strip()
                break
    
    llm_code = llm_code.strip()

    logger.info("LLM Generated code for chart generation:")
    logger.info(llm_code)

    try:
        # Clean the dataframe first
        cleaned_df = clean_dataframe_for_analysis(df)
        if cleaned_df.empty:
            return create_error_figure("No valid data available after cleaning")
        
        logger.info(f"Cleaned DataFrame info: shape={cleaned_df.shape}, columns={list(cleaned_df.columns)}")
        
        # Use the secure execute_code_with_dataframe function
        result = execute_code_with_dataframe(llm_code, cleaned_df)
        
        if result['success']:
            logger.info("Code executed successfully via secure code execution")
            logger.info(f"Execution output: {result['output']}")
            
            # Parse the output to find saved file paths
            output_lines = result['output'].split('\n')
            png_file = None
            html_file = None
            
            for line in output_lines:
                if 'Chart saved as PNG:' in line:
                    png_file = line.split('Chart saved as PNG:')[-1].strip()
                elif 'Chart saved as HTML:' in line:
                    html_file = line.split('Chart saved as HTML:')[-1].strip()
            
            # Try to load the HTML file and extract the figure
            if html_file and os.path.exists(html_file):
                try:
                    # Read the HTML file and create a simple figure with a link
                    fig = go.Figure()
                    fig.add_annotation(
                        text=f"Chart successfully generated!<br>"
                             f"<a href='{html_file}'>View Interactive Chart</a><br>"
                             f"PNG file: {png_file if png_file else 'Not available'}<br>"
                             f"Data points: {len(cleaned_df)}",
                        xref="paper", yref="paper",
                        x=0.5, y=0.5, showarrow=False,
                        font=dict(size=14, color="green")
                    )
                    fig.update_layout(
                        title="Chart Generation Successful",
                        xaxis=dict(showgrid=False, showticklabels=False),
                        yaxis=dict(showgrid=False, showticklabels=False),
                        width=800, height=600
                    )
                    logger.info(f"Chart files created: PNG={png_file}, HTML={html_file}")
                    return fig
                except Exception as load_error:
                    logger.warning(f"Could not load generated chart file: {load_error}")
            
            # If we can't load the chart file, return a success message with output
            fig = go.Figure()
            fig.add_annotation(
                text=f"Chart code executed successfully!<br>"
                     f"Output: {result['output'][:200]}...<br>"
                     f"Files may have been created in generated_charts/",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=12, color="blue")
            )
            fig.update_layout(
                title="Chart Generation - Code Executed",
                width=800, height=600
            )
            return fig
            
        else:
            logger.error(f"Secure code execution failed: {result['error']}")
            return create_error_figure(f"Chart generation failed: {result['error']}")

    except Exception as e:
        logger.error(f"Error in secure chart generation: {e}")
        return create_error_figure(f"Failed to generate chart: {str(e)}")



def create_error_figure(error_message: str) -> go.Figure:
    """Create a figure displaying an error message."""
    
    fig = go.Figure()
    fig.add_annotation(
        text=error_message,
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16, color="red")
    )
    fig.update_layout(
        title="Chart Generation Error",
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False),
        width=800, height=600
    )
    return fig


def save_chart_file(plotly_figure: go.Figure, user_prompt: str) -> str:
    """Save chart as PNG file only."""
    import os
    from datetime import datetime
    
    # Create charts directory if it doesn't exist
    charts_dir = "generated_charts"
    os.makedirs(charts_dir, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_prompt = "".join(c for c in user_prompt if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_prompt = safe_prompt.replace(' ', '_')[:50]  # Limit length
    
    png_filename = f"{charts_dir}/chart_{timestamp}_{safe_prompt}.png"
    
    # Save as PNG (requires kaleido)
    try:
        plotly_figure.write_image(png_filename, width=800, height=600, format='png')
        logger.info(f"Chart saved as PNG: {png_filename}")
        return png_filename
    except Exception as e:
        logger.error(f"Could not save PNG file: {e}")
        # Create a fallback filename to indicate the error
        error_filename = f"{charts_dir}/chart_{timestamp}_error.txt"
        with open(error_filename, 'w') as f:
            f.write(f"Error saving chart: {e}\nPrompt: {user_prompt}")
        logger.info(f"Error details saved to: {error_filename}")
        return error_filename


def get_object_id(object_name: str) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    """
    Simplified get_object_id function that returns placeholder data for testing.
    
    Args:
        object_name (str): The name of the object to find.
        
    Returns:
        Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]: 
            (object_id, object_type, version_id, error_msg)
    """
    
    logger.info(f"Getting object ID for: {object_name}")
    
    # Check if object exists in our fake database
    if object_name in FAKE_OBJECTS_DATABASE:
        # Return placeholder IDs for testing
        return f"obj_id_{object_name}", "downhole-collection", "version_latest", None
    else:
        error_msg = f"Unable to find object named '{object_name}' in the workspace."
        logger.error(error_msg)
        return None, None, None, error_msg


# Placeholder API functions that return fake data for testing
async def get_list_of_objects_from_api(all_versions: bool = False) -> List[Dict[str, Any]]:
    """
    Placeholder API function that returns fake objects data for testing.
    
    Args:
        all_versions (bool): If True, returns all versions, otherwise only latest versions.
        
    Returns:
        List[Dict[str, Any]]: List of objects with their metadata.
    """
    if all_versions:
        return FAKE_OBJECTS_ALL_VERSIONS
    else:
        return FAKE_OBJECTS_LIST


async def get_objects_info_from_api(object_names: List[str]) -> List[Dict[str, Any]]:
    """
    Placeholder API function that returns fake detailed object information for testing.
    
    Args:
        object_names (List[str]): List of object names to get information for.
        
    Returns:
        List[Dict[str, Any]]: Detailed information for the requested objects.
    """
    result = []
    for obj_name in object_names:
        if obj_name in FAKE_OBJECTS_DATABASE:
            result.append(FAKE_OBJECTS_DATABASE[obj_name])
        else:
            result.append({
                "error": f"Object '{obj_name}' not found in workspace",
                "available_objects": list(FAKE_OBJECTS_DATABASE.keys())
            })
    return result


async def get_object_versions_info_from_api(object_names: List[str]) -> List[Dict[str, Any]]:
    """
    Placeholder API function that returns fake version information for testing.
    
    Args:
        object_names (List[str]): List of object names to get version information for.
        
    Returns:
        List[Dict[str, Any]]: Version information for the requested objects.
    """
    result = []
    for obj_name in object_names:
        if obj_name in FAKE_OBJECT_VERSIONS_INFO:
            result.append(FAKE_OBJECT_VERSIONS_INFO[obj_name])
        else:
            result.append({
                "error": f"Object '{obj_name}' not found in workspace",
                "available_objects": list(FAKE_OBJECT_VERSIONS_INFO.keys())
            })
    return result 


async def download_table_data_from_api(object_name: str, collections_attribute: Optional[str]) -> List[float]:
    """
    Downloads table data for a specific collections attribute from an object.
    
    Args:
        object_name (str): The name of the object.
        collections_attribute (Optional[str]): The collections attribute to download.
        
    Returns:
        List[float]: The downloaded data as a list of floats.
    """
    from .fake_data import FAKE_TABLE_DATA
    
    logger.info(f"Downloading table data for {object_name}, attribute: {collections_attribute}")
    
    object_id, object_type, version_id, error_msg = get_object_id(object_name)
    
    if error_msg:
        logger.error(f"Error getting object ID: {error_msg}")
        return []

    # Use fake data from fake_data.py
    logger.info("Using fake data from fake_data.py")
    
    # Try to get data for the specific object and attribute
    if object_name in FAKE_TABLE_DATA:
        object_data = FAKE_TABLE_DATA[object_name]
        
        if collections_attribute and collections_attribute.lower() in object_data:
            # Direct match for the attribute
            data = object_data[collections_attribute.lower()]
            logger.info(f"Found fake data for {object_name}.{collections_attribute} with {len(data)} values")
            return data
        elif collections_attribute:
            # Try common attribute aliases
            attribute_aliases = {
                "au": "gold",
                "ag": "silver", 
                "cu": "copper",
                "pb": "lead",
                "zn": "zinc",
                "fe": "iron",
                "mo": "molybdenum",
                "u": "uranium"
            }
            
            normalized_attr = collections_attribute.lower()
            if normalized_attr in attribute_aliases:
                mapped_attr = attribute_aliases[normalized_attr]
                if mapped_attr in object_data:
                    data = object_data[mapped_attr]
                    logger.info(f"Found fake data for {object_name}.{mapped_attr} (alias for {collections_attribute}) with {len(data)} values")
                    return data
            
            # If specific attribute not found, return the first available attribute
            if object_data:
                first_attr = list(object_data.keys())[0]
                data = object_data[first_attr]
                logger.warning(f"Attribute '{collections_attribute}' not found for {object_name}, returning {first_attr} data with {len(data)} values")
                return data
        else:
            # No specific attribute requested, return first available
            if object_data:
                first_attr = list(object_data.keys())[0]
                data = object_data[first_attr]
                logger.info(f"No specific attribute requested for {object_name}, returning {first_attr} data with {len(data)} values")
                return data
    
    # Fallback: object not found in fake data, generate basic placeholder
    logger.warning(f"No fake data found for object '{object_name}', returning placeholder data")
    import random
    random.seed(hash(f"{object_name}_{collections_attribute}"))  # Consistent fake data
    return [round(random.uniform(0.1, 100.0), 2) for _ in range(50)]


def generate_llm_response(conditional_RAG_prompt: str) -> str:
    """
    Generate a response using the Gemini LLM model.
    
    Args:
        conditional_RAG_prompt (str): The prompt to send to the LLM.
        
    Returns:
        str: The generated response text.
    """
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION,
    )

    model = "gemini-2.5-flash"    
    contents = [
        types.Content(role="user", parts=[types.Part.from_text(text=conditional_RAG_prompt)]),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.0,
        top_p=0.95,
        max_output_tokens=8192,
        response_modalities=["TEXT"],
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    llm_response = response.text

    return llm_response 