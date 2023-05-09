from typing import Union, Dict, List
import logging
from logging import config
from configparser import ConfigParser

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from const import html2, chat_html
from chat_api import request_chatgpt
from config import settings

app = FastAPI()

# 配置日志
log_dict = settings["logging"]
logging.config.dictConfig(log_dict)
logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
        self.client_conversions: Dict[int, List] = {}

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: int):
        self.active_connections.pop(client_id)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

    async def get_all_connections(self) -> List[int]:
        return list(self.active_connections.keys())

    async def get_connection_by_client_id(self, client_id: int) -> WebSocket:
        return self.active_connections.get(client_id)

    def insert_conversion(self, client_id: int, message: str, is_user: bool = True) -> List[Dict]:
        messages = self.client_conversions.get(client_id)
        if not messages:
            messages = []
        if is_user:
            messages.append({'role': 'user', 'content': message})
        else:
            messages.append({'role': 'assistant', 'content': message})
        if len(messages) >= 10:
            messages = []
        self.client_conversions[client_id] = messages
        return messages


websocket_manager = ConnectionManager()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/ws")
def get_ws_html():
    return HTMLResponse(chat_html)


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.websocket("/test/ws/{client_id}")
async def chatgpt_web(websocket: WebSocket, client_id: int):
    await websocket_manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket_manager.send_personal_message(f"你说: {data}", websocket)
            await websocket_manager.broadcast(f"用户-{client_id}说 : {data}")
    except WebSocketDisconnect:
        websocket_manager.disconnect(client_id)
        await websocket_manager.broadcast(f"用户-{client_id} 离开了该群聊")


@app.websocket("/chat/ws/{client_id}")
async def chatgpt_web(websocket: WebSocket, client_id: int):
    await websocket_manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            messages = websocket_manager.insert_conversion(client_id, data)
            iter_res = request_chatgpt(messages)
            chunk_list = []
            for chunk in iter_res:
                delta = chunk['choices'][0]['delta']
                finish_reason = chunk['choices'][0]['finish_reason']
                chunk_list.append(delta)
                send_msg = delta.get("content") if not finish_reason else finish_reason
                if not send_msg:
                    continue
                await websocket_manager.send_personal_message(send_msg, websocket)
            answer_str = ''.join([m.get('content', '') for m in chunk_list])
            new_messages = websocket_manager.insert_conversion(client_id, answer_str, is_user=False)
            logger.info(f"用户{client_id}当前的对话上下文: {new_messages}")
    except WebSocketDisconnect:
        websocket_manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"请求chatgpt异常: {e}")
