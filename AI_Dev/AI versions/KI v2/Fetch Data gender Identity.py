import requests
import random
import os

REPLY_COMMENT_THRESHHOLD = 10
TRAINIG_DATA_PORTION = 0.85
TRAINING_DATA_PATH = os.path.join(os.path.dirname(__file__), "Data","Training","Gender Intelligence")
TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), "Data","Test","Gender Intelligence")
LOG_DATA_PATH = os.path.join(os.path.dirname(__file__), "Log","Gender Intelligence")

links = ["gdrrhd", "bn764h", "80g0oe", "2f73tk", "5enoq0", "27wkkb", "el0jyh",
"6v8qhn", "9v8fke", "871hfo", "55203p", "9i5iny",
"91i57k", "dadwpc", "8sq5uz", "b38asl", "2h3nny", "42e3ha"
"8sq0tg", "7w5oi3", "5j2e70", "7ypng0", "f3aj6r",
 "95jn3c", "8tfj01", "eolm15", "6jepz7",
"8lvq1o", "em6tlz", "e2dkja", "dadwpc", "ep44vd",
"d5sdla", "cppn6x", "6fjvcd", "cl90eh", "922wi4", "60v7y6"]
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
                comment = comment.replace("'", "")
                comments.append(comment)
                numberOfCommentsPerLink[link] = numberOfCommentsPerLink[link] +1 
print(numberOfCommentsPerLink)
#shuffle comments and store them as .txt files
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