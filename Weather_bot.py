from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

# initialize telegram bot
bot_token = "5616684519:AAF6CpH3ESy58bED-39a2KTR05PGrgeZvVQ"
update = Updater(bot_token, use_context=True)

dispatcher = update.dispatcher


# Greet message when the bot start
def start(update, context):
    greet = """WELCOME TO WEATHER-FORECAST💧⛄️☁️☔️"""

    context.bot.send_chat_action(
        chat_id=update.effective_message.chat_id, action="typing"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=greet)


def handle_message(update, context):

    city = str(update.message.text).lower()

    import requests

    api_key = "4c0b058647d489799cb157d186004397"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    data = requests.get(url).json()

    def get_weather():
        if data["cod"] == 200:
            temp = data["main"]["temp"]
            weather = data["weather"][0]["main"]
            wind = data["wind"]["speed"]
            temp -= 273.15
            return round(temp, 2), weather, wind
        else:
            return "City not found"

    if get_weather() == "City not found":
        text = "City not found🚫🌈!"
    else:
        temp, weather, wind = get_weather()
        # print(f"       {city} is {weather} with the temperature of {temp}c")

        text = f"WEATHER AT {city.upper()}:\n🌡Temperature  : {temp} C\n⛅️ Weather     : {weather}\n💨 Wind        : {wind} Km/h"

    context.bot.send_chat_action(
        chat_id=update.effective_message.chat_id, action="typing"
    )

    # send response back to telegram user
    context.bot.send_message(chat_id=update.effective_message.chat_id, text=f"{text}")


# def youtube_url(update, context):
#     update.message.reply_text(
#         "Youtube Link =>\
#     https://www.youtube.com/"
#     )


def help(update, context):
    text = """Available Commands :-
    Enter a city name to get the weather forecast - Example: //London"""
    context.bot.send_chat_action(
        chat_id=update.effective_message.chat_id, action="typing"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler("help", help)
dispatcher.add_handler(help_handler)


# dispatcher.add_handler(CommandHandler("youtube", youtube_url))


handle_message = MessageHandler(Filters.text, handle_message)
dispatcher.add_handler(handle_message)

update.start_polling()
update.idle()
