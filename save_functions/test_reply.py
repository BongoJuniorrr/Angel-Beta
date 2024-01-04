import chatbot

while True:
    you = input("You: ")
    if (you == "turn off"):
        exit()
    ans = chatbot.reply(you)
    print("Angel: " + ans)