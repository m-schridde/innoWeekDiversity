import requests
import random
import os

REPLY_COMMENT_THRESHHOLD = 10
TRAINIG_DATA_PORTION = 0.85
TRAINING_DATA_PATH = os.path.join(os.path.dirname(__file__), "Data","Training","Culture Identity")
TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), "Data","Test","Culture Identity")


links = ["7yarkw", "gdoc5m", "6tw3ej", "7pgy9o", "7r5nnw", "1epqg5", "6tbw5h", "59baza", 
 "76nk8i","8042i7", "5cqo7h", "8u1gxn", "73fspe",
 "76d97c", "4ri151",
 "76v2mm", "9ua2zp", "9ecpew",
"b0vu18", "54zkvi", "bt9ls2", "6yj3iv",
"84a8vh", "fzm78m", "faqd2h", "6bmazx",
"6uuhak", "82ubm0", "5mnt6x", "b0rfwe",
"4k2t8s", "8iyekv", "dgs2em", "bqffg7", "51nfxq", "b46708"]
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