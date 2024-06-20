import asyncio, nats, os, json, shutil

from dotenv import load_dotenv


load_dotenv()

nast_server_local = os.getenv("NATS_SERVER_LOCAL")
input_ui_directory = os.getenv("SOURCE_INPUT_UI_DIRECTORY")
destination_folder = os.getenv("DESTINATION_INPUT_UI_DIRECTORY")


async def upload_img():
    try:
        source_file = os.path.join(input_ui_directory, "img.jpg")
        destination_folder = destination_folder
        os.makedirs(destination_folder, exist_ok=True)
        destination_path = os.path.join(
            destination_folder, os.path.basename(source_file)
        )
        shutil.copy(source_file, destination_path)
    except Exception as e:
        print(e)


async def main():

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print(
            "Received a message on '{subject} {reply}': {data}".format(
                subject=subject, reply=reply, data=data
            )
        )

    pub_topic = "topic.from.ui"
    sub_topic = "topic.to.ui"
    raw = {
        "file_path": "/input/ui/img.jpg",
        "mean_rgb": "",
        "color_name": "",
        "is_ui_request": True,
    }

    json_msg = json.dumps(raw)

    try:
        client = await nats.connect(nast_server_local)
        print("connected to the Nats server")

        await client.subscribe(sub_topic, cb=message_handler)
        await upload_img()
        await client.publish(pub_topic, json_msg.encode())
        while True:
            await asyncio.sleep(1)

    except asyncio.CancelledError:
        pass

    except Exception as e:
        print(f"Error in main loop: {e}")

    finally:
        print("disconnecting...")
        await client.drain()
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
