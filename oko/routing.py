# from django.urls import path

# from oko import consumers

# websocket_urlpatterns = [
#     path('', consumers.ChatConsumer.as_asgi()),
#     # path('<str:room_name>/',consumers.ChatConsumer.as_asgi(), name='room'),

# ]

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from oko import consumers

# URLs that handle the WebSocket connection are placed here.
websocket_urlpatterns=[
                    re_path("", consumers.ChatRoomConsumer.as_asgi(),),
                    re_path("/admindashboard/chat_list", consumers.ChatRoomConsumer.as_asgi(),),
                ]                        


application = ProtocolTypeRouter( 
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
               websocket_urlpatterns
            )
        ),
    }
)