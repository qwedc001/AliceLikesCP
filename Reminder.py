from alicebot import Plugin
from time import strftime, localtime
from alicebot.adapter.apscheduler import scheduler_decorator
from alicebot.adapter.mirai.event import GroupMessage,FriendMessage
import datetime
import json

configPath = "accounts.json"
class DailySubscribeRequestHandler(Plugin):
    priority:int = 1
    block: bool = False
    
    async def handle(self) -> None:
        params = str(self.event.message).lower().split(" ",1)
        if len(params) == 1:
            return
        params = params[1].split(" ")
        if params[0] == "subscribe" or params[0] == "订阅":
            jsonCfg = {}
            with open(configPath,mode='r') as cfg:
                jsonCfg = json.loads(cfg.read())
                cfg.close()
            with open(configPath,mode='w') as cfg:
                if isinstance(self.event,GroupMessage):
                    if self.event.sender.permission != "MEMBER":
                        jsonCfg["boardcast"]["group"].append(self.event.sender.group.id)
                    else:
                        await self.event.reply("尝试订阅失败，需要管理员或者群主进行订阅操作才可订阅。")
                elif isinstance(self.event,FriendMessage):
                    jsonCfg["boardcast"]["friend"].append(self.event.sender.id)
                cfg.write(json.dumps(jsonCfg))
                cfg.close()
            await self.event.reply("订阅成功")
                
        elif params[0] == "cancel" or params[0] == "取消":
            with open(configPath,mode='r') as cfg:
                jsonCfg = json.loads(cfg.read())
                cfg.close()
            with open(configPath,mode='w') as cfg:
                if isinstance(self.event,GroupMessage):
                    if self.event.sender.group.id in jsonCfg["boardcast"]["group"]:
                        jsonCfg["boardcast"]["group"].remove(self.event.sender.group.id)
                    else:
                        await self.event.reply("未找到订阅")
                elif isinstance(self.event,FriendMessage):
                    if self.event.sender.id in jsonCfg["boardcast"]["friend"]:
                        jsonCfg["boardcast"]["friend"].remove(self.event.sender.id)
                    else:
                        await self.event.reply("未找到订阅")
                cfg.write(json.dumps(jsonCfg))
                cfg.close()
            await self.event.reply("解除订阅成功")

    async def rule(self) -> bool:
        return (
            str(self.event.message).lower().startswith("/daily")
            or str(self.event.message).lower().startswith("/d")
        )

@scheduler_decorator(
    trigger="cron", trigger_args={"hour": 12}, override_rule=True
)
class DailySubscribeSender(Plugin):
    priority:int = 0
    block:bool = True


    async def handle(self) -> None:
        group = []
        friend = []
        cfUpcoming = generateUpcomingContestMsg("codeforces.com",False)
        atcUpcoming = generateUpcomingContestMsg("atcoder.jp",False)
        with open(configPath,mode='r') as cfg:
            data = json.loads(cfg.read())
            group = data["boardcast"]["group"]
            friend = data["boardcast"]["friend"]
            cfg.close()
        for g in group:
            await self.bot.get_adapter("mirai").send(
                cfUpcoming,
                message_type="group",
                target=g,  # 群号
            )
            
            await self.bot.get_adapter("mirai").send(
                atcUpcoming,
                message_type="group",
                target=g,  # 群号
            )
        for f in friend:
            await self.bot.get_adapter("mirai").send(
                cfUpcoming,
                message_type="friend",
                target=f,  # 群号
            )
            
            await self.bot.get_adapter("mirai").send(
                atcUpcoming,
                message_type="friend",
                target=f,  # 群号
            )

    async def rule(self) -> bool:
        return False
