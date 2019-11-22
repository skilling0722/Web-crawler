import requests
from bs4 import BeautifulSoup
import re
import time

subject_links = []
comment_list = []

# 게시판에서 게시글들 링크 수집
def post_collector():
    # 페이지 구간 설정
    for page in range(1, 5):
        res = requests.get('http://www.etoland.co.kr/bbs/board.php?bo_table=etoboard01&sca=%C8%B8%BF%F8%B0%D4%BD%C3%C6%C7&page='+str(page))

        soup = BeautifulSoup(res.content, 'html.parser')

        links = soup.find_all("td", class_="mw_basic_list_subject")

        for link in links:
            lists = link.find_all('a')

            subject_link = lists[1]['href']
            p = re.compile('../bbs/.*')
            m = p.match(subject_link)

            if m:
                subject_links.append('http://www.etorrent.co.kr' + m.group()[2:])
            else:
                pass
    time.sleep(0.1)

# 게시글에 접근하여 댓글 수집
def comment_collector():
    for post in subject_links:
        res = requests.get(post)
        soup = BeautifulSoup(res.content, 'html.parser')

        textarea = soup.find_all('textarea')

        for comment in textarea:
            # print(comment.get_text())
            comment_list.append(comment.get_text())
    time.sleep(0.1)

def save():
    with open("C:/Users/Yoo/Desktop/comment.txt", "w", encoding='UTF8') as f:
        for comment in comment_list:
            f.write(comment + '\n\n')

if __name__ == "__main__":
    post_collector()
    comment_collector()
    save()

    print("CLOSE!")

