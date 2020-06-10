import json
import discord
import requests

TG_URL = "https://api.telegram.org/bot{}/sendMessage"

class Discogram(discord.Client):
    def __init__(self, telegram_token, chat_id):
        super().__init__()
        self.telegram_token = telegram_token
        self.chat_id = chat_id

    def send_tg_message(self, msg):
        data = {"chat_id": self.chat_id, "text": msg}
        print(f"Sending: {msg}")
        print(requests.post(TG_URL.format(self.telegram_token), data=data).text)

    async def on_ready(self):
        print('Logged on as %s', self.user)

    async def on_voice_state_update(self, member, before, after):
        if before.channel == None and after.channel != None:
            msg = f"User: {member.name} connected to the channel: {after.channel.name}"
            self.send_tg_message(msg)

        elif before.channel != None and after.channel == None:
            msg = f"User: {member.name} disconnected from the channel: {before.channel.name}"
            self.send_tg_message(msg)

if __name__ == '__main__':
    with open("config.json", "r") as f:
        config = json.load(f)

    client = Discogram(config["telegram_token"], config["telegram_chat"])
    client.run(config["discord_token"])
