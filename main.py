import openai
import discord
from json import load


config = load(open("config.json"))
openai.api_key = config["api_key"]


class Oxerator:
    def __init__(self):
        self.client = discord.Client()
        self.on_ready = self.client.event(self.on_ready)
        self.on_message = self.client.event(self.on_message)

    async def on_ready(self):
        print(f"Logged on as {self.client.user}")

    async def on_message(self, m: discord.Message):
        if m.author.id in config["access"] and "search" in m.content:
            try:
                content = str(m.content).split("search")[-1]
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "user",
                            "content": content
                            + str("answer not more than 2000 characters"),
                        }
                    ],
                )
                result = response.choices[0].message["content"]
                if "As an AI language model," in str(result):
                    str(result).replace("As an AI language model,", "")
                if len(str(result)) > 2000:
                    await m.channel.send(
                        "Discord do not allow more than 2000 character, therefore this question you asked `{}` cannot be answered".format(
                            content
                        )
                    )
                else:
                    await m.channel.send(result)
            except Exception as e:
                print(e)


Oxerator().client.run(config["token"])
