import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from AppOko.models import Message, CustomUser, ChatRoom
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from datetime import datetime
import locale



RU_MONTH_VALUES = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апреля': 4,
    'мая': 5,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 11,
    'декабря': 12,
}


def int_value_from_ru_month(date_str):
    for k, v in RU_MONTH_VALUES.items():
        date_str = date_str.replace(k, str(v))

    return date_str




class ChatRoomConsumer(AsyncWebsocketConsumer):
    print("класс запустился")
    
    async def connect (self):
        self.group_name = 'my_socket'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        x = self.channel_name
        print(x)
        return x

        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        print(body)
        room_id = text_data_json['room_id']
        print(room_id)
        user_id = text_data_json['user_id']
        print(user_id)
        # room_id2 = await sync_to_async(ChatRoom.objects.get)(id=room_id)
        # print(room_id2)
        # user_id2 = await sync_to_async(CustomUser.objects.get)(id=user_id)
        # print(user_id2)
        await self.save_message(user_id, room_id, body)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type":"chatbox_message",
                "room_id": room_id,
                "user_id": user_id,
                "body": body,    
            },
        )

    async def chatbox_message(self,event):
        print(self.channel_layer)
        print(self.channel_name)
        print('чатбокс открылся')
        user_id = event["user_id"]
        room_id = event["room_id"]
        body = event["body"]
        # room_id2 = await sync_to_async(ChatRoom.objects.get)(id=room_id)
        user_id = str(user_id)
        room_id = str(room_id)
        print(user_id)
        user_id2 = await sync_to_async(CustomUser.objects.get)(id=user_id)
        print('сейчас возьмем логин')
        user_id3 = user_id2.username
        print('сейчас создастся сообщение')
        user_type = user_id2.user_type
        
        # await self.save_message(user_id2, room_id2, body)
        
        message = await sync_to_async(Message.objects.last)()
        
        message_text_created = message.created
        message_text_updated = message.updated
        date_str = '05 марта 2015, 13:00'
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8') 
        date_str = int_value_from_ru_month(date_str)
        message_text_created = str(message_text_created).split('.')[0]
        message_text_created = str(message.created.strftime('%d %B %Y г. %H:%M'))
        message_text_updated = message_text_updated.strptime(date_str, '%d %m %Y, %H:%M')
        message_text_updated = str(message_text_updated.strftime('%d %B %Y, %H:%M'))
        
        await self.send(
            text_data=json.dumps(
            {
                "user_id": user_id3,
                "body": body,
                "room_id": room_id,
                "created": message_text_created,
                "updated": message_text_updated,
                "user_type": user_type
            }
            )
        )
        

    @database_sync_to_async
    def save_message(self, user, room, body):
        print('создание сообщения в функции')
        room_id2 = ChatRoom.objects.get(id=room)
        user_id2 = CustomUser.objects.get(id=user)

        Message.objects.create(user=user_id2, room=room_id2, body=body) 
        print('сообщение создалось')