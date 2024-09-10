import os
import asyncio
import instaloader
from aiogram import Bot, Dispatcher, types
from aiogram import html

# Instaloader sozlamalari
loader = instaloader.Instaloader()
username = 'Abduvohid_2629'
password = '20042629'
try:
    loader.login(username, password)
except Exception as e:
    print(f"Login xatolik: {e}")

# Bot sozlamalari
token = '7006912627:AAEpuTvYmUoZpdR56zIN4x0kufLhYO-a2_A'
bot = Bot(token=token)
dp = Dispatcher()

@dp.message()
async def handle_instagram_video(message: types.Message):
    link = message.text
    user_id = message.from_user.id
    loading_message = await bot.send_message(
        chat_id=user_id,
        text='📹 Video serverdan yuklanmoqda\nIltimos biroz kuting !'
    )

    try:
        shortcode = link.split('/')[4]
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        download_folder = f"{shortcode}"

        os.makedirs(download_folder, exist_ok=True)

        if post.is_video:
            loader.download_post(post, target=download_folder)

            video_path = None
            for file in os.listdir(download_folder):
                if file.endswith(".mp4"):
                    video_path = os.path.join(download_folder, file)

            if video_path and os.path.exists(video_path):
                video = types.input_file.FSInputFile(video_path)

                progress_message = await bot.send_message(chat_id=user_id, text='Yuklanmoqda...')
                await loading_message.delete()

                for i in range(1, 11):
                    percent = i * 10
                    progress_bar = '⬛️' * i + '⬜️' * (10 - i)
                    await progress_message.edit_text(text=f'{progress_bar}\n{percent}% yuklandi')
                    await asyncio.sleep(0.1)

                await progress_message.delete()

                await bot.send_video(
                    chat_id=user_id,
                    video=video,
                )

                final_message = await message.answer('Tayyor')
                await message.delete()
                await asyncio.sleep(0.5)
                await final_message.delete()

                for file in os.listdir(download_folder):
                    os.remove(os.path.join(download_folder, file))
                os.rmdir(download_folder)
            else:
                await message.answer(text='Video yuklashda xato yuz berdi.')

        else:
            await bot.send_message(chat_id=user_id, text="Bu URL video emas, iltimos video URL kiriting.")

    except Exception as e:
        await bot.send_message(chat_id=user_id, text=f"Xatolik yuz berdi: {e}")
        print(e)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
