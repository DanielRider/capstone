## you will need to add client id information in the script to use it

    ##page to get authentication info: https://www.reddit.com/prefs/apps
    ## medium post explaining the details: https://towardsdatascience.com/scraping-reddit-data-1c0af3040768
    ## Praw docs: https://praw.readthedocs.io/en/stable/tutorials/comments.html
    ## add the detials to the argparser 
## and provide the filepath as an argument to obtain the dataset 


import argparse

import pandas as pd
import numpy as np
from tqdm import tqdm
import praw
import re
import os
import requests

filter_char = lambda c: ord(c) < 256

sub_id_to_population_map = {
    "t5_2rtve": "lupus",
    "t5_2syer" : "gout",
    "t5_2s3g1" : "ibs",
    "t5_2tyg2" : "Psychosis",
    "t5_395ja" : "costochondritis",
    "t5_2saq9" : "POTS",
    "t5_2s23e" : "MultipleSclerosis",
    "t5_2s1h9" : "Epilepsy",
    "t5_2qlaa" : "GERD",
    "t5_2r876" : "CysticFibrosis",
    }

parser = argparse.ArgumentParser(description="Intake Reddit Client ID & Secret, and file path to training/testing data.")

parser.add_argument("--client_id", type=str, help="Reddit Client ID")
parser.add_argument("--client_secret", type=str, help="Reddit Client Secret")
parser.add_argument("--password", type=str, help="Reddit Password")
parser.add_argument("--user_agent", type=str, help="Reddit User Agent")
parser.add_argument("--username", type=str, help="Reddit Username")

parser.add_argument("--file_path", type=str, help="Path to training/testing dataframe")

args = parser.parse_args()

session = requests.Session()
session.verify = r'C:\Users\oicaa4986\AppData\Local\Programs\Python\Python310\lib\site-packages\certifi\cacert.pem'  # Path to cert file !! python -m requests.certs
reddit = praw.Reddit(
    client_id=args.client_id,
    client_secret=args.client_secret,
    password=args.password,
    user_agent=args.user_agent,
    username= args.username,
    requestor_kwargs={'session': session}
)

print ("Logged in as: " + reddit.user.me().name)

df = pd.read_csv(args.file_path, index_col=None)
url_format = "https://www.reddit.com/r/{}/comments/{}/"
posts = []
print ("Extracting posts...")
for _, row in tqdm(df.iterrows(), total=df.shape[0]):
    url = url_format.format(sub_id_to_population_map[row['subreddit_id']], row['post_id'])
    submission = reddit.submission(url=url)
    text = (submission.title.encode('utf-8') + b'\n' + submission.selftext.encode('utf-8')).decode("UTF-8")
    posts.append(text)

df["text"] = posts
df['text'] = df['text'].apply(lambda s: ''.join(filter(filter_char, s)))
df.to_csv(args.file_path.split(".csv")[0] + "_inc_text.csv", index=False)

print ("New dataframe generated: " + args.file_path.split(".csv")[0] + "_inc_text.csv.")