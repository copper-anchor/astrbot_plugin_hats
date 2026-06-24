from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import At,Image, Plain
import os
import random


@register(
    "astrbot_plugin_hats",
    "Futureppo",
    "今天你想戴什么帽子？",
    "1.0.0",
    "https://github.com/copper-anchor/astrbot-plugin-hats"
)
class Hats(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    @filter.command("戴帽子",alias={"今日帽子","帽子工厂","脑袋凉凉的","hats"})
    async def hats(self, event: AstrMessageEvent):
        '''随机抽选一张高帽图片并发送,同时@发送者'''
        #获取发送者的ID与昵称
        sender_id = event.get_sender_id()
        try:
            sender_name = event.get_sender_name()
        except AttributeError:
            sender_name = str(sender_id)

        hats_folder = os.path.join(os.path.dirname(__file__),"hats")
        if not os.path.exists(hats_folder):
            yield event.plain_result("hats文件不存在,请检查插件目录")
            return
        
        #获取hats文件中的所有图片文件
        image_files = [f for f in os.listdir(hats_folder) if f.lower().endswith(('.png','.jpg','.jpeg','.gif'))]
        if not image_files:
            yield event.plain_result("hats文件夹中没有图片文件,")
            return
        random_image = random.choice(image_files)
        image_path = os.path.join(hats_folder,random_image)
        image_name = os.path.splitext(random_image)[0]

        message_chain = [
            #At(qq=sender_id),
            Plain(f"你今天的帽子是：{image_name}"),
            Image.fromFileSystem(image_path)
        ]

        #发送消息
        yield event.chain_result(message_chain)