import requests
from src.log import Log
from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, CardItem

log = Log()

class Push():
    """
    msg : 消息内容
    push ： 推送的配置
    """
    def __init__(self,msg,push) -> None:
        self.qmsg_key = push['PushKey']['Qmsg']
        self.Server_key = push['PushKey']['Server']
        self.PushMode = push['PushMode']
        self.EnterpriseId = push['PushKey']['Epwc']['EnterpriseId']
        self.AppId = push['PushKey']['Epwc']['AppId']
        self.AppSecret = push['PushKey']['Epwc']['AppSecret']
        self.UserUid = push['PushKey']['Epwc']['UserUid']
        self.token = push['PushKey']['Dingtalk']['token']
        self.secret = push['PushKey']['Dingtalk']['secret']
        self.msg = msg

    #qmsg酱推送
    def Qmsg(self) -> None:
        if self.qmsg_key == "":
            log.info("没有配置qmsg酱key")
        else:
            try:
                qmsg_url = f'https://qmsg.zendee.cn/send/{self.qmsg_key}'
                data = {'msg': self.msg}
                zz = requests.post(url=qmsg_url,data=data).json()
                if zz['code'] == 0:
                    log.info("qmsg酱"+zz['reason'])
                else:
                    log.info("qmsg酱"+zz['reason'])
            except Exception as e:
                log.error("qmsg酱可能挂了:"+e)

    #Sever酱推送
    def Server(self,title="米游社签到") -> None:
        if self.Server_key == "":
            log.info("没有Server酱cookie")
        else:
            Server_url = f"https://sctapi.ftqq.com/{self.Server_key}.send"
            data = {
                "title":title,
                "desp":self.msg
            }
            zz = requests.post(url=Server_url,data=data).json()
            if zz['code'] == 0:
                log.info("Server推送成功")
            else:
                log.info("Server推送失败"+zz['message'])
    
    # 企业微信推送
    def Epwc(self):
        try:
            if self.AppId != "" and self.AppSecret != "" and self.UserUid != "" and self.EnterpriseId != "":
                def GetToken():
                    url = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.EnterpriseId}&corpsecret={self.AppSecret}&debug=1'
                    response = requests.get(url=url).json()
                    return response['access_token']
                url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={GetToken()}"
                body = {
                    "touser" : self.UserUid,
                    "msgtype" : "text",
                    "agentid" : int(self.AppId),
                    "text" : {"content" : self.msg},
                    "safe":0,
                    "duplicate_check_interval": 1800
                }
                response = requests.post(url=url,json=body).json()
                if response['errcode'] == 0:
                    log.info("企业微信推送成功")
                else:
                    log.info("企业微信推送失败")
            else:
                log.info("企业微信：配置没有填写完整")
        except Exception as e:
            log.info(f"企业微信推送时出现错误,错误码:{e}")
    # Dingtalk推送
    def Dingtalk(self) -> None:
        if self.token == "":
            log.info("没有配置Dingtalk的Token")
        else:
            try:
                webhook = f'https://oapi.dingtalk.com/robot/send?access_token={self.token}'
                data = {'msg': self.msg}
                if self.secret == "":
                    # 方式二：勾选“加签”选项时使用（v1.5以上新功能）
                    xiaoding = DingtalkChatbot(webhook, secret=self.secret)
                else:
                    # 方式一：通常初始化方式
                    xiaoding = DingtalkChatbot(webhook)
                # Text消息@所有人
                zz = xiaoding.send_text(msg=self.msg, is_at_all=False)
                if zz['errcode'] == 0:
                    log.info("钉钉机器人"+zz['errmsg'])
                else:
                    log.info("钉钉机器人"+zz['errmsg'])
            except Exception as e:
                log.error("钉钉机器人可能挂了:"+e)
    def push(self):
        if self.PushMode == "" or self.PushMode == "False":
            log.info("配置了不进行推送")
        elif self.PushMode == "qmsg":
            self.Qmsg()
        elif self.PushMode == "server":
            self.Server()
        elif self.PushMode == "epwc":
            self.Epwc()
        elif self.PushMode == "dingtalk":
            self.Dingtalk()
        else:
            log.info("推送配置错误")
            
