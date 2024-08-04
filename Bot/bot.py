import telebot
from Database.ChannelsDatabase import ChannelsDatabase
from Database.UsersDatabase import UsersDatabase
from Database.WalletDatabase import WalletDatabase
from privacy import BOT_TOKEN
from Bot.messages import *
from Bot.buttons import *


bot = telebot.TeleBot(BOT_TOKEN);


@bot.message_handler(commands=["start", "language"])
def start (message) -> None:
    database = UsersDatabase(message.chat.id);
    database.addUser();
    markup = telebot.types.InlineKeyboardMarkup();
    for text, callback in startButtons.items():
        btn = telebot.types.InlineKeyboardButton(text=text, callback_data=callback)
        markup.add(btn);
    bot.send_message(chat_id=message.chat.id, text=startMessage, parse_mode="html", reply_markup=markup);


@bot.callback_query_handler(func=lambda call: True)
def inline (call) -> None:
    database = UsersDatabase(call.message.chat.id);
    database.addUser();
    language: str = database.takeLanguage();
    if (call.data in startButtons.values()):
        database.updateLanguage(call.data);
        language = call.data;
        markup = telebot.types.InlineKeyboardMarkup();
        nxt = telebot.types.InlineKeyboardButton(text=lang_ch[language][1], callback_data="starting");
        markup.add(nxt);
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=lang_ch[language][0], parse_mode="html", reply_markup=markup);
    elif (call.data == "starting"):
        walletDatabase = WalletDatabase(call.message.chat.id);
        if (walletDatabase.isRegistered()):
            call.data = "mainmenu";
            inline(call);
            return;
        markup = telebot.types.InlineKeyboardMarkup();
        btn1 = telebot.types.InlineKeyboardButton(text=howItWorks[language][0], url=howItWorks[language][1]);
        btn2 = telebot.types.InlineKeyboardButton(text=startMakeMoney[language][0], callback_data=startMakeMoney[language][1]);
        markup.add(btn1);
        markup.add(btn2);
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"{startMenu[language][0]}{call.message.chat.first_name}{startMenu[language][1]}",
                              parse_mode="html", reply_markup=markup);
    elif (call.data == "activate"):
        walletDatabase = WalletDatabase(call.message.chat.id);
        walletDatabase.createWallet();
        call.data = "mainmenu";
        inline(call);
        return;
    elif (call.data == "mainmenu"):
        walletDatabase = WalletDatabase(call.message.chat.id);
        userSubscribes: tuple[int, float] = walletDatabase.getAll();
        dailyIncome: float = 0.0;
        unsubscribeCount: int = 0;
        for channelID, price in userSubscribes:
            status = bot.get_chat_member(chat_id=channelID, user_id=call.message.chat.id).status;
            if (status in ("member", "creator", "administrator")):
                dailyIncome += price;
            else:
                unsubscribeCount += 1;
        markup = telebot.types.InlineKeyboardMarkup();
        for text, callback in mainmenuButtons.items():
            btn = telebot.types.InlineKeyboardButton(text=text, callback_data=callback);
            markup.add(btn);
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=(mainmenu % (call.message.chat.first_name, len(userSubscribes), dailyIncome)),
                              parse_mode="html", reply_markup=markup);
        if (unsubscribeCount != 0):
            bot.send_message(chat_id=call.message.chat.id, text=(breakIncome[language] % unsubscribeCount), parse_mode="html");


def startBot () -> None:
    print("<<< Succesfuly started >>>");
    bot.polling(none_stop=True, interval=0);