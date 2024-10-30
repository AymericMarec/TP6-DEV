from sys import argv
import requests
from datetime import datetime
startTime = datetime.now()


def get_content(url):
    return requests.get(url).text

def write_content(content, file):
    path =""
    Page = open(path+file,"wb")
    Page.write(content.encode())
    Page.close()
    print("fichier : "+file+" a fini d'etre ecrit")

def read_url(file):
    url_file = open(file,"r")
    List_url = url_file.read()
    List_url = List_url.split("\n")
    return List_url

try :
    file = argv[1]
except :
    print("Faut donner le nom du fichier en argument hein")
    exit(0)

List_url = read_url(file)
index = 0
for url in List_url:
    index+=1
    content = get_content(url)
    write_content(content,str(index)+".html")
print(datetime.now() - startTime)