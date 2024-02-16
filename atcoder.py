from alicebot import Plugin
from api import Clist

clist = Clist()

class AtcoderHandler(Plugin):
    priority:int = 1
    block: bool = False
    
    async def handle(self) -> None:
        params = str(self.event.message).lower().split(" ",1)
        if len(params) == 1:
            await self.help()
            return
        params = params[1].split(" ")
        if params[0] == "contests" or params[0] == "比赛信息":
            await self.event.reply(clist.generateUpcomingContestMsg("atcoder.jp",True))

    async def help(self):
        msg = "[帮助信息]\n" +"/atc [contests/比赛信息] : 查询即将到来的比赛,数据源clist.by"
        await self.event.reply(msg)

    async def rule(self) -> bool:
        return (
            str(self.event.message).lower().startswith("/atcoder")
            or str(self.event.message).lower().startswith("/atc")
        )