from alicebot import Plugin
from api import Clist

clist = Clist()

class CodeforcesHandler(Plugin):
    priority:int = 1
    block: bool = False
    
    async def handle(self) -> None:
        params = str(self.event.message).lower().split(" ",1)
        if len(params) == 1:
            await self.help()
            return
        params = params[1].split(" ")
        if params[0] == "contests" or params[0] == "比赛信息":
            await self.event.reply(clist.generateUpcomingContestMsg("codeforces.com",True))
        if params[0] == "profile" or params[0] == "个人资料":
            try:
                handle,operation = params[1],params[2]

            except Exception as e:
                await self.event.reply("/cf profile [handle] [operation] 缺少参数")

    async def help(self):
        msg = "[帮助信息]\n" +"/cf [contests/比赛信息] : 查询即将到来的比赛,数据源clist.by"
        await self.event.reply(msg)

    async def rule(self) -> bool:
        return (
            str(self.event.message).lower().startswith("/codeforces")
            or str(self.event.message).lower().startswith("/cf")
        )