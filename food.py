import requests
from bs4 import BeautifulSoup as bs
import numpy as np
import datetime
from tele_config import *
from pprint import pprint as pp
SSAFY_ID=os.getenv("SSAFY_ID")
SSAFY_PWD=os.getenv("SSAFY_PWD")
LOGIN_DATA={'userId': SSAFY_ID,'userPwd': SSAFY_PWD}
LOGIN_URL = 'https://edu.ssafy.com/comm/login/SecurityLoginCheck.do'
s = requests.Session()
res = s.post(LOGIN_URL, data=LOGIN_DATA, verify=False, allow_redirects=False)
# print(res.raise_for_status())

url = 'https://edu.ssafy.com/edu/board/notice/list.do#;'
res = s.get(url).text
doc = bs(res, 'html.parser')
result=doc.find_all("a")
food_contents=[]
for i in result:
    if i.text[:9]=="[기타] [중식]":
        food_contents.append(i.get("onclick")[-6:-3])
notice_url = 'https://edu.ssafy.com/edu/board/notice/detail.do?brdItmSeq={}'.format(food_contents[0])
# pp(notice_url)
res = s.get(notice_url).text
doc = bs(res, 'html.parser')
result=doc.find_all("table")
foodlist=result[0]
trs = foodlist.find_all('tr')
#data scraping
#--------------------------------------------------------------------------------------------------------
indent=trs[0].text.index('층')-1 # 매주 바뀌는 듯.. 야매로 찾을 수 있도록
#--------------------------------------------------------------------------------------------------------
check=0
for i,value in enumerate(trs):
    if value.text[:6]=="\n"+" "*indent+"구분":
        check=i
        break
days=trs[check].text
days=days.split("\n")
days=days[2:-1]
days_array=np.array(days)
for i in range(5):
    days_array[i]=days_array[i][indent:-1]
#날짜데이터 가져오기

check=0
for i,value in enumerate(trs):
    if value.text[1+indent:6+indent]=='멀티스퀘어':  # 매주 바뀌는 듯....
        check=i
        break
menu=[]
# pp(check)
for i in range(check,check+16):
    menu.append(trs[i].text.split("\n")[1:-1])
menu[0]=menu[0][3:]
menu[8]=menu[8][1:]
# pp(menu)
menu_array=np.array([])
for i in range(16):
    menu_array=np.append(menu_array,np.array(menu[i]))
menu_array=menu_array.reshape((16,5)).T
menu_array=menu_array.reshape((5,2,8))
menu_dict={}
for i in range(5):
    menu_dict[i]=menu_array[i].reshape((2,8))

def foodMsg(chat_name, chat_id, day="오늘"):
    dt = datetime.datetime.now(datetime.timezone.utc)
    tz = datetime.timezone(datetime.timedelta(hours=7))
    dt = dt.astimezone(tz)
    #timezone을 설정하여 한국 시간대에 맞출 수 있도록
    wd=dt.weekday()
    # print(dt)
    check=True
    if day=="내일":
        wd+=1
    elif day=="어제":
        wd-=1
    elif day=="모레":
        wd+=2
        
    if wd>=5 or wd<0:
        getTelegram(sendParams(chat_id,"주중의 식단만 확인 가능합니다."))
        check=False
        
    if check:
        message=""
        if chat_name!=None:
            message+="{}님 안녕하세요 \n\n".format(chat_name)
        if menu_dict[wd][0][-1][indent:]=="\u3000":
            message+="{}은 즐거운 휴일입니다.\n푹 쉬세요 :)\n".format(days_array[wd])
        else:
            message+="{}의 A형 식단은\n".format(days_array[wd])
            for i in range(7):
                message+=menu_dict[wd][0][i][indent:]+"\n"
            message+="총 칼로리는 {}입니다.\n\n".format(menu_dict[wd][0][-1][indent:].replace(u'\xa0', u' '))
            message+="{}의 B형 식단은\n".format(days_array[wd])
            for i in range(7):
                message+=menu_dict[wd][1][i][indent:]+"\n"
            message+="총 칼로리는 {}입니다.\n\n".format(menu_dict[wd][1][-1][indent:].replace(u'\xa0', u' '))
        message+="인싸봇 올림. 좋은 하루 되세요 :)"
        getTelegram(sendParams(chat_id,message))