# from django.urls import path

# from oko import consumers

# websocket_urlpatterns = [
#     path('', consumers.ChatConsumer.as_asgi()),
#     # path('<str:room_name>/',consumers.ChatConsumer.as_asgi(), name='room'),

# ]

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path, path
from oko import consumers

# URLs that handle the WebSocket connection are placed here.
websocket_urlpatterns=[
                    re_path("", consumers.ChatRoomConsumer.as_asgi(),),
                    path("ws://127.0.0.1:6379/", consumers.ChatRoomConsumer.as_asgi(),),
<<<<<<< Updated upstream
                    path("ws://192.168.0.1:6379/", consumers.ChatRoomConsumer.as_asgi(),),
                    path("ws://reklama-oko.ru:6379/", consumers.ChatRoomConsumer.as_asgi(),),
=======
>>>>>>> Stashed changes
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