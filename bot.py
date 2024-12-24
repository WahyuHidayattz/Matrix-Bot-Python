from function import solve_matrix_obe_with_multipliers
import telebot
from telebot.types import ForceReply
from dotenv import load_dotenv
import os

load_dotenv()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
group_id = os.getenv("GROUP_ID")
user_states = {}
STATE_WAITING_MATRIX_INPUT = "waiting_matrix_input"

@bot.message_handler(commands=['start'])
def command_start(message):
    chat_id = message.chat.id
    first_name = message.chat.first_name
    last_name = message.chat.last_name or ""
    full_name = first_name + " " + last_name
    text = f"Hai {full_name}, selamat datang di Matrix Bot! Bot ini berfungsi untuk menyelesaikan soal matrix Gauss Jordan.\n"
    text += "Bot ini dibuat oleh Wahyu Hidayat @wahyu135\n\n"
    text += "Silahkan ketik command berikut :\n"
    text += "/gauss_jordan untuk menyelesaikan soal matrix Gauss Jordan\n"
    bot.send_message(chat_id=message.chat.id, text=text)
    send_log(message)


@bot.message_handler(commands=['gauss_jordan'])
def command_gauss_jordan(message):
    chat_id = message.chat.id
    text = (
        "Silahkan masukkan matriks augmented Anda, contoh format input:\n"
        "`[[3, 2, 1, 22], [2, 3, 2, 28], [1, 1, 3, 22]]`\n\n"
        "Bot akan menyelesaikan sistem persamaan dengan metode Gauss Jordan."
    )
    bot.send_message(chat_id=chat_id, text=text, parse_mode="MARKDOWN")
    user_states[chat_id] = STATE_WAITING_MATRIX_INPUT
    send_log(message)


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == STATE_WAITING_MATRIX_INPUT)
def handle_matrix_input(message):
    chat_id = message.chat.id
    try:
        user_input = eval(message.text)
        if not isinstance(user_input, list) or not all(isinstance(row, list) for row in user_input):
            raise ValueError("Input bukan matriks valid!")
        hasil = solve_matrix_obe_with_multipliers(user_input)
        text = "Hasil dari persamaan matrix :\n\n"
        for i in hasil:
            text += i + "\n"
        bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        bot.send_message(chat_id=chat_id, text=f"Terjadi kesalahan: {str(e)}")
    finally:
        user_states.pop(chat_id, None)
    
    send_log(message)


def send_log(message):
    chat_id     = message.chat.id
    first_name  = message.chat.first_name
    last_name   = message.chat.last_name or ""
    full_name   = first_name + " " + last_name
    text = "Laporan BOT Matrix\n"
    text += f"Nama : {full_name}\n"
    text += f"Chat Id : {chat_id}\n"
    text += f"Text : \n{message.text}"
    bot.send_message(chat_id=group_id, text=text)


if __name__ == "__main__":
    print("Bot berjalan...")
    bot.infinity_polling()
