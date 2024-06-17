import json, shutil, os

from dotenv import load_dotenv
from nats.aio.client import Client
from nats.aio.msg import Msg
from utils import is_verified, publish_message, build_json_message

load_dotenv()

output_base_directory = os.getenv("OUTPUT_BASE_DIRECTORY")


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

    async def publish_message(self, message: str, pub_topic: str = None) -> None:
        pub_topic = pub_topic or self.pub_topic
        await publish_message(message, self.client, pub_topic)

    async def process_message(self, data: str) -> None:
        raise NotImplementedError("Subclasses must implement process_message method")


class SortWorkflowHandler(BaseHandler):
    def __init__(self, client: Client, pub_topic: str):
        super().__init__(client, pub_topic)

    async def process_message(self, data: dict) -> None:
        source_path = data["file_path"]
        mean_rgb = data["mean_rgb"]
        color_name = data["color_name"]
        is_ui_request = data["is_ui_request"]

        try:
            if await is_verified(source_path):

                img_name = os.path.basename(source_path)

                destination_path = os.path.join(
                    output_base_directory, color_name, img_name
                )
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                shutil.copy(source_path, destination_path)
                print(f"Image {img_name} successfuly sorted in {destination_path}")
                os.remove(source_path)
                print(f"Image {img_name} successfuly removed from in {source_path}")
                json_message = build_json_message(
                    file_path=destination_path,
                    mean_rgb=mean_rgb,
                    color_name=color_name,
                    is_ui_request=is_ui_request,
                )
                # this could be an another handler
                if is_ui_request:
                    print("Publishing msg to UI...")
                    await self.publish_message(json_message)
        except Exception as e:
            print(f"Error in SortWorkflowHandler: {e}")
