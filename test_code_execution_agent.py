"""
Test file for code execution agent using simulated LLM-generated plotting function.
This tests the secure code execution with actual geological data visualization code.
"""

import pandas as pd
from src.evo_ai.code_execution_agent import execute_code
from src.evo_ai.fake_data import FAKE_TABLE_DATA


def simulated_test_code():
    """
    Test function that simulates LLM-generated plotting code execution.
    Uses the gold assay data from thalanga_local_drillholes_dt and executes
    a complete plotting function via the secure code execution environment.
    """
    
    # Get the gold data from FAKE_TABLE_DATA
    object_name = 'thalanga_local_drillholes_dt'
    if object_name not in FAKE_TABLE_DATA:
        print(f"Error: {object_name} not found in FAKE_TABLE_DATA")
        print(f"Available objects: {list(FAKE_TABLE_DATA.keys())}")
        return
    
    object_data = FAKE_TABLE_DATA[object_name]
    if 'gold' not in object_data:
        print(f"Error: 'gold' attribute not found in {object_name}")
        print(f"Available attributes: {list(object_data.keys())}")
        return
    
    gold_data = object_data['gold']
    print(f"✅ Loaded {len(gold_data)} gold assay values from {object_name}")
    
    # Create the complete code to execute including DataFrame creation and plotting
    test_code = f"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

def llm_generated_plot(df):
    \"\"\"
    Generates a Plotly histogram of gold assay data.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing geological assay data.
                       Expected columns: 'gold'.

    Returns:
    plotly.graph_objects.Figure: A Plotly figure displaying the histogram.
    \"\"\"
    
    # Ensure the 'gold' column exists and is numeric
    if 'gold' not in df.columns:
        raise ValueError("DataFrame must contain a 'gold' column for this plot.")

    # Convert 'gold' to numeric, coercing errors to NaN, then drop NaNs for plotting
    # px.histogram handles NaNs by default, but explicit conversion is good practice.
    df_plot = df.copy()
    df_plot['gold'] = pd.to_numeric(df_plot['gold'], errors='coerce')
    df_plot = df_plot.dropna(subset=['gold'])

    if df_plot.empty:
        print("Warning: No valid 'gold' data found after cleaning. Cannot generate plot.")
        return px.scatter().update_layout(title="No data to display for Gold Assay Histogram")

    # Create the histogram
    fig = px.histogram(df_plot,
                       x='gold',
                       nbins=15,  # As requested by the user
                       title='Distribution of Gold Assay (Thalanga Local Drillholes)'
                      )

    # Update layout for better readability and geological context
    fig.update_layout(
        xaxis_title='Gold Assay (g/t)',
        yaxis_title='Frequency',
        bargap=0.05,  # Add a small gap between bars for better visual separation
        template='plotly_white' # Professional styling
    )

    return fig

# Create DataFrame with gold assay data
gold_values = {gold_data}
df = pd.DataFrame({{'gold': gold_values}})

print(f"Created DataFrame with {{len(df)}} gold assay values")
print(f"Gold data range: {{df['gold'].min():.3f}} to {{df['gold'].max():.3f}} g/t")
print(f"Gold data mean: {{df['gold'].mean():.3f}} g/t")

# Generate the plot
fig = llm_generated_plot(df)

# Create output directory
os.makedirs('generated_charts', exist_ok=True)

# Generate timestamp for unique filenames
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# Save the chart as both PNG and HTML
png_file = f'generated_charts/thalanga_gold_histogram_{{timestamp}}.png'
html_file = f'generated_charts/thalanga_gold_histogram_{{timestamp}}.html'

try:
    fig.write_image(png_file, width=800, height=600)
    print(f"Chart saved as PNG: {{png_file}}")
except Exception as e:
    print(f"Could not save PNG: {{e}}")

try:
    fig.write_html(html_file)
    print(f"Chart saved as HTML: {{html_file}}")
except Exception as e:
    print(f"Could not save HTML: {{e}}")

print("Chart generation completed successfully!")
print(f"Chart type: Histogram")
print(f"Data points: {{len(df)}}")
print(f"Bins used: 15")
"""
    
    print("🔧 Executing LLM-generated plotting code via secure code execution...")
    print("=" * 60)
    
    # Execute the code using the secure code execution agent
    result = execute_code(test_code)
    
    print("EXECUTION RESULTS:")
    print("=" * 60)
    print(f"Success: {result['success']}")
    print(f"Execution Time: {result['execution_time']:.2f} seconds")
    
    if result['success']:
        print("✅ CODE EXECUTION SUCCESSFUL!")
        print("\nOutput:")
        print("-" * 40)
        print(result['output'])
        
        # Check for generated code in the response
        if 'generated_code' in result and result['generated_code']:
            print("\nGenerated Code:")
            print("-" * 40)
            for code_block in result['generated_code']:
                print(f"Language: {code_block['language']}")
                print("Code:")
                print(code_block['code'])
                
        if 'execution_results' in result and result['execution_results']:
            print("\nExecution Results:")
            print("-" * 40)
            for exec_result in result['execution_results']:
                print(f"Outcome: {exec_result['outcome']}")
                if exec_result['output']:
                    print(f"Output: {exec_result['output']}")
                    
    else:
        print("❌ CODE EXECUTION FAILED!")
        print(f"Error: {result['error']}")
    
    print("=" * 60)
    return result


def test_simple_code():
    """
    Test function for simple code execution to verify the system is working.
    """
    print("🧪 Testing simple code execution...")
    
    simple_code = """
# Simple test to verify code execution is working
import pandas as pd
import numpy as np

# Create some test data
data = [1.2, 2.5, 0.8, 3.1, 1.9, 2.2, 0.5, 4.2, 1.8, 2.9]
df = pd.DataFrame({'gold': data})

print(f"Created test dataset with {len(df)} values")
print(f"Mean gold value: {df['gold'].mean():.2f}")
print(f"Max gold value: {df['gold'].max():.2f}")
print("Simple code execution test completed!")
"""
    
    result = execute_code(simple_code)
    
    print(f"Simple test result - Success: {result['success']}")
    if result['success']:
        print(f"Output: {result['output']}")
    else:
        print(f"Error: {result['error']}")
    
    return result


if __name__ == "__main__":
    print("🚀 TESTING CODE EXECUTION AGENT")
    print("=" * 70)
    
    # First test simple execution
    print("\n1. SIMPLE CODE TEST")
    print("-" * 30)
    test_simple_code()
    
    print("\n\n2. SIMULATED LLM PLOTTING TEST")
    print("-" * 35)
    # Test the main simulated plotting code
    result = simulated_test_code()
    
    print(f"\n🎉 Test completed! Final result: {'SUCCESS' if result['success'] else 'FAILED'}") 