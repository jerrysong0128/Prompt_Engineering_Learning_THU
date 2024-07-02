Corresponding Author: Jerry Song; [jerrysong0128@gmail.com](mailto:jerrysong0128@gmail.com)

This repository contains the prompt engineering projects developed during my research assistant period at Tsinghua University. The critical files and first-level folders are disclosed in the following structure:
```markdown
├── 1.edge-functions-supabase/
│   └── supabase
├── 2.langchain-langgraph-learning/
│   ├── direct_chat_Legacy
│   ├── learning_Langchain_agent-tool
│   ├── learning_langgraph
│   └── query_esg_metadate_with_langgraph
│   │    ├── v_1_langgraph-multi-agent-ESG.ipynb
│   │    ├── v_2_Langgraph-agent-supervisor-ESG.ipynb
│   │    └── v_3_Langgraph-agent-langgraph-ESG.ipynb
├── 3.query_esg_metadata/
│   ├── out
│   ├── tools
│   │    ├── get_esg_language.py
│   │    └── get_esg_metadata_with_lan.py
│   ├── main.py
│   └── test.py
└── README.md
```

## Project 1: Searching the embedding using edge functions and supabse

```markdown
├── supabase/
│   └── functions/
│   │    ├── search/
│   │    │    └──index.ts
│   │    └── search-jerry/
│   │    │    └──index.ts
│   └── migrations/
```
This project demonstrates how to perform searches using edge functions in Supabase. It includes two main search implementations:

- **search/**: This function performs direct searches within Supabase's inherent database.
- **search-jerry/**: This revised version enhances the search capability by utilizing PINECONE, a more advanced vector database designed for storing embeddings.

## Project 2: Query the ESG metadate from a report url using Langgraph

### v_1_langgraph-multi-agent-ESG

![v_1_langgraph-multi-agent-ESG](/2.langchain-langgraph-learning/query_esg_metadate_with_langgraph/archive/v_1_langgraph-multi-agent-ESG.jpeg)

### v_2_Langgraph-agent-supervisor-ESG

![v_2_Langgraph-agent-supervisor-ESG](/2.langchain-langgraph-learning/query_esg_metadate_with_langgraph/archive/v_2_Langgraph-agent-supervisor-ESG.jpeg)

### v_3_Langgraph-agent-langgraph-ESG

To be continue

## Project 3: Query the ESG metadate from a report url using Langchain and revised output

This project focuses on extracting metadata from PDF reports. The process involves identifying the language of the PDF to apply the appropriate OCR techniques. The roadmap for this project includes:

- **Language Identification**: Capturing characters in the PDF to identify the language(s) used (e.g., Chinese Traditional + English). This psrt still using llm.
- **PDF Unstructuring**: Using the identified language(s) to unstructure the PDF content accurately.
- **Metadata Extraction**: Outputting the text and string data to extract the metadata from the PDF report.
