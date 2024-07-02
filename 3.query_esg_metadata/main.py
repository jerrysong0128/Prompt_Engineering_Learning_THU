from datetime import datetime
import pandas as pd
from tools.get_esg_language import query_ESG_Lan # only for language
from tools.get_esg_metadata_with_lan import query_ESG_Metadata # only for language
import random

# Define the id wanted
# id_wanted = range(52806,52810) # ids wanted

# Function to generate 5 random numbers between 0 and 56154
def generate_random_numbers():
    return [random.randint(0, 56154) for _ in range(5)]

# Generate the random numbers
id_wanted = generate_random_numbers()

# Read the test data
urls_df = pd.read_csv('<PATH_TO_URL>') #Your path to the CSV file
id_url_list = list(zip(urls_df['id'], urls_df['pdf_url']))
url_list_want = [id_url_list[i] for i in id_wanted]

# Define the df to store the ESG metadata
df_ESG_Metadata  = pd.DataFrame()

# Combine the functions to query the ESG metadata
def query_collection(id,url):
    respond_lan = query_ESG_Lan(id,url)
    if len(respond_lan["language"]) > 1:
        language_string = '+'.join(respond_lan["language"])
    else:
        language_string = respond_lan["language"][0]
    print(url,language_string)
    respond_Metadata = query_ESG_Metadata(id,url,language_string)
    return respond_Metadata


# Loop the url list and query the ESG metadata
for id_url in url_list_want:
    json_respond = query_collection(id_url[0],id_url[1])
    df_ESG_Metadata = pd.concat([df_ESG_Metadata, pd.DataFrame([json_respond])], axis=0)
    print(f"{json_respond}\nid: ", id_url[0], " Collected at: ", datetime.now().strftime("%H:%M:%S"), " Finished Total: ", len(df_ESG_Metadata))

# Save the df with a timestamped CSV file
now = datetime.now()
dt_string_now = now.strftime("%Y%m%d_%H%M%S")
df_ESG_Metadata.to_csv(f'./out/ESG_Report_Metadata_{dt_string_now}.csv', index=False)