import requests
url = open("./url.txt","r").readline()
url = url.strip()
print(url)
#url = "https://cdn.dq1503.bid/bg.jpg"
response = requests.get(url)
img = response.content
print(response)
with open("./test.jpg","wb") as f:
    f.write(img)
