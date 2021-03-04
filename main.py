import telebot
from telebot import types

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="issiqnonbot"

)

mycursor = mydb.cursor()

# sql = "INSERT INTO test (chat_id) VALUES (%s)"
# sql1 = "INSERT INTO test (chat_id) VALUES (%s)"
# sql2 = "UPDATE test SET name = %s WHERE test.chat_id = %s"
# sql3 = "UPDATE test SET number = %s WHERE test.chat_id = %s"
# sql4 = "UPDATE test SET location = %s WHERE test.chat_id = %s"
# sql5 = "UPDATE test SET set = %s WHERE test.chat_id = %s"


# val = (message.text, message.chat.id)
#
#             mycursor.execute(sql, val)
#             mydb.commit()
#             print(message.text)
name = ''
surname = ''
age = 0
number=0

bot = telebot.TeleBot("1522468171:AAEWg026vU5I3SXMc_OdA8L5HPg_vE72z7Y")


user_data={}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    #
    sqldel = "DELETE FROM test WHERE chat_id = %s"
    adr = (message.chat.id,)
    mycursor.execute(sqldel, adr)
    mydb.commit()
    #


    # print(mycursor.rowcount, "record(s) deleted")

    #

    sql = "INSERT INTO test (chat_id, name) VALUES (%s, %s)"

    val = (message.chat.id, "New")

    mycursor.execute(sql, val)

    mydb.commit()

    # print(message.text)
# keyboard
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("🇺🇸", callback_data="states")
    item2 = types.InlineKeyboardButton("🇷🇺", callback_data="russia")
    item3 = types.InlineKeyboardButton("🇺🇿", callback_data="uzb")

    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, "🇺🇿\nHush kelibsiz, {0.first_name}!\nMening ismim <b>{1.first_name}</b>. Bizning hizmatimizdan foydalanayotganingizdan mamnunmiz!\n👇🏾Iltimos, tilni tanglang"
                                       "\n\n🇷🇺\nДобро пожаловать, {0.first_name}!\nМоё имя <b>{1.first_name}</b>. Мы рады, что Вы пользуетесь нашим сервисом!\n👇🏾Пожалуйста, выберите язык"                                       
                                        "\n\n🇺🇸\nWelcome, {0.first_name}!\nMy name is <b>{1.first_name}</b>. We are pleasant that You are using our service!\n👇🏾Please, choose the language".format(message.from_user,bot.get_me()),
                    parse_mode= "html", reply_markup=markup)



@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
         try:
             if call.message:
                 if call.data == 'states':
                     bot.send_message(call.message.chat.id, "Please, input your full name")
                     bot.register_next_step_handler(call.message, echo_usa)

                 elif call.data == 'russia':
                     bot.send_message(call.message.chat.id, "Пожалуйста, введите ваше имя и фамилию")
                     bot.register_next_step_handler(call.message, echo_russia)

                 elif call.data == 'uzb':
                     bot.send_message(call.message.chat.id, "Iltimos, ismingiz va familiyangizni yozing")
                     bot.register_next_step_handler(call.message, echo_uzb)

                 # print(call.message.chat.id)
                 # val1 = call.message.chat.id
                 # mycursor.execute(sql1, val1)
                 # mydb.commit()

                 print(call.data)
                 sql = "UPDATE `test` SET `lang` = %s WHERE `test`.`chat_id` = %s"
                 val = (call.data, call.message.chat.id)
                 mycursor.execute(sql, val)

                 mydb.commit()

         except Exception as e:
            print(repr(e))



             #--------------START Если юзер выбрал США-----------------------


def echo_usa(message):
    try:
                if  ((message.text>='a' and message.text<='z') or (message.text >="A" and message.text<="Z") or (message.text>='а' and message.text<='я') or (message.text>='А' and message.text<='Я')):
                    print(message.text)

                    sql = "UPDATE `test` SET `name` = %s WHERE `test`.`chat_id` = %s"
                    val = (message.text, message.chat.id)
                    mycursor.execute(sql, val)
                    mydb.commit()

                    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=True)
                    button_phone = types.KeyboardButton(text="Send phone contact", request_contact=True)
                    keyboard.add((button_phone))
                    bot.send_message(message.chat.id, " Please, share with Your contact.", reply_markup=keyboard)
                    bot.register_next_step_handler(message, location_usa)




                else:
                    bot.send_message(message.chat.id,"Please,write you name correctly")
                    bot.register_next_step_handler(message, echo_usa)





    except Exception as e:
            print(repr(e))



	#bot.reply_to(message, message.text)





def location_usa(message):

    print(message.contact)

    if (message.contact):

        print(message.contact.phone_number)
        sql = "UPDATE `test` SET `number` = %s WHERE `test`.`chat_id` = %s"
        val = (message.contact.phone_number, message.chat.id)
        mycursor.execute(sql, val)
        mydb.commit()

        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button_geo = types.KeyboardButton(text="Send location", request_location=True)
        keyboard.add(button_geo)
        bot.send_message(message.chat.id, "Please, share with Your location.", reply_markup=keyboard)
        bot.register_next_step_handler(message, oursets_usa)

    else:
        print(message.text)
        bot.send_message(message.chat.id, "You must to share your contact")

        bot.register_next_step_handler(message,location_usa)





def oursets_usa(message):
    print(message.location)

    if (message.location):
        sql = "UPDATE `test` SET `latitude` = %s, `longitude` = %s WHERE `test`.`chat_id` = %s"
        val = (message.location.latitude, message.location.longitude, message.chat.id)
        mycursor.execute(sql, val)
        mydb.commit()

        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        set1choose = types.KeyboardButton(text="Set 1")
        set2choose = types.KeyboardButton(text="Set 2")
        set3choose = types.KeyboardButton(text="Customer Order")
        keyboard.add(set1choose, set2choose, set3choose)
        bot.send_message(message.chat.id, "Hot brad for the breakfast every day🤩"
                                          "\nPlease check our options out👇🏾"
                                          "\n\n🔸Set 1:"
                                          "\n        Delivery of 2 hot breads every day during 1 month"
                                          "\n        Price:  120 000 sum + delivery cost"
                                          "\n\n🔸Set 2:"
                                          "\n        Delivery of 4 hot breads every day during 1 month "
                                          "\n        Price:  240 000 sum + delivery cost"
                                          "\n\n🔸 Custom order"
                                          "\n        Your conditions and our offer "

                                          "\n", reply_markup=keyboard)
    else:
        print(message.text)
        bot.send_message(message.chat.id, "You must to share your location(no need to write)")

        bot.register_next_step_handler(message,oursets_usa)






@bot.message_handler(content_types=['text'])
def lalala_usa(message):
    print(message)



    if message.text=="Set 1":
        sql = "UPDATE `test` SET `set` = %s WHERE `test`.`chat_id` = %s"
        val = (message.text, message.chat.id)
        mycursor.execute(sql, val)
        mydb.commit()

        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        set1choose = types.KeyboardButton(text="CONFIRM")
        set2choose = types.KeyboardButton(text="REFRESH")
        keyboard.add(set1choose, set2choose)
        bot.send_message(message.chat.id, "🔸 Set #1\n\n"
                                             "💳 2 hot breads for the breakfast everyday during 1 month  \n"
                                             "2000 som * 2 breads * 30 days = 120 000 som \n\n"
                                             "🏎 Delivery cost:\n"
                                             "5000 som (up to 5 breads) * 30 days = 150 000 som\n\n"
                                             "🕒 The delivery will be executed during 30 mins or less\n\n"
                                             "💳 Total cost: 270 000 som\n\n"
                                             "✅ Please confirm your subscription"

                                          "\n", reply_markup=keyboard)




    elif message.text=="Set 2":

        sql = "UPDATE `test` SET `set` = %s WHERE `test`.`chat_id` = %s"
        val = (message.text, message.chat.id)
        mycursor.execute(sql, val)
        mydb.commit()

        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        set1choose = types.KeyboardButton(text="CONFIRM")
        set2choose = types.KeyboardButton(text="REFRESH")
        keyboard.add(set1choose, set2choose)

        bot.send_message(message.chat.id, "🔸 Set #2\n\n"
                                          "📌 4 hot breads for the breakfast everyday during 1 month\n"
                                          "2000 som * 4 breads * 30 days = 240 000 som\n\n"
                                          "🏎 Delivery cost:\n"
                                          " 5000 som (up to 5 breads) * 30 days = 150 000 som\n\n"
                                          "🕒 The delivery will be executed during 30 mins or less\n\n"
                                          "💳 Total cost: 390 000 som\n\n"
                                          "✅ Please confirm your subscription", reply_markup=keyboard)

    elif message.text=="CONFIRM":
        sql = "UPDATE `test` SET `CONFIRMATION` = %s WHERE `test`.`chat_id` = %s"
        val = (message.text, message.chat.id)
        mycursor.execute(sql, val)
        mydb.commit()

        bot.send_message(message.chat.id, "We will contact you as soon as possible")

    elif message.text == "REFRESH":
       bot.register_next_step_handler(message,send_welcome)

    elif message.text =="Customer Order":
        sql = "UPDATE `test` SET `set` = %s WHERE `test`.`chat_id` = %s"
        val = (message.text, message.chat.id)
        mycursor.execute(sql, val)
        mydb.commit()

        bot.send_message(message.chat.id,"Please write down your offers and our Client Service Officer will contact you as soon as possible")

        bot.register_next_step_handler(message,ifwrittencustomorder_usa)
    # ------------------------------------------------
    # -------------------------------------------------
    # Если  в русском интерфейсе  юзер выбирает сеты
    # -------------------------------------------------
    # ---------------------------------------------


    elif message.text=="ПОДТВЕРДИТЬ":
        sql = "UPDATE `test` SET `CONFIRMATION` = %s WHERE `test`.`chat_id` = %s"
        val = (message.text, message.chat.id)
        mycursor.execute(sql, val)
        mydb.commit()

        bot.send_message(message.chat.id, "Наш менеджер свяжеться с вами")

    elif message.text == "ЗАНОВО":
       bot.register_next_step_handler(message,send_welcome)





    elif message.text=="Сет 1":

        sql = "UPDATE `test` SET `set` = %s WHERE `test`.`chat_id` = %s"
        val = (message.text, message.chat.id)
        mycursor.execute(sql, val)
        mydb.commit()

        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        set1choose = types.KeyboardButton(text="ПОДТВЕРДИТЬ")
        set2choose = types.KeyboardButton(text="ЗАНОВО")
        keyboard.add(set1choose, set2choose)

        bot.send_message(message.chat.id, "🔸 Сет #1\n\n"
                                          "📌 2 горячие лепёшки на завтрак в течении 1 месяца  \n"
                                          "2000 сум * 4 лепёшки * 30 дней = 120 000 сум  \n\n"
                                          "🏎 Цена доставки:\n"
                                          "5000 сум (до 5 лепёшек) * 30 дней = 150 000 сум\n\n"
                                          "🕒 Доставка осуществляется в меньше чем за 30 минут\n\n"
                                          "💳 Общая цена: 270 000 сум\n\n"
                                          "✅ Пожалуйста подтвердите заказ",reply_markup=keyboard)
    elif message.text=="Сет 2":

        sql = "UPDATE `test` SET `set` = %s WHERE `test`.`chat_id` = %s"
        val = (message.text, message.chat.id)
        mycursor.execute(sql, val)
        mydb.commit()

        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        set1choose = types.KeyboardButton(text="ПОДТВЕРДИТЬ")
        set2choose = types.KeyboardButton(text="ЗАНОВО")
        keyboard.add(set1choose, set2choose)

        bot.send_message(message.chat.id, "🔸 Сет #2\n\n"
                                          "📌 4 горячие лепёшки на завтрак в течении 1 месяца \n"
                                          " 2000 сум * 4 лепёшки * 30 дней = 240 000 сум\n\n"
                                          "🏎 Цена доставки:\n"
                                          " 5000 сум (до 5 лепёшек) * 30 дней = 150 000 сум\n\n"
                                          "🕒 Доставка осуществляется в меньше чем за 30 минут\n\n"
                                          "💳 Общая цена: 390 000 сум\n\n"
                                          "✅ Пожалуйста подтвердите заказ",reply_markup=keyboard)
    elif message.text=="Особый заказ":
        sql = "UPDATE `test` SET `set` = %s WHERE `test`.`chat_id` = %s"
        val = (message.text, message.chat.id)
        mycursor.execute(sql, val)
        mydb.commit()

        bot.send_message(message.chat.id,
                         "Пожалуйста, напишите Ваши предложения и наш Менеджер по работе с клиентами")

        bot.register_next_step_handler(message, ifwrittencustomorder_ru)

        # КОНЕЦ Если  в русском интерфейсе  юзер выбирает сеты

        # Если  в узбекском интерфейсе  юзер выбирает сеты

    elif message.text == "Tasdiqlash":
        sql = "UPDATE `test` SET `CONFIRMATION` = %s WHERE `test`.`chat_id` = %s"
        val = (message.text, message.chat.id)
        mycursor.execute(sql, val)
        mydb.commit()

        bot.send_message(message.chat.id, "Bizning menedjeremiz siz bilan aloqaga chikadi.")

    elif message.text == "Qaytadan":
        bot.register_next_step_handler(message, send_welcome)


    elif message.text == "Set №1":

        sql = "UPDATE `test` SET `set` = %s WHERE `test`.`chat_id` = %s"
        val = (message.text, message.chat.id)
        mycursor.execute(sql, val)
        mydb.commit()

        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        set1choose = types.KeyboardButton(text="Tasdiqlash")
        set2choose = types.KeyboardButton(text="Qaytadan")
        keyboard.add(set1choose, set2choose)

        bot.send_message(message.chat.id, "🔸 Set #1\n\n"
                                          "💳 1 oy davomida nonushtaga 2 tadan qaynoq non  \n"
                                          "2000 sum * 2 qaynoq non * 30 kun = 120 000 so'm  \n\n"
                                          "🏎 Yetkazib berish narxi:\n"
                                          "5000 so'm (5ta nongacha) * 30 kun = 150 000 сум\n\n"
                                          "🕒 Yetkazib berish 30 minut ichida amalga oshirilad\n\n"
                                          "💳 Umumiy Narx: 270 000 сум\n\n"
                                          "✅ Iltimos buyurtmani tasdiqlang",reply_markup=keyboard)
    elif message.text == "Set №2":

        sql = "UPDATE `test` SET `set` = %s WHERE `test`.`chat_id` = %s"
        val = (message.text, message.chat.id)
        mycursor.execute(sql, val)
        mydb.commit()


        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        set1choose = types.KeyboardButton(text="Tasdiqlash")
        set2choose = types.KeyboardButton(text="Qaytadan")
        keyboard.add(set1choose, set2choose)

        bot.send_message(message.chat.id, "🔸 Set #2\n\n"
                                          "💳 1 oy davomida nonushtaga 2 tadan qaynoq non  \n"
                                          "2000 sum * 4 qaynoq non * 30 kun = 240 000 so'm \n\n"
                                          "🏎 Yetkazib berish narxi:\n"
                                          "5000 so'm (5ta nongacha) * 30 kun = 150 000 сум\n\n"
                                          "🕒 Yetkazib berish 30 minut ichida amalga oshirilad\n\n"
                                          "💳 Umumiy Narx: 390 000 сум\n\n"
                                          "✅ Iltimos buyurtmani tasdiqlang",reply_markup=keyboard)
    elif message.text == "Maxsus buyurtma":

        sql = "UPDATE `test` SET `set` = %s WHERE `test`.`chat_id` = %s"
        val = (message.text, message.chat.id)
        mycursor.execute(sql, val)
        mydb.commit()


        bot.send_message(message.chat.id,
                         "Iltimos, O'zingizni shartlaringizni yozing va mijozlar bilan ishlash bo'limining xodimi siz bilan bog'lanadi")
        bot.register_next_step_handler(message, ifwrittencustomorder_uz)

def ifwrittencustomorder_usa(message):
    sql = "UPDATE `test` SET `CUSTOM` = %s WHERE `test`.`chat_id` = %s"
    val = (message.text, message.chat.id)
    mycursor.execute(sql, val)
    mydb.commit()

    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    set1choose = types.KeyboardButton(text="CONFIRM")
    set2choose = types.KeyboardButton(text="REFRESH")
    keyboard.add(set1choose, set2choose)
    bot.send_message(message.chat.id, "✅ Please confirm your subscription"

                                      "\n", reply_markup=keyboard)

def ifwrittencustomorder_ru(message):
        sql = "UPDATE `test` SET `CUSTOM` = %s WHERE `test`.`chat_id` = %s"
        val = (message.text, message.chat.id)
        mycursor.execute(sql, val)
        mydb.commit()

        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        set1choose = types.KeyboardButton(text="ПОДТВЕРДИТЬ")
        set2choose = types.KeyboardButton(text="ЗАНОВО")
        keyboard.add(set1choose, set2choose)
        bot.send_message(message.chat.id, "✅ Please confirm your subscription"

                                          "\n", reply_markup=keyboard)

def ifwrittencustomorder_uz(message):
            sql = "UPDATE `test` SET `CUSTOM` = %s WHERE `test`.`chat_id` = %s"
            val = (message.text, message.chat.id)
            mycursor.execute(sql, val)
            mydb.commit()

            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            set1choose = types.KeyboardButton(text="Tasdiqlash")
            set2choose = types.KeyboardButton(text="Qaytadan")
            keyboard.add(set1choose, set2choose)
            bot.send_message(message.chat.id, "✅ Please confirm your subscription"

                                              "\n", reply_markup=keyboard)

        #КОНЕЦ Если  в узбекском интерфейсе  юзер выбирает сеты



    # --------------FINISH Если юзер выбрал США-----------------------


    # --------------START Если юзер выбрал РОССИЮ.-----------------------
@bot.message_handler(func=lambda m: True)
def echo_russia(message):
        try:
            if ((message.text >= 'a' and message.text <= 'z') or (message.text >= "A" and message.text <= "Z") or (
                    message.text >= 'а' and message.text <= 'я') or (message.text >= 'А' and message.text <= 'Я')):
                print(message.text)

                sql = "UPDATE `test` SET `name` = %s WHERE `test`.`chat_id` = %s"
                val = (message.text, message.chat.id)
                mycursor.execute(sql, val)
                mydb.commit()

                keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=True)
                button_phone = types.KeyboardButton(text="Отправить свой номер", request_contact=True)
                keyboard.add((button_phone))
                bot.send_message(message.chat.id, " Пожалуйста, отправьте свой номер.", reply_markup=keyboard)
                bot.register_next_step_handler(message, location_russia)


            else:
                bot.send_message(message.chat.id, "Пожалуйста, напишите свое имя правильно")
                bot.register_next_step_handler(message, echo_usa)





        except Exception as e:
            print(repr(e))


def location_russia(message):
    print(message.contact)

    if (message.contact):

        print(message.contact.phone_number)

        sql = "UPDATE `test` SET `number` = %s WHERE `test`.`chat_id` = %s"
        val = (message.contact.phone_number, message.chat.id)
        mycursor.execute(sql, val)
        mydb.commit()

        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
        keyboard.add(button_geo)
        bot.send_message(message.chat.id, "Пожалуйста, поделитесь своим местоположением.", reply_markup=keyboard)
        bot.register_next_step_handler(message, oursets_russia)

    else:
        print(message.text)
        bot.send_message(message.chat.id, "Вы должны переслать свои контакты")

        bot.register_next_step_handler(message,location_russia)


def oursets_russia(message):

    if (message.location):
            print(message.location)
            sql = "UPDATE `test` SET `latitude` = %s, `longitude` = %s WHERE `test`.`chat_id` = %s"
            val = (message.location.latitude, message.location.longitude, message.chat.id)
            mycursor.execute(sql, val)

            mydb.commit()

            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            set1chooserus = types.KeyboardButton(text="Сет 1")
            set2chooserus= types.KeyboardButton(text="Сет 2")
            set3chooserus = types.KeyboardButton(text="Особый заказ")
            keyboard.add(set1chooserus, set2chooserus, set3chooserus)
            bot.send_message(message.chat.id,"Горячие лепешки на завтрак каждый день🤩"
                                                   "\nПожайлуста, выберите  опции 👇🏾"
                                                   "\n\n🔸Сет 1:"
                                                   "\n        Доставка 2х горячих лепёшек в течении 1 месяца"
                                                   "\n        Цена:  120 000 сум + плата за доставку"
                                                   "\n\n🔸Сет 2:"
                                                   "\n        Доставка 4х горячих лепёшек в течении 1 месяца "
                                                   "\n        Цена:  240 000 сум + плата за доставку"
                                                   "\n\n🔸Особый заказ"
                                                   "\n        Ваши условия и наше предложение "
        
                                               "\n", reply_markup=keyboard)

    else:
        print(message.text)
        bot.send_message(message.chat.id, "Вы должны указать свое местоположение (писать не нужно)")

        bot.register_next_step_handler(message, oursets_usa)




    # --------------FINISH Если юзер выбрал РОССИЮ.-----------------------

    # --------------START Если юзер выбрал UZBEKISTAN.-----------------------
@bot.message_handler(func=lambda m: True)
def echo_uzb(message):
        try:
            if ((message.text >= 'a' and message.text <= 'z') or (message.text >= "A" and message.text <= "Z") or (message.text >= 'а' and message.text <= 'я') or (message.text >= 'А' and message.text <= 'Я')):
                print(message.text)

                sql = "UPDATE `test` SET `name` = %s WHERE `test`.`chat_id` = %s"
                val = (message.text, message.chat.id)
                mycursor.execute(sql, val)
                mydb.commit()

                keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=True)
                button_phone = types.KeyboardButton(text="Telefon raqamni jo'natmoq", request_contact=True)
                keyboard.add((button_phone))
                bot.send_message(message.chat.id, " Iltimos, telefon raqamingiz bilan ulashing", reply_markup=keyboard)
                bot.register_next_step_handler(message, location_uzb)


            else:
                bot.send_message(message.chat.id, "Iltimos, ismingizni to'g'ri yozing")
                bot.register_next_step_handler(message, echo_uzb)



        except Exception as e:
            print(repr(e))






def location_uzb(message):
        print(message.contact)

        if (message.contact):
            print(message.contact.phone_number)


            sql = "UPDATE `test` SET `number` = %s WHERE `test`.`chat_id` = %s"
            val = (message.contact.phone_number, message.chat.id)
            mycursor.execute(sql, val)
            mydb.commit()

            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=True)
            button_geo = types.KeyboardButton(text="Manzilni jo'natmoq", request_location=True)
            keyboard.add(button_geo)
            bot.send_message(message.chat.id, "Iltimos, manzilingiz bilan ulashing", reply_markup=keyboard)
            bot.register_next_step_handler(message, oursets_uzb)


        else:
            print(message.text)
            bot.send_message(message.chat.id, "Kontaktlaringizni yo'naltirishingiz kerak")
            bot.register_next_step_handler(message, location_uzb)

def oursets_uzb(message):
    if (message.location):
        print(message.location)
        sql = "UPDATE `test` SET `latitude` = %s, `longitude` = %s WHERE `test`.`chat_id` = %s"
        val = (message.location.latitude, message.location.longitude, message.chat.id)
        mycursor.execute(sql, val)

        mydb.commit()

        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        set1choose = types.KeyboardButton(text="Set №1")
        set2choose = types.KeyboardButton(text="Set №2")
        set3choose = types.KeyboardButton(text="Maxsus buyurtma")
        keyboard.add(set1choose, set2choose, set3choose)
        bot.send_message(message.chat.id,"Har kuni nonushtaga qaynoq nonlar🤩"
                                               "\nIltimos, imkoniyatlarni tanlang👇🏾"
                                               "\n\n🔸Set 1:"
                                               "\n        1 oy davomida 2ta qaynoq non yetkazib berish"
                                               "\n        Narxi:  120 000 so'm + yetkazib berish narxi"
                                               "\n\n🔸Set 2:"
                                               "\n        1 oy davomida 4ta qaynoq non yetkazib berish "
                                               "\n        Narxi:  240 000 so'm + yetkazib berish narxi"
                                               "\n\n🔸Maxsus buyurtma"
                                               "\n        Sizning shartlaringiz va bizning taklifimiz"
    
                                               "\n", reply_markup=keyboard)

    else:
        print(message.text)
        bot.send_message(message.chat.id, "Siz joylashgan joyingizni ko'rsatishingiz kerak (yozishning hojati yo'q)")

        bot.register_next_step_handler(message, oursets_uzb)

        # --------------FINISH Если юзер выбрал UZBEKISTAN.-----------------------


bot.polling()