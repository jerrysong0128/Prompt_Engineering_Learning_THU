#For API
import os
#For Extract PDF
import fitz  
import requests
from io import BytesIO
#For OpenAI and Langchain
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field, conlist, constr
from langchain_core.prompts import PromptTemplate

# Get the OpenAI API key from the environment (Should be Revised)
openai_api_key = os.getenv('OPENAI_API_KEY')


# define the function to extract text from a PDF file
def extract_pdf_text_from_url(
        url: str
        ) -> str:
    """
    Extracts text from a PDF file available at a given URL.
    Args:
        url (str): The URL of the PDF file.
    Returns:
        str: The extracted text, limited to 2500 characters.    
    Raises:
        ValueError: If the URL is invalid or the file is not a PDF.
    """
    # Download the PDF file
    response = requests.get(url)

    # Raise an exception if the URL is invalid
    if response.status_code != 200:
        raise ValueError("Invalid URL")

    #Raise an exception if the file is not a pdf
    if response.headers['Content-Type'] != 'application/pdf':
        raise ValueError("The file is not a PDF")

    pdf_data = BytesIO(response.content)

    # Open the PDF file
    document = fitz.open(stream=pdf_data, filetype="pdf")

    # Iterate pages to read the text from each page
    raw_text = ""
    for page_number in range(document.page_count):
        page = document.load_page(page_number)
        raw_text += page.get_text()

    # Limit the text to 2500 characters
    cutted_text = raw_text[:2500]

    return cutted_text


# Define the llm model
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0
)

# The language classification list
language_type = ["chi_sim",
            "chi_tra",
            "eng",
            "fra",
            "jpn",
            "kor",
            "spa"]

# Define a validator for the language field
LanguageStr = constr(regex=f"^({'|'.join(language_type)})$")
LanguageListType = conlist(LanguageStr, min_items=1)

# Parser inject instructions
class ESG_Language(BaseModel):
    id: int
    pdf_url: str = Field(
        description="Report PDF link (can be directly clicked to open)."
        )
    language: LanguageListType  = Field(
        description=f"Major Report language \
                (MUST clearly distinguish between Traditional Chinese (chi_tra) and Simplified Chinese (chi_sim).\
                MUST Select from the list {language_type}.\
                Bilingual reports can select multiple languages (if needed))."
    )

# Set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=ESG_Language)


# Define the prompt template
prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


# Define the model (Most Important!!!)
model_ESG_Metadata = prompt | llm | parser


# Define the function to query ESG metadata
def query_ESG_Lan(id: int, url: str) -> None:
    report_text = extract_pdf_text_from_url(url)
    content=f"The pdf ({url}) is an ESG report from a company with id MUST be ({id}).\
    The pdf contains the following text:\n{report_text}\
    MUST RETURN:\
    1. The id of the report.\
    2. The url of the report.\
    3. The language of the report.\
    "
    return model_ESG_Metadata.invoke({"query": content})


# End of the code