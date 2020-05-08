import requests
import random
import os

REPLY_COMMENT_THRESHHOLD = 21
TRAINIG_DATA_PORTION = 0.85
TRAINING_DATA_PATH = os.path.join(os.path.dirname(__file__), "Data","Training","Differently Abled")
TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), "Data","Test","Differently Abled")


links = ["8o41m0", "bwucw5", "8mlniq", "b590k8", "9shhk3", "780094", "8rl6ud","5v3r0e", 
"8mptfi", "9xokko", "b3iy69", "9ml01l", "a4nwoh", "9r5unz", "aq5e4f", "8fn8mb", "dc7jrm", "cb986e", "73ob43",
 "8r3kn9", "exbcj3", "bgo4kr", "bx0g13",
 "bgg8w8", "9lkow3"]
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
theSum = 0
for i in numberOfCommentsPerLink:
    theSum += numberOfCommentsPerLink[i]
print(theSum)

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