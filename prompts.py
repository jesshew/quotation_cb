client_initial_question = """
# Client Information Gathering Questions

### Company Background and Industry
1. Can you provide some background about your company?
2. Which industry do you operate in, and what is your company’s niche or specialization?
3. Who are your primary customers?
4. What are the main objectives you want to achieve?
5. What key features or functionalities do you need?

### Current Challenges
6. What are the biggest challenges your firm is currently facing?
7. Can you describe your current processes?

### Workflow and System Impact
8. How will this solution benefit your firm as a whole?

### Existing Workflow or System
9. Can you describe your current workflow or system?

### Pain Point Identification
10. Where is your current system falling short or causing delays?
11. Are there any parts of the process that are particularly time-consuming/ prone to error?"""

client_initial_question_v1 = """
# Client Information Gathering Questions

### Company Background and Industry
1. Can you provide some background about your company?
2. Which industry do you operate in, and what is your company’s niche or specialization?
3. Who are your primary customers, and what are their main needs or pain points?

### Project Goals and Objectives
4. What are your short-term goals for this project?
5. What are your long-term goals for this project?
6. What are the main objectives you want to achieve?
7. What key features or functionalities do you need?

### Current Challenges
8. What are the biggest challenges your firm is currently facing?
9. Can you describe your current processes?

### Workflow and System Impact
10. How do you envision this solution impacting your team's workflow?
11. How will this solution benefit your firm as a whole?

### Existing Workflow or System
12. Can you describe your current workflow or system?

### System Shortcomings and Efficiency
13. Where is your current system falling short or causing delays?
14. Are there any parts of the process that are particularly time-consuming?
15. Which areas are prone to errors in your current system?"""


client_follow_up_v1 = """
Based on the initial list of questions and the client’s provided answers, generate **insightful and targeted follow-up questions** that will help deepen my understanding of the following critical aspects:

1. **Client Overview**  
   **Objective:** Gain a comprehensive understanding of the client’s business, operations, and strategic goals to ensure the project aligns with their broader objectives.  

2. **Project Vision and Value**  
   **Objective:** Clarify the intended impact of the project on the client’s business. Understand how it will improve their processes, solve key challenges, and deliver measurable benefits.  
   **Focus:** Investigate specific outcomes, long-term goals, and how success will be defined.

3. **Existing System or Workflow Description**  
   **Objective:** Delve deeper into the client’s current tools, workflows, and processes to uncover pain points, integration requirements, and opportunities for optimization.  
   **Focus:** Identify inefficiencies, technical limitations, or gaps that the project will address.

4. **Budget and Resource Constraints**  
   **Objective:** Clearly define any limitations or constraints—financial, resource-based, or time-related—that could impact project success.  
   **Focus:** Understand the flexibility of the budget, timeline expectations, and resource availability.

---
**Instructions for Output:**  
- Generate follow-up questions that are tailored, specific, and actionable.  Keep the questions short and extremely readable / easy to understand 
- Each question should build upon the client’s initial responses, prompting them to provide more detailed or nuanced insights.  
- Include additional context or examples where appropriate to clarify the intent of the question.

Give your output as string in the following format:
question index.<question>\n
answer: <leave blank> 
"""

client_follow_up_v2 = """
Based on the initial list of questions and the client’s provided answers, generate **insightful and targeted follow-up questions** that will help deepen my understanding of the following critical aspects:

1. **Client Overview**  
   **Objective:** Gain a comprehensive understanding of the client’s business, operations, and strategic goals to ensure the project aligns with their broader objectives.  

2. **Project Vision and Value**  
   **Objective:** Clarify the intended impact of the project on the client’s business. Understand how it will improve their processes, solve key challenges, and deliver measurable benefits.  
   **Focus:** Investigate specific outcomes, long-term goals, and how success will be defined.

3. **Existing System or Workflow Description**  
   **Objective:** Delve deeper into the client’s current tools, workflows, and processes to uncover pain points, integration requirements, and opportunities for optimization.  
   **Focus:** Identify inefficiencies, technical limitations, or gaps that the project will address.

4. **Budget and Resource Constraints**  
   **Objective:** Clearly define any limitations or constraints—financial, resource-based, or time-related—that could impact project success.  
   **Focus:** Understand the flexibility of the budget, timeline expectations, and resource availability.

---
**Instructions for Output:**  
- Generate follow-up questions that are tailored, specific, and actionable.  Keep the questions short and extremely readable / easy to understand 
- Each question should build upon the client’s initial responses, prompting them to provide more detailed or nuanced insights.  
- Include additional context or examples where appropriate to clarify the intent of the question.

Give your output as string in the following format:
question index.<question>\n
answer: <leave blank> 
"""

client_follow_up = """
Based on the initial list of questions and the client’s provided answers, generate **insightful and targeted follow-up questions** that will help deepen my understanding of the following critical aspects:

1. **Client Overview**  
   **Objective:** ask relevant questions that will directly contribute to better project requirements gathering. (ie: department team that the project is meant for ..etc)

2. **Project Vision and Value**  
   **Objective:** Clarify the intended impact of the project on the client’s business. Understand how it will improve their processes, solve key challenges, and deliver measurable benefits.  
   **Focus:** Investigate specific outcomes, immediate expected goals, and how success will be defined.

3. **Existing System or Workflow Description**  
   **Objective:** Delve deeper into the client’s current tools, workflows, and processes to uncover pain points, integration requirements, and opportunities for optimization.  
   **Focus:** Identify inefficiencies, technical limitations, or gaps that the project will address.

4. **Budget and Resource Constraints**  
   **Objective:** Clearly define any limitations or constraints—financial, resource-based, or time-related—that could impact project success.  
   **Focus:** Understand the flexibility of the budget, timeline expectations, and resource availability.

Instructions:
Each question should:
Build on provided client information
Non repetitive, and unique. Avoid asking similar questions.
Include realistic sample answers relevant to the client's context
Focus on gathering quantifiable or specific information


Format responses as: 
<question> (<sample answers>)
Leave answer fields blank for client input
"""

client_follow_up = """
Based on the initial list of questions and the client’s provided answers, generate **insightful and targeted follow-up questions** that will help deepen my understanding of the following critical aspects:

1. **Client Overview**  
   **Objective:** ask relevant questions that will directly contribute to better project requirements gathering. (ie: department team that the project is meant for ..etc)

2. **Project Vision and Value**  
   **Objective:** Clarify the intended impact of the project on the client’s business. Understand how it will improve their processes, solve key challenges, and deliver measurable benefits.  
   **Focus:** Investigate specific outcomes, immediate expected goals, and how success will be defined.

3. **Existing System or Workflow Description**  
   **Objective:** Delve deeper into the client’s current tools, workflows, and processes to uncover pain points, integration requirements, and opportunities for optimization.  
   **Focus:** Identify inefficiencies, technical limitations, or gaps that the project will address.

4. **Budget and Resource Constraints**  
   **Objective:** Clearly define any limitations or constraints—financial, resource-based, or time-related—that could impact project success.  
   **Focus:** Understand the flexibility of the budget, timeline expectations, and resource availability.

Instructions:
Each question should:
Build on provided client information
Non repetitive, and unique. Avoid asking similar questions.
Include realistic sample answers relevant to the client's context
Focus on gathering quantifiable or specific information


Output top 10 questions in the following format: 
<question>(sample answers)
Just return the text and NOTHING else. Do not overexplain, omit code guards.
"""



question_generator = """
You are a chatbot project manager responsible for gathering detailed requirements in order to generate an accurate and comprehensive quotation for a client’s chatbot project. 
Your task is to ask good follow up questions based on what you already know
Consider the following inputs:

1. **Requirements Rubric:** Use this as a baseline list of initial questions of the chatbot project
2. **Project Details:** Background information on the client, industry, and high-level project requirements.

### Instructions:
- Analyze the rubric and project details to generate clear, concise, succinct questions
- If the project requirement already includes an answer to a question in the rubric, do not generate that question.
- Ensure your generated questions are highly relevant and specific to the client's business context. Avoid general or vague questions; tailor each question to the client's specific operations.


### Output Format:
Give your output as string in the following format:
<index><question>

Just return the string text and NOTHING else, omit code guards.
"""

question_generator_v1 = """
You are a chatbot project manager responsible for gathering detailed requirements in order to generate an accurate and comprehensive quotation for a client’s chatbot project. 
Your task is to ask good follow up questions based on what you already know
Consider the following inputs:

1. **Requirements Rubric:** Use this as a baseline list of initial questions of the chatbot project
2. **Project Details:** Background information on the client, industry, and high-level project requirements.

### Instructions:
- Analyze the rubric and project details to generate clear, concise, succinct questions
- Ensure your generated questions are highly relevant and specific to the client's business context. Avoid general or vague questions; tailor each question to the client's specific operations.


### Output Format:
Give your output as string in the following format:
<index><question>

Just return the string text and NOTHING else, omit code guards.
"""

followup_question_generator_v1="""
You are a meticulous evaluator that grades the completeness of answers based on a given rubric. Your role is to thoroughly analyze the answer and the rubric provided, 
assign a percentage score based on how well the answer meets the criteria outlined in the rubric, then generate an extensive list of follow up questions to close the gap.

Follow these steps:
1. **Understand the Context**: Carefully read through the rubric to understand the expectations and criteria for evaluation.
2. **Assess the Answer**: Analyze the answer provided and identify which elements of the rubric are addressed and to what extent.    - Check if the answer explicitly mentions or addresses all the quantifiable criteria listed in the rubric (e.g., "10 intents required, 8 provided").
3. **Grade Completeness**:
   - If the answer meets all aspects of the rubric comprehensively, assign a score of 100%.
   - If some criteria are partially met, deduct points based on the weight of the missing or incomplete criteria.
   - Deduct points proportionally for missing values.
   - If significant parts of the rubric are missing, assign a proportionately lower score.
4. Generate clear, concise, succinct follow up questions, Each question should:
    - Build on provided client information, Aimed to close a specific gap
    - Include realistic sample options relevant to the client's context
Output everything in a nice format as string
Give your output as string in the following format:
<index><question>

Just return the string text and NOTHING else, omit code guards.
"""

followup_question_generator="""
You are a meticulous evaluator that grades the completeness of answers based on a given rubric. Your role is to thoroughly analyze the answer and rubric provided, then generate thoughtful follow-up questions that reference specific details from the response while addressing gaps in the rubric criteria.
Follow these steps:

Understand the Context:

Carefully read through the rubric to understand the expectations and criteria for evaluation
Note key terms, concepts, and specific requirements mentioned


Assess the Answer:

Analyze how the provided answer aligns with rubric elements
Identify both explicit statements and implicit assumptions in the response
Map specific phrases or examples given against rubric requirements
Track any metrics or quantities mentioned versus those required


Generate Contextual Questions:
Create questions that HAS NOT BEEN answered and:

Reference specific details or examples provided in the answer
Bridge identified gaps between the response and rubric requirements
Build upon the respondent's stated approach or methodology
Include relevant industry-specific examples based on their context
Connect different aspects of their response to create deeper insights

Output the top 8 questions as a simple list,with each question demonstrating clear connection to previously stated information
"""

 
# uses feedback instead of the answer
extensive_question_generator= """You are tasked with generating a comprehensive list of questions based on a provided Requirements Rubric and Project Details. 
Use the structure and criteria from the rubric to create a list of specific, actionable, and quantifiable questions tailored to the given project context. Format the output as a properly indexed string list.

Inputs:

Requirements Rubric: A detailed document that includes section names, criteria, explanations, priority, and quantifiable values.
Project Details: Background information including the client name, industry, project goals, and any relevant high-level details.
Expected Output: An list of questions based on the rubric criteria and tailored to the provided project details. 
Each question should directly address a section and criterion from the rubric, ensuring it aligns with the client's industry, project objectives, and potential challenges.
### Output Format: String, with just the list of questions, do not explain anything.
"""






"""
Clearly defines the main purposes of the project, ensuring all stakeholders understand the core goals.
Identifies current business challenges to ensure that the requirements address real and pressing issues.
Specifies responsibilities and processes for updating and integrating new content, ensuring data remains current and accurate.
Lists required knowledge resources and assesses data quality to facilitate effective use and minimize data cleaning efforts.
Outlines necessary preprocessing steps to maintain data consistency and organization.
Details the scope of web scraping activities, including the number of websites and pages, to ensure comprehensive data acquisition.

Intent Definitions (High Priority)
Intermediate, Fallback, Single-Step, Multi-Step, Simple Intents
Clearly categorizes various user intents with examples, ensuring the chatbot can handle a wide range of interactions effectively.
Provides end-to-end example flows to illustrate user interactions, making it easy to manage expectations.

Improved Development Process: Enhances clarity and completeness of chatbot functionalities.
Enhanced Communication: Aligns developer understanding with user interaction expectations.
Setting Clear Expectations: Defines specific interaction scenarios and success criteria.
4. Performance & Scalability
Usage Expectations and Concurrent User Load (High Priority)
Defines expected usage volumes and simultaneous user capacity, ensuring the system can handle projected demand.
Peak Usage Patterns (High Priority)
Identifies peak hours and volumes to optimize performance during high-demand periods.
Performance Requirements (Medium Priority)
Specifies response times and reliability standards to maintain optimal performance.
Managing Multiple Requests and Future Growth Accommodation (Medium to Low Priority)
Outlines strategies for handling simultaneous tasks and accommodating future scalability needs.
Contribution to Outcomes:

Improved Development Process: Ensures system robustness and reliability.
Seamless Post-Production Monitoring: Facilitates performance tracking and scalability planning.
Setting Clear Expectations: Establishes clear performance benchmarks and scalability plans.
5. Technical Integration
Database Interaction, Integration with Existing Platforms, AI Integration, Action Execution and System Usage, Platform Needs, Hosting and Deployment Needs (High Priority)
Details requirements for system integrations, AI functionalities, action executions, platform support, and deployment preferences to ensure seamless technical operations.
Contribution to Outcomes:

Improved Development Process: Streamlines integration with existing systems and technologies.
Enhanced Communication: Clarifies technical dependencies and requirements.
Setting Clear Expectations: Defines specific technical integration points and deployment strategies.
6. User Experience
User Personas (High Priority)
Identifies key user groups and their needs to tailor the chatbot’s functionality and interactions effectively.
Feedback Mechanisms Implementation and Language/Tone/Personality (Medium Priority)
Establishes methods for collecting user feedback and defines the chatbot’s communication style to enhance user satisfaction and continuous improvement.
Contribution to Outcomes:

Enhanced Client Relationship and Communication: Aligns the chatbot’s design with user expectations and preferences.
Seamless Post-Production Monitoring: Implements feedback loops for ongoing enhancements.
Setting Clear Expectations: Defines user-centric design criteria and success measures.
7. User Support
Automatic Handover Triggers (High Priority)
Specifies conditions under which the chatbot should escalate issues to human agents, ensuring user issues are appropriately addressed.
Data Sharing During Handover (Medium Priority)
Defines what user information should be transferred to live agents to maintain context and continuity.
Contribution to Outcomes:

Enhanced Client Relationship and Communication: Ensures seamless support transitions.
Setting Clear Expectations: Clarifies support escalation processes and data handling protocols.
8. Security & Compliance
Handling Sensitive Data (Medium Priority)
Addresses the management of sensitive information and adherence to industry-specific regulations, ensuring data security and compliance.
Contribution to Outcomes:

Improved Development Process: Integrates security requirements into the development lifecycle.
Setting Clear Expectations: Defines compliance standards and data handling procedures.
9. System Reliability
Fallback Procedures for System Failures (Medium Priority)
Outlines actions to mitigate system downtime impacts, ensuring minimal disruption to users.
Maintenance (Low Priority)
Details maintenance schedules and requirements to sustain system reliability over time.
Contribution to Outcomes:

Seamless Post-Production Monitoring: Ensures ongoing system reliability and user trust.
Setting Clear Expectations: Defines contingency plans and maintenance responsibilities.
Conclusion
An exceptional project requirement is characterized by its clarity, completeness, feasibility, and alignment with business objectives. By meticulously addressing each component outlined in the Requirements Rubric—ranging from business objectives and data management to technical integration and user experience—requirements can significantly enhance the development process, foster robust client relationships, ensure effective post-production monitoring, and set clear, achievable expectations. Prioritizing high-impact areas ensures that critical aspects are thoroughly addressed, while medium and low-priority elements support sustained project success and adaptability."""




grade_completeness_prompt="""
You are a meticulous evaluator that grades the completeness of answers based on a given rubric. Your role is to thoroughly analyze the answer and the rubric provided, and assign a percentage score based on how well the answer meets the criteria outlined in the rubric. Follow these steps:

1. **Understand the Context**: Carefully read through the rubric to understand the expectations and criteria for evaluation.
2. **Assess the Answer**: Analyze the answer provided and identify which elements of the rubric are addressed and to what extent.    - Check if the answer explicitly mentions or addresses all the quantifiable criteria listed in the rubric (e.g., "10 intents required, 8 provided").
3. **Grade Completeness**:
   - If the answer meets all aspects of the rubric comprehensively, assign a score of 100%.
   - If some criteria are partially met, deduct points based on the weight of the missing or incomplete criteria.
   - Deduct points proportionally for missing values.
   - If significant parts of the rubric are missing, assign a proportionately lower score.
4. **Output**: Return the final score as a JSON object, just give the JSON object and nothing else
{"score":<INT VALUE>, "area_to_improve":<top 3 feedback and actionable next steps>, "category_to_focus" :<List top 3 category key>, "category_to_quantify":<List top 3 category key>}  

Just return the json item and NOTHING else, omit code guards.
"""

missing_task= """You are an AI assistant tasked with analyzing a detailed client requirements document for a chatbot project and a populated components breakdown sheet. Your task is to identify missing ALL tasks/components that are not explicitly mentioned. 

Do the following: 

Analyze the Inputs:
Thoroughly review the client requirements document
Cross-check these insights with the populated breakdown sheet to identify missing Components/Tasks
For each identified task, propose a submodule and its associated unit type (e.g., "Per Language," "Per Entity," "One Time").

Provide a logical calculation for the quantity of each unit type required. Refer to the client’s requirements (e.g., language diversity, user demographics, expected chatbot usage volume).
Output Format:
list ALL missing tasks as a csv with Module,Submodule,Unit Type,Quantity,Mandays per Unit,Remarks column
-Just return the csv text and NOTHING else, omit code guards.
"""

flare_task_v1= """You are an expert AI consultant specializing in task decomposition and detailed project planning. Your role is to cross-reference the provided client requirements document and the components sheet to generate a granular list of tasks that needs to be done. Make sure the list is EXTREMELY GRANULAR and covers the entire software development lifecycle

Use the components sheet as the baseline.
Ensure tasks align with client goals, challenges, and functional needs outlined in the requirements document.
Ensure each task specifies the corresponding unit_type (i:e., "Per Channel," "Per Integration," "One Time").

The tasks should be presented as a CSV-formatted string
Just return the csv text and NOTHING else, omit the ``` code guards.
"""

flare_task_v2= """You are an expert AI consultant specializing in task decomposition and detailed project planning. Your role is to cross-reference the provided client requirements document and the components sheet to generate a granular list of tasks. For similar tasks with identical unit types, group them together under a single consolidated task, specifying the quantity to avoid unnecessary granularity.

Use the components sheet as the baseline. Ensure tasks align with client goals, challenges, and functional needs outlined in the requirements document. Ensure each consolidated task specifies the corresponding unit_type (e.g., "Per Channel," "Per Integration," "One Time") and includes the total quantity.

The tasks should be presented as a CSV-formatted string. Just return the CSV text and NOTHING else, omit the ``` code guards.
"""

flare_task= """As an expert AI consultant specializing in task decomposition and project planning, analyze the provided project documentation to create a structured breakdown of tasks. Your analysis should:

Cross-reference the requirements document against the component list to identify and group related tasks

Consolidate similar tasks that share:
The same type of work
Similar objectives
Identical unit types
Common implementation patterns


Create logical groupings while maintaining separation for:
Chatbot flow type (Canned, Raged, NER, Simple Step)
Testing activities (unit, integration, performance)
Deployment stages
Security implementations
Monitoring systems
Maintenance tasks
Cost/billing components
Distinct business flows


For each consolidated task, provide:
Clear scope
Description
Unit type (e.g., "Per Instance", "One Time")
Total quantity (min 1)
Estimated Mandays for EACH unit within range of (0.25 - 2)

Format the output as a CSV with these columns:
task_name, description, unit_type, quantity, mandays_per_unit
   
- Make sure you encapsulate all TEXT column in "" 
- Omit ``` code guards and additional commentary."""

flare_task_quotationv3= """As an expert AI consultant specializing in task decomposition and project planning, analyze the provided project documentation to create a structured breakdown of tasks. Your analysis should:

Cross-reference the requirements document against the component list to identify and group related tasks

Consolidate similar tasks that share:
The same type of work
Similar objectives
Identical unit types
Common implementation patterns


Create logical groupings while maintaining separation for:
Chatbot flow type (Canned, Raged, NER, Simple Step)
Testing activities (unit, integration, performance)
Deployment stages
Security implementations
Monitoring systems
Maintenance tasks
Cost/billing components
Distinct business flows


For each consolidated task, provide:
Clear scope
Description
Unit type (e.g., "Per Instance", "One Time")
Estimated Mandays for EACH unit within range of (0.25 - 2)

Format the output as a CSV with these columns:
task_name, description, unit_type, mandays_per_unit
   
- Make sure you encapsulate all TEXT column in "" 
- Omit ``` code guards and additional commentary."""

populate_csv_v1 = """"
You are an expert AI consultant tasked with cross-referencing a detailed client requirements document and a components/pricing breakdown sheet for a chatbot project. 
Your job is to map each client requirement to the most appropriate components from the breakdown sheet and determine the exact number of units required based on logical calculations. 
DO NOT CHANGE the column "mandays_per_unit", THAT IS PREDEFINED. 
Use the following methodology:

1. **Mapping Client Requirements to Components**:
   - **One-to-One Mapping**: If a single component fully satisfies a requirement, map it directly.
     Example: "Track order status" → API-based Simple.
   - **One-to-Many Mapping**: If multiple components are needed to fulfill a requirement, list all the components.
     Example: "Multilingual chatbot" → Language Support (Translation Provided) + Intent Classifier.

2. **Logical Calculation of Units**:
   - Use the "Unit Type" column in the breakdown sheet to determine the number of units.
   - Provide logical justifications for each calculation:
     - **Per Language**: For services like "Language Translation Services," calculate the number of languages specified in the requirements.
       Example: For a client from Malaysia who needs Malay, English, and Mandarin, allocate 3 units.
     - **Per Entity**: For services like "Named Entity Recognition," count the distinct entities mentioned.
       Example: For identifying "order ID," "customer name," and "phone number," allocate 3 units.
     - **Per API Call**: For API-related components, estimate the number of calls based on expected traffic or usage.
   - Highlight any assumptions made during calculation.

3. **Output Format(csv txt)**:
   - Original Csv with Quantity populated, with a new remarks column. Clearly document all decision and assumptions made
   - make sure you encapsulate all TEXT column in "", and keep numeric columns as is.
-Just return the csv text and NOTHING else, omit the ``` code guards.
"""

populate_csv = """"
You are an expert AI consultant tasked with cross-referencing a detailed client requirements document and a components/pricing breakdown sheet for a chatbot project. 
Your job is to map each client requirement to the most appropriate components from the breakdown sheet and determine the exact number of units required based on logical calculations. 
Use the following methodology:

1. **Mapping Client Requirements to Components**:
   - **One-to-One Mapping**: If a single component fully satisfies a requirement, map it directly.
     Example: "Track order status" → API-based Simple.
   - **One-to-Many Mapping**: If multiple components are needed to fulfill a requirement, list all the components.
     Example: "Multilingual chatbot" → Language Support (Translation Provided) + Intent Classifier.

2. **Logical Calculation of Units**:
   - Use the "Unit Type" column in the breakdown sheet to determine the number of units.
   - Provide logical justifications for each calculation:
     - **Per Language**: For services like "Language Translation Services," calculate the number of languages specified in the requirements.
       Example: For a client from Malaysia who needs Malay, English, and Mandarin, allocate 3 units.
     - **Per Entity**: For services like "Named Entity Recognition," count the distinct entities mentioned.
       Example: For identifying "order ID," "customer name," and "phone number," allocate 3 units.
     - **Per API Call**: For API-related components, estimate the number of calls based on expected traffic or usage.
   - Highlight any assumptions made during calculation.

3. **Output Format(csv txt)**:
   - Csv with the columns "base_project_name","module","submodule","unit_type","quantity","remarks"; Clearly document all decision and assumptions made in the remarks column.
   - make sure you encapsulate all TEXT column in "", and keep numeric columns as is.
-Just return the csv text and NOTHING else, omit the ``` code guards.
"""
populate_csv_v2 = """"
You are an expert AI consultant tasked with cross-referencing a detailed client requirements document and a task breakdown sheet for a chatbot project. 
Your job is to map each client requirement to the most appropriate components from the breakdown sheet and determine the exact number of units(quantity) required based on logical calculations. 
Use the following methodology:

1. **Mapping Client Requirements to Components**:
   - **One-to-One Mapping**: If a single component fully satisfies a requirement, map it directly.
     Example: "Track order status" → API-based Simple.
   - **One-to-Many Mapping**: If multiple components are needed to fulfill a requirement, list all the components.
     Example: "Multilingual chatbot" → Language Support (Translation Provided) + Intent Classifier.

2. **Logical Calculation of Units**:
   - Use the "unit_typee" column in the breakdown sheet to determine the number of units.
   - Provide logical justifications for each calculation:
     - **Per Language**: For services like "Language Translation Services," calculate the number of languages specified in the requirements.
       Example: For a client from Malaysia who needs Malay, English, and Mandarin, allocate 3 units.
     - **Per API Call**: For API-related components, estimate the number of calls based on expected traffic or usage.
   - Clearly Document what is included and Highlight any assumptions made during calculation.

3. **Output Format(csv)**:
   - just return csv with "task_name" "unit_type","mandays_per_unit","quantity","remarks";
   - Clearly document all decision and assumptions made in the remarks column.
   - make sure you encapsulate all TEXT column in "", and keep numeric columns as is.
-Just return the csv text and NOTHING else, omit the ``` code guards.
"""

structure_qa = """Rewrite this for clarity while keeping all specific details, metrics, and constraints.
Do not include context or assumptions beyond the input provided.
Structure the document to ensure clarity and logical flow.
"""