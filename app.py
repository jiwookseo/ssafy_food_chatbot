from flask import Flask, render_template, request
import csv, json
import requests
import os
from tele_config import *
from food import *
# from cur import * 보안 & 크롤링 불가
from pprint import pprint as pp

app=Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")

#webhook
#setwebhook > 웹훅 설정 > 텔레그램에게 알림 설정
# 텔레그램이 우리에게 알림을 줄 대 사용할 루트
# 만약 특정 유저가 우리 봇으로 메세지를 보내게 되면
# 텔레그램이 우리에게 json으로 알림을 보내온다.

@app.route('/setwebhook')
def setwebhook():
    getTelegram('setWebhook?url={}/{}'.format(my_url,tele_key))
    return render_template("setWebhook.html"), 200
    
@app.route('/deletewebhook')
def delete_webhook():
    getTelegram('deleteWebhook?url={}/{}'.format(my_url,tele_key))
    return render_template("deleteWebhook.html"), 200
    
@app.route("/{}".format(tele_key), methods=['POST'])
def telegram():
    doc = request.get_json()
    chatName, chatId, chatMsg = getData(doc)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if chatMsg[-2:] == "식단" or chatMsg[-2:] == "ㅅㄷ":
        foodMsg(chatName, chatId, chatMsg[0:2])
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    elif chatMsg == "알림해제" or chatMsg == "알림 해제" or chatMsg == "알림취소" or chatMsg == "알림 취소" or chatMsg == "취소" or chatMsg == "구독 취소" or chatMsg == "구독취소":
        with open('except.csv', 'r') as f:
            except_id = csv.reader(f)
            except_list=np.array([])
            for row in except_id:
                except_list=np.append(except_list,row,axis=0)
        except_list=np.append(except_list,chatId)
        with open('except.csv', 'w') as f:
            a=csv.writer(f)
            a.writerow(except_list)
        getTelegram(sendParams(chatId,"{} 님 구독 취소되었습니다.".format(chatName)))

    elif chatMsg == "알림설정" or chatMsg == "알림 설정" or chatMsg == "구독" or chatMsg == "구독 설정" or chatMsg == "구독설정":
        with open('except.csv', 'r') as f:
            except_id = csv.reader(f)
            except_list=np.array([])
            for row in except_id:
                except_list=np.append(except_list,row,axis=0)
        except_list=list(except_list)
        if str(chatId) in except_list:
            except_list.remove(str(chatId))
        with open('except.csv', 'w') as f:
            a=csv.writer(f)
            a.writerow(except_list)
        getTelegram(sendParams(chatId,"{} 님 구독 설정되었습니다.".format(chatName)))
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    elif chatMsg == "문의" or chatMsg == "문의 사항"or chatMsg == "문의사항":
        msg=""
        msg+="'[문의]' 태그를 붙이고 궁금하신 점을 말씀해주시면 빠른 시일 내에 답변해드립니다."
        getTelegram(sendParams(chatId,msg))
        
    elif chatMsg == "요청" or chatMsg == "요청사항" or chatMsg == "요청 사항":
        msg=""
        msg+="'[요청]' 태그를 붙이고 궁금하신 점을 말씀해주시면 향후 업데이트에 반영해드립니다."
        getTelegram(sendParams(chatId,msg))
    
    elif chatMsg[:4]=="[문의]":
        getTelegram(sendParams(chatId,"{}님 감사합니다.\n빠른 시일 내에 답변해드리겠습니다.".format(chatName)))
        getTelegram(sendParams(tele_myid,chatMsg+str(chatId)+chatName))
        
    elif chatMsg[:4]=="[요청]":
        getTelegram(sendParams(chatId,"{}님 좋은 의견 감사합니다.\n향후 업데이트에 참고토록 하겠습니다.".format(chatName)))
        getTelegram(sendParams(tele_myid,chatMsg+str(chatId)+chatName))
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # elif chatMsg == "커리큘럼" or chatMsg == "수업" or chatMsg == "커리" or chatMsg == "수업 일정" or chatMsg == "수업일정" or chatMsg == "일정" or chatMsg == "ㅋㄹㅋㄹ":
    #     curMsg(chatName, chatId)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    elif chatMsg=="명령어" or chatMsg=="command":
        msg="명령어 > 사용 가능한 명령어 :\n"
        msg+="식단 > 어제, 오늘, 내일, 모레 식단 출력 기능\n"
        msg+="구독 취소 > 매일 아침, 식단 정기알림 구독을 취소합니다.\n"
        msg+="구독 설정 > 매일 아침, 식단 정기알림 구독을 신청합니다.(default)\n"
        # msg+="커리큘럼 or 수업일정 > 이번 주 커리큘럼 출력 기능\n"
        msg+="문의, 요청 사항 > 궁금하신 점이나, 필요한 기능이 있으면 알려주세요.\n"
        getTelegram(sendParams(chatId,msg))
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    elif chatMsg[:3]=="msg" and str(chatId)==str(tele_myid):
        admin=chatMsg.split(",")
        getTelegram(sendParams(admin[1],admin[2]))
        getTelegram(sendParams(tele_myid,"{}님께 {} 메세지 보내기 완료".format(admin[1],admin[2])))
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    else:
        msg="잘못된 명령어입니다.\n\n"
        msg+="명령어 > 사용 가능한 명령어 :\n"
        msg+="식단 > 어제, 오늘, 내일, 모레 식단 출력 기능\n"
        msg+="구독 취소 > 매일 아침, 식단 정기알림 구독을 취소합니다.\n"
        msg+="구독 설정 > 매일 아침, 식단 정기알림 구독을 신청합니다.(default)\n"
        # msg+="커리큘럼 or 수업일정 > 이번 주 커리큘럼 출력 기능\n"
        msg+="문의, 요청 사항 > 궁금하신 점이나, 필요한 기능이 있으면 알려주세요.\n"
        getTelegram(sendParams(chatId,"{} 님 죄송합니다. {}".format(chatName,msg)))
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data[chatId]=chatName
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data,f)
    return '', 200

@app.route('/sendFoodmsg')
def sendFoodmsg():
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    id_set=set(data.keys())
    with open('except.csv', 'r') as f:
        except_id = csv.reader(f)
        except_list=np.array([])
        for row in except_id:
            except_list=np.append(except_list,row,axis=0)
        except_set=set(except_list)
    msg_id=id_set-except_set
    for chatId in msg_id:
        foodMsg(data[chatId],chatId)
    return render_template("sendFoodmsg.html"), 200