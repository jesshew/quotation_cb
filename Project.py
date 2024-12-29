from enum import Enum
from ProjectClient import Client,zus_coffee,ssm, game
from prompts import *
from langtrace_python_sdk import langtrace
from langtrace_python_sdk.utils.with_root_span import with_langtrace_root_span
import openai
from contextlib import contextmanager
import json

@contextmanager
def openai_session():
    """Context manager to properly handle OpenAI API sessions"""
    try:
        # Initialize client
        client = openai.OpenAI()
        yield client
    finally:
        # Clean up client resources
        if hasattr(client, 'close'):
            client.close()

@with_langtrace_root_span()
def call_o1_mini(prompt):
    print(f"calling o1-mini with prompt: {prompt}")
    with openai_session() as client:
        try:
            client = openai.OpenAI()
        
        # Call API
            response = client.chat.completions.create(
                model="o1-mini",  # Replace with the appropriate model
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract response text
            result = response.choices[0].message.content
            return result
        
        except Exception as e:
            return f"Error generating output: {str(e)}"
    

@with_langtrace_root_span()
def call_4o_mini(prompt):
    print(f"calling 4o-mini with prompt: {prompt}")
    with openai_session() as client:
        try:
            client = openai.OpenAI()
        
        # Call API
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Replace with the appropriate model
                # model="chatgpt-4o-latest",  # Replace with the appropriate model
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract response text
            result = response.choices[0].message.content
            return result
        
        except Exception as e:
            return f"Error generating output: {str(e)}"

class ProjectType(Enum):
    Page = "Page"
    Sage = "Sage"
    Engage = "Engage"

class Project:
    def __init__(self, project_type: ProjectType, session_id = None):
        self.project_type = project_type
        self.session_id = session_id 

        # requirement_rubric, fetch from db
        # then retrive from here again, omit recalls to fetch the same thing over and over
        self.rubric = [] 
        self.rubric_section_names = []
        self.project_detail = []
        self.structured_qa = ""
        self.component_list = []
        self.component_csv = ""
        self.flared_csv = ""

    def set_rubric(self,rubric):
        self.rubric = rubric

    def set_component_csv(self,component_csv):
        self.component_csv = component_csv

    def get_component_csv(self):
        return self.component_csv

    def set_component_list(self,component_list):
        self.component_list = component_list

    def set_rubric_section_names(self,rubric_section_names):
        self.rubric_section_names = rubric_section_names

    def set_project_detail(self,project_detail):
        self.project_detail = project_detail

    def add_project_detail(self,project_detail):
        self.project_detail.append(project_detail)

    def get_project_detail(self):
        return(self.project_detail)
    
    # the rubric to generate project questions
    def project_question_generation_rubric(self, ):
        headers = [ 'Criteria', 'Initial Questions', 'Quantifiable Value']
        # table = '| ' + ' | '.join(headers) + ' |'
        table = ' | '.join(headers) 
        # table += '\n' + '| ' + ' | '.join(['---'] * len(headers)) + ' |'
        
        # print(len(self.rubric))
        for entry in self.rubric:
            # print(entry)
            # table += f"\n{entry['criteria']} | {entry['explanation']} | {entry['priority']} | {entry['quantifiable_value'] or ''}"
            table += f"\n{entry['criteria']} | {entry['initial_question']} | {entry['quantifiable_value'] or ''}"
            # table += f"\n| {entry['section_name']} | {entry['criteria']} | {entry['explanation']} | {entry['priority']} | {entry['quantifiable_value'] or ''} |"
        return table
    
    # the rubric to grade answers project questions
    def project_question_grading_rubric(self):
        headers = ['Criteria', 'Explanation', 'Priority', 'Quantifiable Value']
        # headers = ['Criteria', 'Explanation', 'Priority', 'Quantifiable Value']
        # table = '| ' + ' | '.join(headers) + ' |'
        table = ' | '.join(headers) 
        # table += '\n' + '| ' + ' | '.join(['---'] * len(headers)) + ' |'
        
        # print(len(self.rubric))
        for entry in self.rubric:
            # print(entry)
            # table += f"\n{entry['criteria']} | {entry['explanation']} | {entry['priority']} | {entry['quantifiable_value'] or ''}"
            table += f"\n{entry['criteria']} | {entry['explanation']} | {entry['priority']} | {entry['quantifiable_value'] or ''}"
            # table += f"\n| {entry['section_name']} | {entry['criteria']} | {entry['explanation']} | {entry['priority']} | {entry['quantifiable_value'] or ''} |"
        return table

    # different pemutation of columns, to reduce token count
    def rubric_to_text(self):
        headers = ['Section Name', 'Criteria', 'Explanation', 'Priority', 'Quantifiable Value']
        # headers = ['Criteria', 'Explanation', 'Priority', 'Quantifiable Value']
        # table = '| ' + ' | '.join(headers) + ' |'
        table = ' | '.join(headers) 
        # table += '\n' + '| ' + ' | '.join(['---'] * len(headers)) + ' |'
        
        # print(len(self.rubric))
        for entry in self.rubric:
            # print(entry)
            # table += f"\n{entry['criteria']} | {entry['explanation']} | {entry['priority']} | {entry['quantifiable_value'] or ''}"
            table += f"\n{entry['section_name']} | {entry['criteria']} | {entry['explanation']} | {entry['priority']} | {entry['quantifiable_value'] or ''}"
            # table += f"\n| {entry['section_name']} | {entry['criteria']} | {entry['explanation']} | {entry['priority']} | {entry['quantifiable_value'] or ''} |"
        return table
    
    def rubric_to_verify(self):
        # headers = ['Section Name', 'Criteria', 'Explanation', "Priority"]
        headers = ['Criteria', 'Explanation', "Priority"]
        # table = '| ' + ' | '.join(headers) + ' |'
        table = ' | '.join(headers) 
        # table += '\n' + '| ' + ' | '.join(['---'] * len(headers)) + ' |'
        
        # print(len(self.rubric))
        for entry in self.rubric:
            merged_columns = entry['explanation'] + " " + (entry['quantifiable_value'] or '')
            # print(entry)
            table += f"\n {entry['criteria']} | {merged_columns} | {entry['priority']}"
            # table += f"\n| {entry['section_name']} | {entry['criteria']} | {entry['explanation']} | {entry['priority']} | {entry['quantifiable_value'] or ''} |"
        return table
    
    def component_to_text(self):
        # If input is empty, return empty string
        if not self.component_list:
            return ""
        
        # Get headers from the first row
        # headers = list(self.component_list[0].keys())
        headers = ["base_project_name", "module", "submodule","unit_type", "quantity"]
        # Create header row
        table = " | ".join(headers) + "\n"
        table += "-" * len(table) + "\n"
        
        # Add data rows
        for row in self.component_list:
                # Convert None values to empty strings and all values to strings
            values = [str(row[header]) if row[header] is not None else "" for header in headers]
            table += " | ".join(values) + "\n"
    
        return table
    
    def get_component_mandays(self):
        # If input is empty, return empty list
        if not self.component_list:
            return []
        
        # Define headers we want to extract
        headers = ["module", "submodule", "mandays_per_unit"]
        
        # Create list of dictionaries with only the headers we want
        result = []
        for row in self.component_list:
            filtered_row = {
                header: row[header] if row[header] is not None else "" 
                for header in headers
            }
            result.append(filtered_row)
    
        return result


    def generate_client_follow_up(self ,system_prompt = client_follow_up):
        # current_form = self.filter_non_empty_answer()
        prompt = f"""
        {system_prompt}

        # Input:
        ## Client Details / Project Requirement Q&A
        {self.project_detail}
        """


        # print(f"\n\generate_client_follow_up with prompt: {prompt}\n\n")
        result = call_o1_mini(prompt)
        # print(f"type, result : {type(result)}, {result}")

        return result
    
    def generate_questions(self, system_prompt=question_generator):
        prompt = f"""
        {system_prompt}

        # Input:
        ## Client Details / Project Requirement Q&A
        {self.project_detail}

        ## Requirement Rubric 
        {self.project_question_generation_rubric()}
        """

        # print(f"\n\generate_questions with prompt: {prompt}\n\n")
        result = call_o1_mini(prompt)
        # print(f"type, result : {type(result)}, {result}")
        return result
    
    def generate_follow_up(self ,system_prompt = followup_question_generator):
        # current_form = self.filter_non_empty_answer()
        prompt = f"""
        {system_prompt}

        # Input:
        ## Client Details / Project Requirement Q&A
        {self.project_detail}

        ## Requirement Rubric 
        {self.project_question_grading_rubric()}
        """

        # print(f"\n\generate_questions with prompt: {prompt}\n\n")
        result = call_o1_mini(prompt)
        return result

    def rewrite_qa(self,system_prompt = structure_qa):
        prompt = f"""
        {system_prompt}

        # Input:
        ## Client Details / Project Requirement Q&A
        {self.get_project_detail()}"""

        result = call_o1_mini(prompt)
        self.structured_qa = result
        # print(f"POPULATED TABLE : {result}")
        return result

    def flare_tasks(self, system_prompt = flare_task):
        # current_form = self.filter_non_empty_answer()
        # {self.get_project_detail()}

        prompt = f"""
        {system_prompt}

        # Input:
        {self.structured_qa}
    

        ## Component List 
        {self.component_to_text()}
        """

        # print(f"\n\ additional_tasks with prompt: {prompt}\n\n")
        result = call_o1_mini(prompt)

        self.flared_csv = result
        # self.set_component_csv(result)
        # print(f"POPULATED ADDITIONAL TASK TABLE : {result}")
        return result


    def populate_template_with_units(self, system_prompt = populate_csv):
        # current_form = self.filter_non_empty_answer()
        prompt = f"""
        {system_prompt}

        # Input:
        ## Client Details / Project Requirement Q&A
        {self.get_project_detail()}

        ## Component List 
        {self.component_to_text()}
        """

        # print(f"\n\populate_template_with_units with prompt: {prompt}\n\n")
        result = call_o1_mini(prompt)
        self.set_component_csv(result)
        # print(f"POPULATED TABLE : {result}")
        return result
    
    def populate_template_with_orgranised_qa(self, system_prompt = populate_csv_v2):
        # organised_qa = self.rewrite_qa()
        # current_form = self.filter_non_empty_answer()
        prompt = f"""
        {system_prompt}

        # Input:
        {self.structured_qa}

        

        ## Component / Tasks List 
        {self.flared_csv}
        """
        # print(f"\n\populate_template_with_units with prompt: {prompt}\n\n")
        result = call_o1_mini(prompt)
        self.set_component_csv(result)
        # print(f"POPULATED TABLE : {result}")
        return result
    
    def additional_tasks(self, system_prompt = missing_task):
        # current_form = self.filter_non_empty_answer()
        prompt = f"""
        {system_prompt}

        # Input:
        ## Client Details / Project Requirement Q&A
        {self.get_project_detail()}

        ## Componet List 
        {self.component_csv}
        """

        # print(f"\n\ additional_tasks with prompt: {prompt}\n\n")
        result = call_o1_mini(prompt)
        # self.set_component_csv(result)
        # print(f"POPULATED ADDITIONAL TASK TABLE : {result}")
        return result
    
    

    