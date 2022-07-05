#Import necessary libraries
from facebook_scraper import get_posts
from fastapi import FastAPI
import pandas as pd
import json
import sqlite3 



app= FastAPI()
@app.get("/")
def read_root():

# Initialize dataframe to scrape Facebook page post
    post_df_full = pd.DataFrame(columns = [])

# Start to collect Facebook post data by facebook_scraper library
    for post in get_posts('supcom.universite.carthage', extra_info=True, pages=2):
        post_entry = post
        fb_post_df = pd.DataFrame.from_dict(post_entry, orient='index')
        fb_post_df = fb_post_df.transpose()
        post_df_full = post_df_full.append(fb_post_df)

# Check dataframe information
    post_df_full.info()

# Delete empty Columns
    post_df_full.dropna(how='all', axis=1, inplace=True)
    post_df_full.drop(["timestamp","time"], axis=1, inplace=True)
    post_df_full = post_df_full.iloc[: , 1:]
    
    


# Save dataframe into excel file
    post_df_full.to_excel('fb_scrapped_data.xlsx')

    
# Convert DataFrame to JSON
    json = post_df_full.to_json(orient="split")


    df1=pd.read_excel('fb_scrapped_data.xlsx')

# Create a connection to the SQLite database
    conn = sqlite3.connect('test_db.sqlite')
    df1.to_sql('scrapped_data', conn, if_exists='replace', index=False)
    conn.close()

#Read SQLite table as a Pandas DataFrame
    conn = sqlite3.connect('test_db.sqlite')
    df1 = pd.read_sql_query('SELECT * FROM scrapped_data', conn)
    conn.close()
    print(df1)
    
    return json