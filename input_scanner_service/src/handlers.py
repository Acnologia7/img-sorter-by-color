import json
from nats.aio.client import Client
from nats.aio.msg import Msg

try:
    from .utils import (
        is_verified,
        publish_message,
        build_json_message,
    )
except ImportError:
    from utils import (
        is_verified,
        publish_message,
        build_json_message,
    )


class BaseHandler:
    def __init__(self, client: Client, pub_topic: str):
        self.client = client
        self.pub_topic = pub_topic

    async def message_handler(self, msg: Msg) -> None:
        try:
            subject = msg.subject
            data = msg.data.decode()
            content = json.loads(data)
            print(f"Received a message on '{subject}': {content}")
            await self.process_message(content)
        except Exception as e:
            print(f"Error in message handling: {e}")

    async def publish_message(self, message: str) -> None:
        await publish_message(message, self.client, self.pub_topic)

    async def process_message(self, data: dict) -> None:
        raise NotImplementedError("Subclasses must implement process_message method")


class UIWorkflowHandler(BaseHandler):
    def __init__(self, client: Client, pub_topic: str):
        super().__init__(client, pub_topic)

    async def process_message(self, data) -> None:
        file_path = data.get("file_path", "")
        is_ui_request = data.get("is_ui_request", False)

        try:
            if await is_verified(file_path):
                json_message = build_json_message(
                    file_path=file_path, is_ui_request=is_ui_request
                )
                await self.publish_message(json_message)
        except Exception as e:
            print(f"Error in UIWorkflowHandler: {e}")
