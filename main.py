from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from bs4 import BeautifulSoup
from random_task import *
from image import search_picture_img
from user import user_about
from daily_rating import *
from vertification_username import validation_username
from login import *
import json

def ldh():
    with open('Bot_token.json', 'r') as f:
        return json.load(f)
token = ldh()

valid = False
username = False
tekshir = False
API_TOKEN = token['Token']

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command(commands=["sign_in"]))
async def sign_in_user(message: types.Message):
    global valid
    if not valid:
        args = message.text.split()
        if len(args) != 2:
            await message.reply("Xato kiritdingiz!!! /sign_in <attempt_number> ko'rinishida kiriting")
        else:
            ans = login_user(int(args[1]), f"print({message.from_user.id})", username)
            if ans:
                res = registerr(username, message.from_user.id)
                if res:
                    valid = True
                    await message.reply(f"Tabriklaymiz siz botimizdan ro'yhatdan o'tdingiz. /start buyrug'i bilan siz botni faollashtirishingiz mumkin.\n Sizni bu bot uchun parollingiz {message.from_user.id} bu parolni hech kimga bermang.")
                else:
                    await message.reply("Siz allaqachon ro'yhatdan o'tkansiz. Siz /sign_up <password> orqali o'z hisobingizga kirib olishingiz mumkin.")
            else:
                await message.reply("Xato attempt number yoki kodni xato yozgansiz!!!")
    else:
        await message.reply("Siz avval username ingizni ro'yhatdan otkazib oling.")

@dp.message(Command(commands=["sign_up"]))
async def sign_up_users(message: types.Message):
    global valid
    if valid:
        await message.reply("Siz ro'hatdan o'tkansiz. Siz oz profilingizdasiz.")
    else:
        args = message.text.split()
        if len(args) != 2:
            await message.reply("Siz xato formatda kiritdingiz!!! /sign_up <password>")
        else:
            try:
                res = sign_up(username, int(args[1]))
                if res:
                    valid = True
                    await message.reply("Tabriklaymiz siz mufaqqiyatli kirdingiz!!! /start buyrugi orqali ishga kiriting.")
                else:
                    await message.reply("Afsuski siz parolingizni xato kiritdingiz!!!")
            except:
                await message.reply("Siz xato formatda kitdingiz!!!")
@dp.message(Command(commands=["register"]))
async def regis(message: types.Message):
    if valid:
        await message.reply("Siz allaqachon ro'yhatdan otkansiz")
    else:
        if not username:
            await message.reply(
                "Siz /login <your_username> qilib yuboring. Oshanda Siz ro'yhatdan otasiz.\n"
                "Misol uchun /login python_devopover."
            )
        else:
            await message.reply(f"Xo'sh endi siz ushbu masalaga <https://robocontest.uz/tasks/EKPQXI3GQ1> shu masalaga <print({message.from_user.id})> codini buboring va yuborgan attemptiyizni nomerini /sign_in <attempts_number> ni yuboring.")

@dp.message(Command(commands=['login']))
async def user_valid(message: types.Message):
    global valid
    global username
    if not valid:
        args = message.text.split()
        if len(args) < 2:
            await message.reply('Usernameni kiriting!!!')
            return
        valid_user_ = validation_username(args[1])
        # print(args)
        if valid_user_:
            username = args[1]
            await message.reply("Siz oldin botimizdan ro'yhatdan o'tkan bolsangiz /sign_up <password> orqali royhatdan otib oling. Agar oldin royhatdan otmagan bolsangiz /register orqali royhatdan oting.")
            # await message.reply(f"Xo'sh endi siz ushbu masalaga <https://robocontest.uz/tasks/EKPQXI3GQ1> shu masalaga <print({message.from_user.id})> codini buboring va yuborgan attemptiyizni nomerini /sign_in <attempts_number> ni yuboring.")
            # await message.reply("Tabriklaymiz siz ro'yhatdan o'tdingiz!!!\n" "/start buyrug'i bilan botni ishlatishingiz mumkin.")
        else:
            await message.reply("Siz usernameni xato yozdingiz!!!")
    else:
        await message.reply(f"Siz alaqchon ro'yhatdan otkansiz. Siz {username} useri bilan royhatdan otkansiz.")



@dp.message(Command(commands=["start"]))
async def send_welcome(message: types.Message):
    if valid:
        await message.answer(
            "Assalomu alaykum!\n"
            "Men sizga yordam berish uchun tayyorman. Quyidagilarni sinab ko'ring:\n\n"
            "🔹 /user_about <username> - Foydalanuvchi haqida ma'lumot\n"
            "🔹 /my_user_about -> Sizni profilingizdagi malumotlarni olib beradi\n"
            "🔹 /logout -> Profilingizdan chiqadi.\n"
            "🔹 /help -> Sizga yordam beradi.\n"
            "🔹 /random_task <difficult min> <difficult max> - Tasodifiy topshiriq\n\n"

            "Yordam kerak bo'lsa, menga xabar bering! 😊"
        )
    else:
        if not username:
            await message.answer(
                "Siz /login <your_username> qilib yuboring. Oshanda Siz ro'yhatdan otasiz.\n"
                "Misol uchun /login python_devopover."
            )
        else:
            await message.reply("Siz ro'yhatdan o'tmagansiz. Yani agar oldin ro'yhatdan otkan bolsangiz /sign_up <password> buyrug'i bilan ro'yhatdan o'tib oling. Agar hali ro'yhatdan o'tmagan bolsangiz /sign_in <attempt_number> orqali ro'yhatdan o'tib oling.")


@dp.message(Command(commands=["user_about"]))
async def user_about_handler(message: types.Message):
    if valid:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.answer("Iltimos, foydalanuvchi nomini kiriting! Misol: /user_about <username>")
            return

        usere = args[1].strip()
        ans = user_about(usere)
        if len(ans) == 1:
            await message.answer(*ans)
            return
        img_url = search_picture_img(usere)
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=img_url,
            caption=f"{usere} natijalari:\n🏆 O'rin: {ans[0]}\n📊 Reyting: {ans[1]}\n📊 Max Reyting: {ans[2]}\n🏆 Rating name: {ans[-1]}",
        )
    else:
        if not username:
            await message.answer(
                "Siz /login <your_username> qilib yuboring. Oshanda Siz ro'yhatdan otasiz.\n"
                "Misol uchun /login python_devopover."
            )
        else:
            await message.reply("Siz ro'yhatdan o'tmagansiz. Yani agar oldin ro'yhatdan otkan bolsangiz /sign_up <password> buyrug'i bilan ro'yhatdan o'tib oling. Agar hali ro'yhatdan o'tmagan bolsangiz /sign_in <attempt_number> orqali ro'yhatdan o'tib oling.")

@dp.message(Command(commands=["my_user_about"]))
async def user_about_handler(message: types.Message):
    if valid:
        usere = username
        ans = user_about(usere)
        if len(ans) == 1:
            await message.answer(*ans)
            return
        img_url = search_picture_img(usere)
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=img_url,
            caption=f"Sizning natijalaringiz:\n🏆 O'rin: {ans[0]}\n📊 Reyting: {ans[1]}\n📊 Max Reyting: {ans[2]}\n🏆 Rating name: {ans[-1]}",
        )
    else:
        if not username:
            await message.answer(
                "Siz /login <your_username> qilib yuboring. Oshanda Siz ro'yhatdan otasiz.\n"
                "Misol uchun /login python_devopover."
            )
        else:
            await message.reply("Siz ro'yhatdan o'tmagansiz. Yani agar oldin ro'yhatdan otkan bolsangiz /sign_up <password> buyrug'i bilan ro'yhatdan o'tib oling. Agar hali ro'yhatdan o'tmagan bolsangiz /sign_in <attempt_number> orqali ro'yhatdan o'tib oling.")

@dp.message(Command(commands=["random_task"]))
async def random_task_handler(message: types.Message):
    if valid:
        args = message.text.split(maxsplit=1)
        if len(args) < 1:
            await message.answer("Iltimos, foydalanuvchi nomi va qiyinchilik darajasini kiriting! Misol: /random_task <min> <max>")
            return

        try:
            parts = args[1].split()
            diff_mn = int(parts[0])
            diff_mx = int(parts[1])

            if diff_mn < 1 or diff_mx < 1:
                await message.answer('Siz manfiy yoki 0 reytingli masala kiritdingiz!!!')
                return
            if diff_mn > diff_mx:
                await message.answer('Minimal reyting maksimal reytingdan katta! Qayta urining!')
                return
            ans = version_1_1_choice_task(username, diff_mn, diff_mx)
            if len(ans) == 1:
                await message.answer(ans[0])
                return
            await message.answer(f"Sizga random qilingan masala {ans[1]} Bu masala qiyinchiligi {ans[0]}%")
        except (IndexError, ValueError):
            await message.answer("Xatolik! To'g'ri format: /random_task <min> <max>")
    else:
        if not username:
            await message.answer(
                "Siz /login <your_username> qilib yuboring. Oshanda Siz ro'yhatdan otasiz.\n"
                "Misol uchun /login python_devopover."
            )
        else:
            await message.reply("Siz ro'yhatdan o'tmagansiz. Yani agar oldin ro'yhatdan otkan bolsangiz /sign_up <password> buyrug'i bilan ro'yhatdan o'tib oling. Agar hali ro'yhatdan o'tmagan bolsangiz /sign_in <attempt_number> orqali ro'yhatdan o'tib oling.")


@dp.message(Command(commands=["help"]))
async def help_handler(message: types.Message):
    if valid:
        await message.answer(
            "/start -> Botni tanishtirish.\n"
            "/my_user_about -> Sizni profilingizdagi malumotlarni olib beradi\n"
            "/user_about <username> -> Profil ma'lumotlari.\n"
            "/random_task <min> <max> -> Tasodifiy masala tanlash.\n"
            "/logout -> Profilingizdan chiqadi.\n"
            "/my_daily_rank -> Sizning bugungi ishlagan masalalaringiz soni.\n"
            "/daily_top_10 -> Bugun eng ko'p yechgan top10 user.\n"
            "/daily_rank_problems -> Berilgan masala orqali siz kunllik reytingizni kotarasiz.\n"
            "/other -> Agar botimizda kamchilik, taklif, shikoyatlaringiz bolsa yozinglar. Unga /other <problem> ko'rinishida yozing."
        )
    else:
        if not username:
            await message.answer(
                "Siz /login <your_username> qilib yuboring. Oshanda Siz ro'yhatdan otasiz.\n"
                "Misol uchun /login python_devopover."
            )
        else:
            await message.reply("Siz ro'yhatdan o'tmagansiz. Yani agar oldin ro'yhatdan otkan bolsangiz /sign_up <password> buyrug'i bilan ro'yhatdan o'tib oling. Agar hali ro'yhatdan o'tmagan bolsangiz /sign_in <attempt_number> orqali ro'yhatdan o'tib oling.")


@dp.message(Command(commands=['my_daily_rank']))
async def my_daily(message: types.Message):
    if valid:
        tasksss = my_rating(username)
        await message.reply(
            f"Siz bugun {tasksss} ta masala ishladingiz"
        )
    else:
        if not username:
            await message.answer(
                "Siz /login <your_username> qilib yuboring. Oshanda Siz ro'yhatdan otasiz.\n"
                "Misol uchun /login python_devopover."
            )
        else:
            await message.reply("Siz ro'yhatdan o'tmagansiz. Yani agar oldin ro'yhatdan otkan bolsangiz /sign_up <password> buyrug'i bilan ro'yhatdan o'tib oling. Agar hali ro'yhatdan o'tmagan bolsangiz /sign_in <attempt_number> orqali ro'yhatdan o'tib oling.")

task_number_num = None
solved = False
@dp.message(Command(commands=['tekshirish']))
async def tek(message: types.Message):
    global solved
    if tekshir:
        k = accmi(task_number_num, username)
        if k:
            solved = True
            return
        



@dp.message(Command(commands=["daily_rank_problems"]))
async def prom(message: types.Message):
    global tekshir
    global task_number_num
    if valid:
        diff_mn = 1
        diff_mx = 99
        ans = version_1_1_choice_task(username, diff_mn, diff_mx)
        if len(ans) == 1:
            await message.answer(ans[0])
            return
        res = difficult(int(ans[0]))
        task_number_num = ans[2]
        await message.reply(f"Sizga {ans[1]} masalasi tushdi.")
        await message.reply(f"Agar masalani {res} min dan oldin yechib bolsangiz /tekshirish buyrug'ini kiriting")
        tekshir = True
        # task_number_num = int(ans[0][-4:])
        for i in range(res * 60 - 2):
            await asyncio.sleep(1)
            if solved:
                break
         
        answer = accmi(ans[2], username) if not solved else True
        if answer:
            rating(username)
            await message.reply('Qoyil. Yaxshi bajardingiz!!!')
        else:
            await message.reply("Afsuski siz ulgurmadingiz!!!") 
    else:
        if not username:
            await message.answer(
                "Siz /login <your_username> qilib yuboring. Oshanda Siz ro'yhatdan otasiz.\n"
                "Misol uchun /login python_devopover."
            )
        else:
            await message.reply("Siz ro'yhatdan o'tmagansiz. Yani agar oldin ro'yhatdan otkan bolsangiz /sign_up <password> buyrug'i bilan ro'yhatdan o'tib oling. Agar hali ro'yhatdan o'tmagan bolsangiz /sign_in <attempt_number> orqali ro'yhatdan o'tib oling.")



@dp.message(Command(commands=["daily_top_10"]))
async def top(message: types.Message):
    if valid:
        ans = 'Natijalar:\n'
        top10 = daily_top_users()
        if top10[0] == False:
            await message.reply("Bugun hali hech kim masala ishlamadi!")
        else:
            idx = 1
            # print(ans)
            for i,j in top10[0].items():
                ans += f'{idx}. {i} = {j} ta\n'
                idx += 1
            
            await message.reply(ans)
    else:
        if not username:
            await message.answer(
                "Siz /login <your_username> qilib yuboring. Oshanda Siz ro'yhatdan otasiz.\n"
                "Misol uchun /login python_devopover."
            )
        else:
            await message.reply("Siz ro'yhatdan o'tmagansiz. Yani agar oldin ro'yhatdan otkan bolsangiz /sign_up <password> buyrug'i bilan ro'yhatdan o'tib oling. Agar hali ro'yhatdan o'tmagan bolsangiz /sign_in <attempt_number> orqali ro'yhatdan o'tib oling.")

@dp.message(Command(commands=["logout"]))
async def logo(message: types.Message):
    global valid
    global username
    if valid:
        await message.reply("Siz profilingizdan chiqdingiz!!!")
        valid = False
        username = None
    else:
        await message.reply("Siz hali ro'yhatdan o'tmagansiz!!!")

@dp.message(Command(commands=["other"]))
async def problemsss(message: types.Message):
    if valid:
        args = message.text
        args = args[7:]
        with open('user_problem.txt','w') as f:
            f.write(f'{username}: {args}')
        await message.reply("Yuborildi.")
    else:
        if not username:
            await message.answer(
                "Siz /login <your_username> qilib yuboring. Oshanda Siz ro'yhatdan otasiz.\n"
                "Misol uchun /login python_devopover."
            )
        else:
            await message.reply("Siz ro'yhatdan o'tmagansiz. Yani agar oldin ro'yhatdan otkan bolsangiz /sign_up <password> buyrug'i bilan ro'yhatdan o'tib oling. Agar hali ro'yhatdan o'tmagan bolsangiz /sign_in <attempt_number> orqali ro'yhatdan o'tib oling.")


@dp.message()
async def not_comonds(message: types.Message):
    await message.answer('Xato buyruqni ishlatdingiz!!!')




async def main():
    print("Bot ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
