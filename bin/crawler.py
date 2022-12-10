from urllib.parse import urlparse, urlencode, quote, unquote
import pickle
import re
import time
import requests
import hashlib
import base64
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
from konlpy.tag import Okt
from konlpy.tag import Kkma
from fake_useragent import UserAgent
import threading
# start url
CUR_DEPTH = 0
CUR_COUNT = 0
MAX_DEPTH = 2
MAX_COUNT = 3
SLEEP = 2  # sec
docList = set()
okt = Okt()
kkma = Kkma()
ua = UserAgent()
DATADIR = "DATA"
SEPARATOR = "/"
def relativeToAbsolute():
	pass

def readText(fileName,ttype):
	print(f'{fileName}.{ttype}')
	with open(DATADIR+SEPARATOR+fileName+"."+ttype, 'rb') as f:
		data = pickle.load(f)
		print(data)

def writeText(url, textChunk,ttype):
	# print(f"{url}")
	hashedurl = quote(url, safe='')
	# print(f"{hashedurl}")
	with open(DATADIR+SEPARATOR+hashedurl+"."+ttype,"wb") as f:
		pickle.dump(textChunk,f)

	readText(hashedurl, ttype)

def crawlDocs(url):
	try:
		header = {'User-Agent':str(ua.chrome)}
		page = requests.get(url, headers=header)
		origin = urlparse(url)
		originalDomain = origin.scheme + "://" + origin.netloc
		if page.status_code == 200:
			extractDocs(page)
			# textChunk = extractDocs(page)
			# writeText(url, textChunk)
			links = extractUrls(url, page)
		else:
			# print(f"page.status_code {page.status_code}")
			pass
	except Exception as err:
		print(f"{err=}")
		pass

def getDocs(url,depth, count):
	#docList = set()
	# print(f'count : {count}, depth: {depth}, p:{url}')
	if count > 0 :
		time.sleep(SLEEP)
		try:
			header = {'User-Agent':str(ua.chrome)}
			page = requests.get(url, headers=header)
			origin = urlparse(url)
			originalDomain = origin.scheme+"://"+origin.netloc
			if depth < 0:
				return
			if page.status_code == 200:
				extractDocs(url, page)
				links = extractUrls(url, page)
				for link in links:
					m = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$\-@\.&+:/?=]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', link)
					if m == []:
						link = originalDomain+link
					if link not in docList:
						docList.add(link)
						# getDocs(link,depth, count)
						t = threading.Thread(target=getDocs, args=(link, depth-1, count-1))
						t.start()
						# print(f'p: {url}, c: {link}')
						# print(docList)
			else:
				# print(page.status_code)
				pass
		except :
			pass
	else:
		#print("STOP CRWALING")
		return 0
# extract Urls from docs
def extractUrls(url, pageChunk):
	retList = set()
	origin = urlparse(url)
	originalDomain = origin.scheme + "://" + origin.netloc

	encoding = EncodingDetector.find_declared_encoding(pageChunk.content, is_html=True)
	soup_data = BeautifulSoup(pageChunk.content, "lxml", from_encoding=encoding)

	for link in soup_data.find_all('a', href=True):
		retList.add(link['href'])

	return retList


# extract doccs 
def extractDocs(url, pageChunk):
	#print("extract Docs")
	text = BeautifulSoup(pageChunk.content, 'html.parser').get_text()
	writeText(url, okt.pos(text,norm=True, stem=True), "pos")
	writeText(url, okt.phrases(text), "phrase")
	#print(okt.nouns(text))
	#print(okt.phrases(text))

# retreive docs from url


#if __name__ == "__main__":
#	#crawlDocs("https://www.dogdrip.net")
#	getDocs("https://www.dogdrip.net",MAX_DEPTH, MAX_COUNT)

#getDocs("https://www.reuters.com/",MAX_DEPTH, MAX_COUNT)
#getDocs("https://www.naver.com/",MAX_DEPTH, MAX_COUNT)
#getDocs("https://www.issuelink.co.kr/community/listview/all/3/adj/_self/blank/blank/blank",MAX_DEPTH, MAX_COUNT)
#getDocs("https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=+%EB%8C%80%ED%86%B5%EB%A0%B9", MAX_DEPTH, MAX_COUNT)