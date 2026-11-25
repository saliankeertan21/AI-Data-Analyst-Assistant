import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

import schemas as sc


from dotenv import load_dotenv
import os

load_dotenv()



# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    max_retries=2,
    api_key = os.getenv("GOOGLE_API_KEY")
    
)

# Create a parser using our Pydantic schema
parser = PydanticOutputParser(
    pydantic_object=sc.BusinessAnalysis
)

# Define the instructions and user input
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an experienced business analyst.

        Analyse the business problem carefully.

        Provide realistic and actionable recommendations.
        Do not invent numerical data or claim that assumptions
        are verified facts.

        If information is insufficient, state the uncertainty.

        {format_instructions}
        """
    ),
    (
        "human",
        "Analyse this business problem: {question}"
    )
])

# Insert the parser's formatting instructions
prompt = prompt.partial(
    format_instructions=parser.get_format_instructions()
)

# Connect the components into one chain
analysis_chain = prompt | llm | parser


def analyze_business_problem(question: str) -> sc.BusinessAnalysis:
    if not question.strip():
        raise ValueError("Please enter a business problem.")

    result = analysis_chain.invoke({
        "question": question
    })

    return result


# Execute and print to console


if __name__== "__main__":
    sample_question="why are sales increasing by 25%?"

    print("analyzing the problem...\n")
    analysis= analyze_business_problem(sample_question)

    print(analysis.model_dump_json(indent=2))
    