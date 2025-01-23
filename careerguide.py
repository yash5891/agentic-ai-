from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from textblob import TextBlob
# Load environment variables
load_dotenv()

class AutomatedTaskGenerator:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")

        # Initialize the LLM
        self.llm = ChatGroq(
            temperature=0.7,
            groq_api_key=self.groq_api_key,
            model_name="mixtral-8x7b-32768"
        )

    def generate_about_company(self, company: str) -> str:
        """
        Generate a description of the company including:
        - Headquarters
        - Unique selling proposition (USP)
        - Owner or key executives
        - A brief overview of their services or products.
        """
        prompt = f"""
        Provide a short description of {company} including:
        - Headquarters
        - Unique selling proposition (USP)
        - Owner or key executives
        - A brief overview of their services or products.
        """
        return self.llm.predict(prompt)

    def generate_case_study(self, company: str, profession: str) -> str:
        """
        Generate a concise real-life case study of the company where they faced a major challenge.
        The case study will highlight the role and contributions of the profession during the crisis.
        """
        prompt = f"""
        Provide a concise real-life case study of {company} in which they faced a major challenge. 
        The case study should:
        - Be 4-6 sentences long.
        - Include the crisis or challenge faced by the company.
        - Highlight the specific role and contributions of a {profession} in addressing the crisis.
        - Focus on how the situation was managed and the outcomes achieved.
        """
        return self.llm.predict(prompt)

    
    def generate_work_done(self, profession: str, company: str) -> list:
        """
        Generate exactly 8 work done points for the professional during the crisis at the company.
        Each task should be tied to the crisis and the professional's contributions.
        """
        prompt = f"""
        Based on the case study of {company}, provide a factual list of exactly 8 specific tasks performed by a {profession}.
        - Each task should directly address the crisis and the professional's role.
        - Ensure there are exactly 8 points.
        - Tasks should be concise and specific.
        """
        
        # Run the prompt until we get exactly 8 tasks
        tasks = []
        while len(tasks) != 8:
            response = self.llm.predict(prompt)
            tasks = response.strip().split("\n")

        # Ensure we have exactly 8 tasks
        return tasks[:8]# Ensure only 8 points are returned

    def generate_task(self, work_done_point: str, company: str) -> dict:
        """
        Generate a task with a question, additional information (data/requirements), and outcome.
        """
        prompt = f"""
        For the task '{work_done_point}' during the crisis at {company}, provide the details in the following structure:
        1. **Task  (Question)**: Provide a task with question 
        2. **Additional Information (Data/Requirements)**: List 2-3 specific data points, tools, resources, or knowledge necessary to perform this task successfully.
        These could include information or data that will help solve the task.
        3. **Task Outcome**: Clearly state the outcome of the task, highlighting the impact it had on the company, and the resolution of the crisis.
        Ensure the response follows this structure exactly.
        """
        response = self.llm.predict(prompt)

        # Parse the response into sections
        lines = response.strip().split("\n")
        task_description = ""
        additional_info = []
        task_outcome = []
        current_section = "description"

        for line in lines:
            if "Additional Information:" in line:
                current_section = "additional_info"
                continue
            elif "Task Outcome:" in line:
                current_section = "outcome"
                continue

            if current_section == "description":
                task_description += line.strip() + " "
            elif current_section == "additional_info":
                if line.strip():
                    additional_info.append(line.strip())
            elif current_section == "outcome":
                if line.strip():
                    task_outcome.append(line.strip())

        return {
            "description": task_description.strip(),
            "additional_info": additional_info,
            "outcome": task_outcome,
        }

    def generate_summary_of_learning(self, profession: str, company: str) -> str:
            """
            Generate a dynamic summary of learning after all the tasks are completed.
            """
            prompt = f"""
            Generate a summary of learning for a {profession} at {company}, where they faced a crisis. The summary should highlight:
            - Key lessons learned from the crisis.
            - How the professional adapted and contributed.
            - The impact of their actions on the resolution of the crisis.
            Ensure the summary is specific to the profession and company.
            """
            return self.llm.predict(prompt)
    def correct_grammar(self, text: str) -> str:
        """
        Correct the grammar of the given text using TextBlob (Python-based solution).
        """
        blob = TextBlob(text)
        corrected_text = blob.correct()  # Automatically corrects spelling and basic grammar issues
        return str(corrected_text)

def main():
    print("Starting the Automated Task Generator...")
    generator = AutomatedTaskGenerator()

    print("📚 Automated Task Generator 📚")
    print("=" * 60)

    # Input details
    company = input("Enter the company name (e.g., 'Apollo Hospitals'): ").strip()
    profession = input("Enter the profession (e.g., 'Risk Analyst'): ").strip()

    # Step 1: About the Company
    print(f"\n### About {company} ###")
    about_company = generator.generate_about_company(company)
    print(about_company)

    # Step 2: Case Study
    print(f"\n### Case Study: {company} ###")
    case_study = generator.generate_case_study(company, profession)
    print(case_study)

    # Step 3: Work Done by the Professional (Strictly 8 Points)
    print(f"\n### Work Done by a {profession} at {company} ###")
    work_done = generator.generate_work_done(profession, company)
    for i, point in enumerate(work_done, 1):
        print(f"{i}. {point}")

    # Step 4: Tasks
    tasks = []
    print(f"\n### Tasks ###")
    for i, work_point in enumerate(work_done, 1):
        task = generator.generate_task(work_point, company)
        tasks.append(task)
        print(f"\nTask {i}:")
        print(f"Task Description (Question): {task['description']}")
        print(f"Additional Information (Data/Requirements): {', '.join(task['additional_info'])}")
        print(f"Task Outcome: {', '.join(task['outcome'])}")

    # Step 5: Generate and print the summary of learning after all tasks
    summary = generator.generate_summary_of_learning(profession, company)
    print(f"\n### Summary of Learning ###")
    print(summary)

if __name__ == "__main__":
    main()
