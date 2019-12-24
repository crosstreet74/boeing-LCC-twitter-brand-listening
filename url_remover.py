import re
import csv
  
def findNSub(string): 
    # findall() has been used  
    # with valid conditions for urls in string 
    result = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', string) 
    return result

lists = []
file = open("sample.csv", "r", encoding="utf-8")
while True:
    line = file.readline().rstrip("\n")
    line = findNSub(line)
    if line:
        lines = line.split("`")
        lists.append(lines)
    else:
        break

with open("crawled_data.csv", "w", newline="", encoding='utf8') as f:
    writer = csv.writer(f)
    writer.writerows(lists)