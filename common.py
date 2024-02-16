
from alicebot import Plugin
from alicebot.adapter.mirai.event import NewFriendRequestEvent,BotInvitedJoinGroupRequestEvent,FriendInputStatusChangedEvent
# 抛弃经常产生的对方正在输入中事件，此事件不予处理
class InputChangeDispatcher(Plugin):
    priority:int = 0
    block: bool = True

    async def handle(self) -> None:
        pass

    async def rule(self) -> bool:
        return isinstance(self.event,FriendInputStatusChangedEvent)

# 自动通过新加群申请
class NewRequestHandler(Plugin):
    priority:int = 0
    block: bool = True

    async def handle(self) -> None:
        await self.event.approve("CP Bot Approved")
    async def rule(self) -> bool:
        return isinstance(self.event,NewFriendRequestEvent) or isinstance(self.event,BotInvitedJoinGroupRequestEvent)
