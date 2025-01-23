Automated Task Generator for Professional Knowledge Extraction
This project automates the process of extracting detailed information about a profession's role within a company. Using ChatGroq's LLM and TextBlob, it generates company profiles, case studies, work done, tasks, and learning summaries for a specific profession during a crisis.

Features
Company Information: Description of the company, key executives, and services.
Case Study: A brief case study of a company’s crisis and the professional's role.
Work Done: Generates 8 specific tasks performed by the professional during the crisis.
Task Details: Describes each task with a question, additional info, and outcome.
Summary of Learning: Highlights the key lessons learned by the professional.
Grammar Correction: Automatically corrects grammar using TextBlob.
Requirements
Python 3.x
langchain_groq
dotenv
textblob
Install dependencies:

bash

pip install langchain_groq textblob python-dotenv
Setup
Clone the repository and navigate to the directory.

Create a .env file with your GROQ_API_KEY:

text

GROQ_API_KEY=your_groq_api_key_here
Run the script:

bash

python main.py
Enter the company name and profession when prompted.

License
MIT License
