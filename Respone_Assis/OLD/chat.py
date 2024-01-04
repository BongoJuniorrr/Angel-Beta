import asyncio, json
import re
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle

async def main(query): # define the function with query as an argument
    try:
        cookies = json.loads(open("bing_cookies.json", encoding="utf-8").read())  # might omit cookies option
        bot = await Chatbot.create(cookies=cookies)
        await bot.ask(prompt=query, conversation_style=ConversationStyle.creative)
        response = await bot.ask(prompt=query, conversation_style=ConversationStyle.creative)
        for message in response["item"]["messages"]:
            if message["author"] == "bot":
                bot_response = message["text"]
        # Remove [^#^] citations in response
        answer = re.sub('\[\^\d+\^\]', '', str(bot_response))
        await bot.close()
        return answer # return the answer
    except:
        return "Can't do that"

# question = input("Ask: ")
# answer = asyncio.run(main(question))
# print(answer)

