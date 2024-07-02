import pandas as pd
from tools.get_esg_language import query_ESG_Lan # only for language


# Define the id wanted
id_wanted = range(256,260) # ids wanted

# Read the test data
urls_df = pd.read_csv('<PATH_TO_URL>') #Your path to the CSV file
id_url_list = list(zip(urls_df['id'], urls_df['pdf_url']))
url_list_want = [id_url_list[i] for i in id_wanted]



for id_url in url_list_want:
    json_respond = query_ESG_Lan(id_url[0],id_url[1])
    print(f"{json_respond}\nid: ", id_url[0])