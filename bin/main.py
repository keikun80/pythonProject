import crawler

MAX_DEPTH=1
MAX_COUNT=2
if __name__ == "__main__":
     URL = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100"
     crawler.getDocs(URL, MAX_DEPTH, MAX_COUNT)
     # crawler.crawlDocs("https://www.dogdrip.net")

