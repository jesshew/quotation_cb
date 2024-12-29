import gradio as gr
from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from Project import * 
from supabase import create_client, Client
import psycopg2
from psycopg2.extras import RealDictCursor
import tempfile
import pandas as pd
from pathlib import Path
import os
from io import StringIO



load_dotenv()
api_key = os.getenv("LANGTRACE_API_KEY")
if api_key is None:
    raise ValueError("Environment variable 'LANGTRACE_API_KEY' is not set. Please set it in your .env file.")
langtrace.init(api_key=api_key)

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
DB_NAME = os.getenv('DB_NAME')

print(SUPABASE_URL, SUPABASE_KEY, DB_NAME)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_db_connection():
    """Establishes and returns a new database connection."""
    db_params = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }
    conn = psycopg2.connect(**db_params)
    return conn

    
def get_latest_components():
    """Fetches the latest project rubric for the project 'Engage'."""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT base_project_name,module,submodule,unit_type,quantity,mandays_per_unit
            FROM base_project_component pc
            WHERE (pc.base_project_name, pc.component_version) IN (
                SELECT base_project_name, MAX(component_version)
                FROM base_project_component
                GROUP BY base_project_name
            )
            ORDER BY pc.base_project_name;
        """)
        
        component = cur.fetchall()
        cur.close()
        conn.close()

        return component

    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

    
def get_section_name_and_rubric_list():
    """Fetches the latest project rubric for the project 'Engage'."""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT section_name, criteria, initial_question,explanation, priority, quantifiable_value
            FROM base_project_rubric
            WHERE LOWER(base_project_name) = LOWER('Engage')
              AND rubric_version = (
                  SELECT MAX(rubric_version)
                  FROM base_project_rubric
                  WHERE LOWER(base_project_name) = LOWER('Engage')
              )
            ORDER BY 
                CASE priority
                    WHEN 'high' THEN 1
                    WHEN 'med' THEN 2
                    WHEN 'low' THEN 3
                    ELSE 4
                END;
        """)
        
        rubric = cur.fetchall()
        cur.close()
        conn.close()

        # Convert feedback to a list of dictionaries for JSON serialization
        rubric_list = [dict(row) for row in rubric]
        section_name_list = {row['section_name']: dict(row) for row in rubric}.keys()
        # print(f"in get_section_name_and_rubric_list: {rubric_list}, {section_name_list}")
        print(f"in get_section_name_and_rubric_list: {section_name_list}")
        return section_name_list, rubric_list

    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

# Initialize project
# zus_quotation = Project(ProjectType.Engage, zus_coffee, form_v8)
zus_quotation = Project(ProjectType.Engage)

def recalculate_costs(df):
    """Recalculate costs based on modified dataframe values"""
    try:
        # Convert quantity and mandays_per_unit to numeric, replacing non-numeric values with 0
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)
        df['mandays_per_unit'] = pd.to_numeric(df['mandays_per_unit'], errors='coerce').fillna(0)
        
        # Calculate mandays and costs
        df, total_mandays, total_cost = calculate_mandays_and_costs(df)
        csv_string = df.to_csv(index=False)
        # Insert the quotation into the database
        insert_quotation(csv_string, total_cost, total_mandays)
        # df['calculated_mandays'] = df['quantity'] * df['mandays_per_unit']
        # total_mandays = df['calculated_mandays'].sum()
        # total_cost = 1500 * total_mandays

        # Format output string
        cost_summary = f"""
        Total Mandays: {total_mandays:.2f}
        Total Cost: ${total_cost:,.2f}
        """
        return df, cost_summary
    except Exception as e:
        return df, f"Error recalculating costs: {str(e)}"

def recalculate_costs_v2(df):
    """Recalculate costs based on modified dataframe values"""
    try:
        # Convert quantity and mandays_per_unit to numeric, replacing non-numeric values with 0
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(1)
        df['mandays_per_unit'] = pd.to_numeric(df['mandays_per_unit'], errors='coerce').fillna(0)

        # Calculate mandays and costs
        df, total_mandays, total_cost = calculate_mandays_and_costs(df)

        csv_string = df.to_csv(index=False)
        # Insert the quotation into the database
        insert_quotation(csv_string, total_cost, total_mandays)
        # df['calculated_mandays'] = df['quantity'] * df['mandays_per_unit']
        # total_mandays = df['calculated_mandays'].sum()
        # total_cost = 1500 * total_mandays

        # Format output string
        cost_summary = f"""
        Total Mandays: {total_mandays:.2f}
        Total Cost: ${total_cost:,.2f}
        """
        return df, f"Successfully Updated Quotation. SessionID:{zus_quotation.session_id}", cost_summary
    except Exception as e:
        return df, f"Error recalculating costs: {str(e)}"
    
def recalculate_costs_v3(quantity_df,task_df):
    """Recalculate costs based on modified dataframe values"""
    try:
        # Convert quantity and mandays_per_unit to numeric, replacing non-numeric values with 0
        quantity_df['quantity'] = pd.to_numeric(quantity_df['quantity'], errors='coerce').fillna(1)
        quantity_df['mandays_per_unit'] = pd.to_numeric(quantity_df['mandays_per_unit'], errors='coerce').fillna(0)

        # Calculate mandays and costs
        quantity_df, total_mandays, total_cost = calculate_mandays_and_costs(quantity_df)

        csv_string = quantity_df.to_csv(index=False)
        task_string = task_df.to_csv(index=False)
        # Insert the quotation into the database
        insert_quotation(csv_string, total_cost, total_mandays, details= task_string)
        # df['calculated_mandays'] = df['quantity'] * df['mandays_per_unit']
        # total_mandays = df['calculated_mandays'].sum()
        # total_cost = 1500 * total_mandays
        # Format output string
        cost_summary = f"""
        Total Mandays: {total_mandays:.2f}
        Total Cost: ${total_cost:,.2f}
        """
        return quantity_df, f"Successfully Updated Quotation. SessionID:{zus_quotation.session_id}", cost_summary
    except Exception as e:
        return quantity_df, f"Error recalculating costs: {str(e)}"


def sanitize_text(text):
    """Remove or replace special characters from text"""
    # Replace single quotes with double quotes to avoid string formatting issues
    text = text.replace("'", '')
    # Remove or replace other problematic characters as needed
    # Add more replacements here if needed
    return text

def process_response(answer, history):
    """Process user responses and generate appropriate follow-up questions."""
    try:
        # Convert history to list if it's not already
        if not isinstance(history, list):
            history = []
            
        # Sanitize the answer before processing
        sanitized_answer = sanitize_text(str(answer))
        
        # Add the user's answer to project details
        zus_quotation.add_project_detail(sanitized_answer)
        
        # Update session in database if we have a session_id
        if zus_quotation.session_id:
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                
                # Update project_requirement in sessions table
                cur.execute("""
                    UPDATE sessions 
                    SET project_requirement = %s
                    WHERE session_id = %s
                """, (json.dumps(zus_quotation.project_detail), zus_quotation.session_id))
                
                conn.commit()
                cur.close()
                conn.close()
            except Exception as e:
                print(f"Error updating session: {str(e)}")
        
        # Generate next question based on conversation stage
        if len(history) == 1:  # After first client information question
            next_question = zus_quotation.generate_client_follow_up()
        elif len(history) == 2:  # After client follow-up
            next_question = zus_quotation.generate_questions()
        else:  # Subsequent project requirements questions
            next_question = zus_quotation.generate_follow_up()
        
        # Ensure we're adding a proper tuple to history
        if isinstance(answer, str) and isinstance(next_question, str):
            history.append((answer, next_question))
        
        return history, next_question
    except Exception as e:
        print(f"Error in process_response: {str(e)}")
        return history, "Error in generating follow up questions"

def map_mandays(df):
    mandays_dict = zus_quotation.get_component_mandays()
    # Create a mapping dictionary from mandays_dict
    mandays_mapping = {
        item['submodule']: item['mandays_per_unit'] 
        for item in mandays_dict 
        if item['submodule']
    }
    
    # Initialize mandays_per_unit and remarks columns
    df['mandays_per_unit'] = 0.0
    df['remarks'] = ''
    
    # Map mandays_per_unit and add remarks
    for idx, row in df.iterrows():
        submodule = row['submodule']
        if submodule in mandays_mapping:
            df.at[idx, 'mandays_per_unit'] = float(mandays_mapping[submodule] or 0)
        else:
            df.at[idx, 'remarks'] = 'Mandays estimation needed - submodule not found in reference data'
            df.at[idx, 'mandays_per_unit'] = 0.5  # Default value
    
    return df

def calculate_mandays_and_costs(df):
    try:
        # df['mandays_per_unit'] = pd.to_numeric(df['mandays_per_unit'].replace('', '0'), errors='coerce').fillna(0)
        # Calculate mandays and costs
        df['calculated_mandays'] = df['quantity'] * df['mandays_per_unit']
        total_mandays = df['calculated_mandays'].sum()
        total_cost = 1500 * total_mandays
        return df, total_mandays, total_cost
    except Exception as e:
        print(f"Error calculating mandays and costs: {str(e)}")
        return None, None, None


def generate_csv_v1():
    """Generate CSV file with calculated mandays and costs"""
    try:
        # Get CSV string from quotation
        csv_string = zus_quotation.populate_template_with_units()

        # Create DataFrame from CSV string
        df = pd.read_csv(StringIO(csv_string))
        
        # Convert quantity and mandays_per_unit to numeric, replacing empty strings and errors with 0
        df['quantity'] = pd.to_numeric(df['quantity'].replace('', '0'), errors='coerce').fillna(0)
        df = map_mandays(df)       
        df, total_mandays, total_cost = calculate_mandays_and_costs(df)
        csv_string = df.to_csv(index=False)
        # Insert the quotation into the database
        insert_quotation(csv_string, total_cost, total_mandays)

        # Format output string
        cost_summary = f"""
        Total Mandays: {total_mandays:.2f}
        Total Cost: ${total_cost:,.2f}
        """
        return df, cost_summary
        
    except Exception as e:
        return None, f"Error generating CSV: {str(e)}"

def generate_csv_v2(progress=gr.Progress()):
    # Step 1: Rewrite QA
    progress(0.33, desc="Step 1: Rewriting QA...")
    structured_qa_result = zus_quotation.rewrite_qa()
    
    # Step 2: Flare Tasks
    progress(0.66, desc="Step 2: Calling flare tasks...")
    flare_tasks_result = zus_quotation.flare_tasks()
    
    df = pd.read_csv(StringIO(flare_tasks_result))
    df['quantity'] = pd.to_numeric(df['quantity'].replace('', '1'), errors='coerce').fillna(1)
    df['mandays_per_unit'] = pd.to_numeric(df['mandays_per_unit'].replace('', '0'), errors='coerce').fillna(0)
    df, total_mandays, total_cost = calculate_mandays_and_costs(df)
    csv_string = df.to_csv(index=False)

    insert_quotation(csv_string, total_cost, total_mandays)

    progress(1.0, desc="Complete!")
    return [df, "Process completed!", f"total_man_days: {total_mandays}\n total_costs:{total_cost}"]

def generate_csv_v3(progress=gr.Progress()):
    # Step 1: Rewrite QA
    progress(0, desc="Step 1: Rewriting QA...")
    structured_qa_result = zus_quotation.rewrite_qa()
    
    # Step 2: Flare Tasks
    progress(0.33, desc="Step 2: Calling flare tasks...")
    flare_tasks_result = zus_quotation.flare_tasks(flare_task_quotationv3)
    
    # Step 3: Populate Template with Flared Task
    progress(0.66, desc="Step 3: Populating quantity...")
    organized_qa_result = zus_quotation.populate_template_with_orgranised_qa()
    task_breakdown_df = pd.read_csv(StringIO(flare_tasks_result))
    quantity_df = pd.read_csv(StringIO(organized_qa_result))

    # df['quantity'] = pd.to_numeric(df['quantity'].replace('', '1'), errors='coerce').fillna(1)
    # df['mandays_per_unit'] = pd.to_numeric(df['mandays_per_unit'].replace('', '0'), errors='coerce').fillna(0)
    # df, total_mandays, total_cost = calculate_mandays_and_costs(df)
    # csv_string = df.to_csv(index=False)

    # insert_quotation(csv_string, total_cost, total_mandays)

    progress(1.0, desc="Complete!")
    return [task_breakdown_df,quantity_df, "Process completed!", "total_man_days: {total_mandays}\n total_costs:{total_cost}"]


def create_new_session():
    """Create a new session in the database and return the session_id"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insert new session with start time
        cur.execute("""
            INSERT INTO sessions (start_time)
            VALUES (CURRENT_TIMESTAMP)
            RETURNING session_id
        """)
        
        session_id = cur.fetchone()[0]
        
        # Insert session_base_project record for "Engage"
        cur.execute("""
            INSERT INTO session_base_project (session_id, base_project_name)
            VALUES (%s, 'Engage')
        """, (session_id,))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return session_id
    except Exception as e:
        print(f"Error creating new session: {str(e)}")
        return None

def start_chat():
    """Initialize chat with first question and create new session"""
    # Create new session and get session_id
    session_id = create_new_session()
    
    # Set the rubric and session_id for the project
    section_name_list, rubric_list = get_section_name_and_rubric_list()
    component_list = get_latest_components()
    
    # Update session_id in Project instance
    zus_quotation.session_id = session_id
    
    zus_quotation.set_rubric(rubric_list)
    zus_quotation.set_rubric_section_names(section_name_list)
    zus_quotation.set_component_list(component_list)
    
    initial_history = [(None, client_initial_question)]
    return client_initial_question, initial_history

def refresh_components():
    """Refresh component list and update quotation"""
    component_list = get_latest_components()
    zus_quotation.set_component_list(component_list)
    print("successfully updated components list")
    # Generate new CSV to reflect updated components
    return

def get_project_state():
    """Get current state of zus_quotation project"""
    # Create status boxes
    status = f"""Session ID: {zus_quotation.session_id}
    Rubric Loaded: {bool(zus_quotation.rubric)}
    Components Loaded: {bool(zus_quotation.component_list)}
    Requirements Loaded: {bool(zus_quotation.project_detail)}"""
    
    # Format requirements as a table if they exist
    requirements_table = ""
    if zus_quotation.project_detail:
        print(f"\n\nrequirements : {type(zus_quotation.project_detail)}")
        # Create markdown box for requirements
        # requirements_table = "\n\n### Project Requirements\n```markdown\n"
        for index,requirement in enumerate(list(zus_quotation.project_detail)):
            requirements_table += f"\n_____________\n"
            requirements_table += f"#Requirement {index+1}\n {requirement}"
    
    return status, requirements_table

def fetch_session(session_id):
    """Fetch session details from database and initialize project state"""
    try:
        # 1. Fetch session details
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT project_requirement, start_time
            FROM sessions
            WHERE session_id = %s
        """, (session_id,))
        
        session = cur.fetchone()
        cur.close()
        conn.close()

        print(session)
        if session:
            # 2. Update zus_quotation with session data
            zus_quotation.session_id = session_id
            
            # Set project requirements if they exist
            if session['project_requirement']:
                try:
                    # Check if the project requirement is a string
                    if isinstance(session['project_requirement'], str):
                        # Attempt to parse it as JSON
                        try:
                            requirements = json.loads(session['project_requirement'])
                        except json.JSONDecodeError:
                            # If JSON parsing fails, split the string into a list
                            requirements = session['project_requirement'].split('\n')  # or use another delimiter if needed
                    else:
                        requirements = session['project_requirement']
                    
                    # Clear existing details and set new ones
                    zus_quotation.project_detail = []
                    for requirement in requirements:
                        zus_quotation.add_project_detail(requirement.strip())  # Use strip() to remove any leading/trailing whitespace
                except Exception as e:
                    return "", "", f"Error processing project requirements in session {session_id}: {str(e)}"
            
            # 3. Fetch and set rubric
            section_name_list, rubric_list = get_section_name_and_rubric_list()
            zus_quotation.set_rubric(rubric_list)
            zus_quotation.set_rubric_section_names(section_name_list)
            
            # 4. Fetch and set components
            component_list = get_latest_components()
            zus_quotation.set_component_list(component_list)
            
            return (*get_project_state(), f"Successfully loaded session {session_id} with all data")
                    # "\n".join(rubric_list),  # Return rubric list as a string
                    # component_list)  # Ensure to extract string values
            
        else:
            return "", "", f"Session {session_id} not found"
            # return "", "", f"Session {session_id} not found", "", ""

    except Exception as e:
        return "", "", f"Error fetching session: {str(e)}",
        # return "", "", f"Error fetching session: {str(e)}", "", ""

def insert_quotation(csv_string, total_price, total_mandays, note=None, details = None, tier_level=1):
    """Insert a new quotation into the database with an updated version."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Fetch the current maximum version for the given session_id
        cur.execute("""
            SELECT COALESCE(MAX(version), 0) + 1
            FROM quotations
            WHERE session_id = %s
        """, (zus_quotation.session_id,))
        
        result = cur.fetchone()
        version = result[0] if result else 1  # Default to version 1 if no result
 # Get the next version number
        total_price = float(total_price) if total_price is not None else None
        total_mandays = float(total_mandays) if total_mandays is not None else None
        
        details = f"{json.dumps(zus_quotation.project_detail)} + {details}" if details else json.dumps(zus_quotation.project_detail)
            
        # Insert new quotation
        cur.execute("""
            INSERT INTO quotations (session_id, version, details, quotation_csv, total_price, total_mandays)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            zus_quotation.session_id,
            version,
            details,  # Convert project details to JSON string
            csv_string,
            total_price,
            total_mandays
        ))
        
        conn.commit()
        cur.close()
        conn.close()

        print("Successfully inserted quotation")

        
    except Exception as e:
        print(f"Error inserting quotation: {str(e)}")

def save_csv(df):
    """Save the DataFrame as a CSV file."""
    if df is not None:
        csv_file_path = "task_list.csv"  # Specify your desired file path
        df.to_csv(csv_file_path, index=False)
        print(f"CSV saved to {csv_file_path}")
        return f"CSV saved to {csv_file_path}"
    return "No data to save."


def save_csv_v3(df, df2):
    """Save the DataFrame as a CSV file."""
    retval = ""
    if df is not None :
        csv_file_path = "task_list.csv"  # Specify your desired file path
        df.to_csv(csv_file_path, index=False)
        retval += f"Task CSV saved to {csv_file_path}\n"
    if df2 is not None :
        quantity_file_path = "quantity_list.csv"  # Specify your desired file path
        df2.to_csv(quantity_file_path, index=False)
        retval += f"Task CSV saved to {quantity_file_path}\n"
    
    with open("project_requirement.txt", "w") as file:
        file.write(zus_quotation.structured_qa)
        retval += f"Project Requirement saved to project_requirement.txt"

    if retval:
        return retval
    return "No data to save."


gr.set_static_paths(["temp/"])
with gr.Blocks(title="Requirements Gathering Chatbot") as demo:

    gr.Markdown("# Requirements Gathering Chatbot")
    with gr.Tab(label= "Main"):
        gr.Markdown("### Instructions for Use - 2 options :")
        gr.Markdown("1. **Start a New Session**: Begin answering questions for a new project. Please make sure to include the original questions in your replies.")
        gr.Markdown("2. **Load an Existing Project**: Go to the **Project Status** tab. Select a session using its **Session ID** (e.g. id: 7) to review previous details.")
        gr.Markdown("**Current Limitation**: Cannot add new answers to exisiting session")

        with gr.Row():
            start_btn = gr.Button("Start New Session")
            clear_btn = gr.Button("Clear")

        with gr.Row():
            with gr.Row():
                chatbot = gr.Chatbot(height=510)
                with gr.Column():
                    current_question = gr.Textbox(label="Edit Area", lines= 20)
                    with gr.Row():
                        submit_btn = gr.Button("Submit")
        
        with gr.Tab(label= "Quotation Generator V1"):
            gr.Markdown("## Quotation 1")
            gr.Markdown("1 API Call to generate the quotation")
            with gr.Row():

                # current_question = gr.Textbox(label="Edit Area", lines= 15)
                # score_display = gr.Textbox(label="Progress", interactive=False)
                with gr.Column(scale = 4):
                    units_table_v1 = gr.Dataframe(interactive=True, col_count=7)  # New table component

                with gr.Column(scale = 1):
                    generate_btn_v1 = gr.Button("Generate Quotation V1")  # New button
                    units_output_v1 = gr.Textbox(label="Cost Summary", lines=3, interactive=False)
                    recalc_btn_v1 = gr.Button("Recalculate")  # New recalculate button
                    # refresh_components_btn = gr.Button("Get Latest Component List")  # New refresh button
        
        with gr.Tab(label= "Quotation Generator V2"):
            gr.Markdown("Calls API 2 times")
            gr.Markdown("1. Rewrite Q&A into Sturctured Project Requirement")
            gr.Markdown("2. Flare Task,Quantity & Estimated Mandays - ALL in one call")
            gr.Markdown("** Cant export CSV yet, saves locally for now")

            with gr.Row():
                # current_question = gr.Textbox(label="Edit Area", lines= 15)
                # score_display = gr.Textbox(label="Progress", interactive=False)
                with gr.Column(scale = 4):
                    units_table_v2 = gr.Dataframe(interactive=True, col_count=7)  # New table component

                with gr.Column(scale = 1):
                    generate_btn_v2 = gr.Button("Generate Task List V2")  # New button
                    units_output_v2 = gr.Textbox(label="Cost Summary", lines=3, interactive=False)
                    progress_update = gr.Textbox(label="Progress Update", lines=2, interactive=False)
                    recalc_btn_v2 = gr.Button("Recalculate")  # New recalculate button
                    save_csv_btn = gr.Button("Save CSV")  # New Save CSV button
                    # refresh_components_btn = gr.Button("Get Latest Component List")  # New refresh button
        
        with gr.Tab(label= "Quotation Generator V3"):
            gr.Markdown("Calls API 3 times")
            gr.Markdown("1. Rewrite Q&A into Sturctured Project Requirement")
            gr.Markdown("2. Flare Task & Estimated Mandays")
            gr.Markdown("3. Derive Quantity from Project Requirement and Flared Tasks ")
            gr.Markdown("** Cant export CSV yet, cause it saves locally for now")
            gr.Markdown("** If quotation gives insanely high number, check task involving token count. (LLM tend to fill huge numbers on those rows)")

            #pending Gap Report
            with gr.Row():
                with gr.Column(scale=4):

                    gr.Markdown("# Task Breakdown Table")
                    tasks_table_v3 = gr.Dataframe(interactive=True, col_count=7)  # New table component
                    gr.Markdown("# Inferred Quantity Table")
                    quantity_table_v3 = gr.Dataframe(interactive=True, col_count=7)  # New table component

                with gr.Column(scale=1):
                    generate_btn_v3 = gr.Button("Generate Task List V3")  # New button
                    units_output_v3 = gr.Textbox(label="Cost Summary", lines=3, interactive=False)
                    units_output_v3 = gr.Textbox(label="Cost Summary", lines=3, interactive=False)
                    progress_update_v3 = gr.Textbox(label="Progress Update", lines=2, interactive=False)
                    recalc_btn_v3 = gr.Button("Recalculate")  # New recalculate button
                    save_csv_btn_v3 = gr.Button("Save CSV")  # New Save CSV button

            generate_btn_v3.click(
                fn=generate_csv_v3,  # Assuming the same function is used
                outputs=[tasks_table_v3,quantity_table_v3, progress_update_v3, units_output_v3]
            )

            recalc_btn_v3.click(
                fn=recalculate_costs_v3,  # Assuming the same function is used
                inputs=[quantity_table_v3,tasks_table_v3],
                outputs=[quantity_table_v3,progress_update_v3, units_output_v3]
            )

            save_csv_btn_v3.click(
                fn=save_csv_v3,
                inputs=[tasks_table_v3,quantity_table_v3],
                outputs=progress_update_v3
            )

            # save_csv_btn_v3.click(
            #     fn=save_csv,
            #     inputs=tasks_table_v3,
            #     outputs=progress_update_v3
            # )

    # Replace single textbox with separate components
    with gr.Tab(label= "Project Status"):
        gr.Markdown("### Past submissions")
        gr.Markdown("Quick hack to load past submissions to regenarate quotations (This page displays Q&A only; previous quotations are not shown yet).")
        gr.Markdown("Use Session ID 7 for test")

        with gr.Row():
            session_input = gr.Number(label="Session ID", precision=0)
            message_box = gr.Textbox(label="Message", interactive=False)
            status_box = gr.Textbox(
                label="Project Status", 
                value="",
                interactive=False
            )
        fetch_btn = gr.Button("Fetch Session")
        
        with gr.Tab(label= "Requirement"):
            fetched_requirements_box = gr.Markdown(
                value=""
            )
       
    # Event handlers
    start_btn.click(
        fn=lambda: (*start_chat(), *get_project_state()),
        outputs=[current_question, chatbot, status_box, fetched_requirements_box]
    )
    
    submit_btn.click(
        fn=lambda answer, history: (*process_response(answer, history), *get_project_state()),
        inputs=[current_question, chatbot],
        outputs=[chatbot, current_question, status_box, fetched_requirements_box]
    )

    
    
    clear_btn.click(
        fn=lambda: ([], ""),
        outputs=[chatbot, current_question]
    )

    generate_btn_v1.click(
        fn=generate_csv_v1,
        outputs=[units_table_v1, units_output_v1]
    )
    
    recalc_btn_v1.click(
        fn=recalculate_costs,
        inputs=[units_table_v1],
        outputs=[units_table_v1, units_output_v1]
    )

    # refresh_components_btn.click(
    #     fn=refresh_components
    # )

    fetch_btn.click(
        fn=fetch_session,
        inputs=[session_input],
        outputs=[status_box, fetched_requirements_box, message_box]
        # outputs=[status_box, fetched_requirements_box, message_box, fetched_rubric_box, fetched_component_box]
    )
    # Update the button to call the new function
    generate_btn_v2.click(
                generate_csv_v2,
                outputs=[units_table_v2, progress_update,units_output_v2]
        )

    recalc_btn_v2.click(
        fn=recalculate_costs_v2,
        inputs=[units_table_v2],
        outputs=[units_table_v2, progress_update,units_output_v2]
    )

    # save_csv_btn.click(
    #     fn=save_csv,
    #     inputs=units_table_v2,
    #     outputs=progress_update
    # )
    save_csv_btn.click(
        fn=save_csv,
        inputs=tasks_table_v3,
        outputs=progress_update
    )
if __name__ == "__main__":
    # Assign interface to demo for hot reloading
    demo.launch(share=True)
    # print(get_latest_components())
