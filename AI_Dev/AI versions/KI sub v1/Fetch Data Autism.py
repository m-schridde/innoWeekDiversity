import requests
import random
import os
import FilterLinks

REPLY_COMMENT_THRESHHOLD = 40
TRAINIG_DATA_PORTION = 0.85
TRAINING_DATA_PATH = os.path.join(os.path.dirname(__file__), "Data","Training","Autism")
TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), "Data","Test","Autism")


links, irrelevant = FilterLinks.get_links(4, "C:\\Users\\I518091\\OneDrive - SAP SE\\Schulungen\\Innoweek\\Threads.xlsx", "Autism")
comments = []
numberOfCommentsPerLink = {}

def checkIfCommentApplicable(comment, link):
    if comment["body"] == "[removed]":

        return False
    if comment["parent_id"].startswith("t3_"):
        
        return True
    else:
        if len(comment["body"].split(" "))>= REPLY_COMMENT_THRESHHOLD:
            return True
        


for link in links:
    numberOfCommentsPerLink[link] = 0
    resp = requests.get("https://api.pushshift.io/reddit/comment/search/?link_id=t3_%s&size=1000&fields=body,parent_id" % link)
    if resp.status_code != 200:
        print("Fehler")
    else:
        data = resp.json()["data"]
        for d in data:
            if checkIfCommentApplicable(d, link):
                comment = d["body"].lower()
                comment = comment.replace("\n"," ")
                comments.append(comment)
                numberOfCommentsPerLink[link] = numberOfCommentsPerLink[link] +1 
print(numberOfCommentsPerLink)
# shuffle comments and store them as .txt files
random.shuffle(comments)
border = round(len(comments)*TRAINIG_DATA_PORTION)
for i in range(border):
    f = open(TRAINING_DATA_PATH + "/Comment %s.txt" % i, "w+", encoding="utf-8")
    f.write(comments[i])
    f.close()
for i in range(border, len(comments)):
    f = open(TEST_DATA_PATH + "/Comment %s.txt" % str(i-border), "w+", encoding="utf-8")
    f.write(comments[i])
    f.close()
print(len(comments)*TRAINIG_DATA_PORTION)
print(len(comments))