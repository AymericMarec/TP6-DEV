from sys import argv
import requests

def get_content(url):
    return requests.get(url).text

def write_content(content, file):
    path = "/tmp/web_page/"
    Page = open(path,"wb")
    Page.write(content.encode())
    Page.close()

try :
    weblink = argv[1]
except :
    print("Faut donner le lien en argument hein")
    exit(0)


print(weblink)
content = get_content(weblink)
write_content(content,"ynov.html")
print(content)
