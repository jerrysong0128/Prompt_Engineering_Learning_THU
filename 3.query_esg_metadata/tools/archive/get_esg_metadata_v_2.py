#For API
import os
#For Extract PDF
import fitz
from pdf2image import convert_from_path
import pytesseract
import requests
from io import BytesIO
#For OpenAI and Langchain
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
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

    # Extract text from the first page using image extraction (Different from the old code)
    images = convert_from_path(url, first_page=1, last_page=1)
    raw_text += pytesseract.image_to_string(images[0])

    # Extract text from the remaining pages
    for page_number in range(0,document.page_count):
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

# The industry classification list
category_industry = ["Energy Equipment & Services",
            "Oil, Gas & Consumable Fuels",
            "Chemicals",
            "Construction Materials",
            "Containers & Packaging",
            "Metals & Mining",
            "Paper & Forest Products",
            "Aerospace & Defense",
            "Building Products",
            "Construction & Engineering",
            "Electrical Equipment",
            "Industrial Conglomerates",
            "Machinery",
            "Trading Companies & Distributors",
            "Commercial Services & Supplies",
            "Professional Services",
            "Air Freight & Logistics",
            "Passenger Airlines",
            "Marine Transportation",
            "Ground Transportation",
            "Transportation Infrastructure",
            "Automobile Components",
            "Automobiles",
            "Household Durables",
            "Leisure Products",
            "Textiles, Apparel & Luxury Goods",
            "Hotels, Restaurants & Leisure",
            "Diversified Consumer Services",
            "Distributors",
            "Internet & Direct Marketing Retail",
            "Broadline Retail",
            "Specialty Retail",
            "Consumer Staples Distribution & Retail",
            "Beverages",
            "Food Products",
            "Tobacco",
            "Household Products",
            "Personal Care Products",
            "Health Care Equipment & Supplies",
            "Health Care Providers & Services",
            "Health Care Technology",
            "Biotechnology",
            "Pharmaceuticals",
            "Life Sciences Tools & Services",
            "Banks",
            "Thrifts & Mortgage Finance",
            " Financial Services",
            "Consumer Finance",
            "Capital Markets",
            "Mortgage Real Estate Investment",
            "Insurance",
            "IT Services",
            "Software",
            "Communications Equipment",
            "Technology Hardware, Storage & Peripherals",
            "Electronic Equipment, Instruments & Components",
            "Semiconductors & Semiconductor Equipment",
            "Diversified Telecommunication Services",
            "Wireless Telecommunication Services",
            "Media",
            "Entertainment",
            "Interactive Media & Services",
            "Electric Utilities",
            "Gas Utilities",
            "Multi-Utilities",
            "Water Utilities",
            "Independent Power and Renewable Electricity Producers",
            "Diversified REITs",
            "Industrial REITs",
            "Hotel & Resort REITs",
            "Office REITs",
            "Health Care REITs",
            "Residential REITs",
            "Retail REITs",
            "Specialized REITs",
            "Real Estate Management & Development"]


# Parser inject instructions
class ESG_Metadata(BaseModel):
    pdf_url: str = Field(description="Report PDF link (can be directly clicked to open.")
    report_title: str = Field(description="Report title (MUST be consistent with the name on the report cover)")
    language: str = Field(description="Report language (Chinese is distinguished between Simplified and Traditional. Bilingual reports can select multiple languages (Chinese, English))")
    report_time: str = Field(description="Report year (year the content reporting, e.g., '2023')")
    report_start_date: str = Field(description="Report start date (start date of the report content, e.g., '2020-01-01')")
    report_end_date: str = Field(description="Report end date (end date of the report content, e.g., '2020-12-31')")
    publication_time: str = Field(description="Report publication time (time when the report is published. If the exact date cannot be found, choose June 30 of that year)")
    country_code: str = Field(description="Country code (country where the company's headquarters is located in three letters. Examples: 1) CHN 2) JPN 3) USA")
    company_full_name: str = Field(description="Company full name (language should be consistent with the report language. For bilingual reports, choose English. Examples: 1) 小米集团 2) Honda Motor Co., Ltd.)")
    company_short_name: str = Field(description="Company short name (For bilingual reports, choose English. Examples: 1) Xiaomi 2) Honda)")
    category: str = Field(description=f"Main business industry classification (MUST select from the Global Industry Classification list {category_industry})")
    stock_code: str = Field(description="Stock code (stock code of the company)")
    stock_name: str = Field(description="Stock name (stock name of the company)")
    stock_market: str = Field(description="Stock market (stock market where the company is listed. Examples: 1)香港交易所, 2)NYSE, 3)上海交易所, 4)LSE)(HINT: Might be inferred from the pdf url)")


# Set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=ESG_Metadata)


# Define the prompt template
prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


# Define the model (Most Important!!!)
model_ESG_Metadata = prompt | llm | parser


# Define the function to query ESG metadata
def query_ESG_Metadata(url: str) -> None:
    report_text = extract_pdf_text_from_url(url)
    content=f"The pdf ({url}) is an ESG report from a company.\
    The pdf contains the following text:\n{report_text}\
    MUST RETURN (in PDF's language):\
    1. The title of the report\
    2. The language of the report.\
    3. The reporting period.\
    4. The start date of the report content.\
    5. The end date of the report content.\
    6. The publication time of the report.\
    7. The the country code.\
    8. The full name of the company.\
    9. The short name of the company.\
    10. The Industry classification of the company's main business operations.\
    11. The stock code.\
    12. The stock name.\
    13. The stock market where company listed.\
    Fill 'Nan' if the information is not available.\
    "
    return model_ESG_Metadata.invoke({"query": content})


# End of the code