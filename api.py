import datetime
import requests
import json
from config import CLIST_AUTH
class WebRequestHandler:
    def __init__(self):
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

class Clist(WebRequestHandler):

    def __init__(self):
        super().__init__()
        self.baseUrl = "https://clist.by/api/v4/"
        self.headers["Authorization"]=CLIST_AUTH

    def getUpcomingContestData(self,website):
        response = requests.get(self.baseUrl+"contest/?upcoming=true&format_time=true&host="+website+"&order_by=end",headers=self.headers)
        data = json.loads(response.text)['objects']
        return data
    
    def generateUpcomingContestMsg(self,website,all):
        msg = "通过clist.by API查询到以下比赛：\n"
        todayCnt = 0
        today = datetime.datetime.now().date()
        for contest in self.getUpcomingContestData(website):
            date = datetime.datetime.strptime(contest['start'], "%d.%m %a %H:%M")
            if not all and date != today:
                continue
            msg += contest['event']+"将在"+date.strftime("%m月%d日 %H:%M")+"开始，链接为"+contest['href']+"\n"
            if date == today:
                todayCnt += 1
        if not all:
            msg += "今日没有来自"+website+"的比赛" if todayCnt == 0 else "今天有"+todayCnt+"场来自"+website+"的比赛" 
        return msg

class Codeforces(WebRequestHandler):

    def __init__(self):
        super().__init__()
        self.baseUrl = "https://codeforces.com/api/"
    
    def getUserStatus(handle):
        response = requests.get(self.baseUrl+"user.info?handles="+handle,headers=self.headers)