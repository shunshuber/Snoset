import re
import requests
from time import sleep
from configparser import ConfigParser
from os import system, name
from threading import Thread, active_count
from re import search, compile
from urllib.parse import urlparse
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.error import BadRequest

ALLOWED_CHAT_ID = 6361610849
BOT_TOKEN = "6515384483:AAGdC30ewYRG6pdOcMJAt8NjK-lFtkh_DuY"

THREADS, channel, post = 0, '', ''

PROXIES_TYPES = ('http', 'socks4', 'socks5')
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
REGEX = compile(r"(?:^|\D)?((" + r"(?:[1-9]|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])"
                + r"\." + r"(?:\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])"
                + r"\." + r"(?:\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])"
                + r"\." + r"(?:\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])"
                + r"):" + (r"(?:\d|[1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{3}"
                           + r"|65[0-4]\d{2}|655[0-2]\d|6553[0-5])")
                + r")(?:\D|$)")
errors = open('errors.txt', 'a+')
cfg = ConfigParser(interpolation=None)
cfg.read("config.ini", encoding="utf-8")

http, socks4, socks5 = '', '', ''
try:
    http, socks4, socks5 = cfg["HTTP"], cfg["SOCKS4"], cfg["SOCKS5"]
except KeyError:
    print(' [ OUTPUT ] Error | config.ini not found!')
    sleep(3)
    exit()
http_proxies, socks4_proxies, socks5_proxies = [], [], []
proxy_errors, token_errors = 0, 0
time_out, real_views = 15, 0

def scrap(sources, _proxy_type):
    for source in sources:
        if source:
            try:
                response = requests.get(source, timeout=time_out)
            except Exception as e:
                errors.write(f'{e}\n')
            if tuple(REGEX.finditer(response.text)):
                for proxy in tuple(REGEX.finditer(response.text)):
                    if _proxy_type == 'http':
                        http_proxies.append(proxy.group(1))
                    elif _proxy_type == 'socks4':
                        socks4_proxies.append(proxy.group(1))
                    elif _proxy_type == 'socks5':
                        socks5_proxies.append(proxy.group(1))

def start_scrap():
    threads = []
    for i in (http_proxies, socks4_proxies, socks5_proxies):
        i.clear()
    for i in ((http.get("Sources").splitlines(), 'http'), (socks4.get("Sources").splitlines(), 'socks4'), (socks5.get("Sources").splitlines(), 'socks5')):
        thread = Thread(target=scrap, args=(i[0], i[1]))
        threads.append(thread)
        thread.start()
    for t in threads:
        t.join()

def get_token(proxy, proxy_type):
    try:
        session = requests.session()
        response = session.get(f'https://t.me/{channel}/{post}', params={'embed': '1', 'mode': 'tme'},
                               headers={
                                   'referer': f'https://t.me/{channel}/{post}', 'user-agent': USER_AGENT},
                               proxies={'http': f'{proxy_type}://{proxy}',
                                        'https': f'{proxy_type}://{proxy}'},
                               timeout=time_out)
        return search('data-view="([^"]+)', response.text).group(1), session
    except AttributeError:
        return 2
    except requests.exceptions.RequestException:
        1
    except Exception as e:
        return errors.write(f'{e}\n')

def send_view(token, session, proxy, proxy_type):
    try:
        cookies_dict = session.cookies.get_dict()
        response = session.get('https://t.me/v/', params={'views': str(token)}, cookies={
            'stel_dt': '-240', 'stel_web_auth': 'https%3A%2F%2Fweb.telegram.org%2Fz%2F',
            'stel_ssid': cookies_dict.get('stel_ssid', None), 'stel_on': cookies_dict.get('stel_on', None)},
            headers={'referer': f'https://t.me/{channel}/{post}?embed=1&mode=tme',
                     'user-agent': USER_AGENT, 'x-requested-with': 'XMLHttpRequest'},
            proxies={'http': f'{proxy_type}://{proxy}',
                     'https': f'{proxy_type}://{proxy}'},
            timeout=time_out)
        return True if (response.status_code == 200 and response.text == 'true') else False
    except requests.exceptions.RequestException:
        1
    except Exception:
        pass

def control(proxy, proxy_type):
    global proxy_errors, token_errors
    token_data = get_token(proxy, proxy_type)
    if token_data == 2:
        token_errors += 1
    elif token_data == 1:
        proxy_errors += 1
    elif token_data:
        send_data = send_view(token_data[0], token_data[1], proxy, proxy_type)
        if send_data == 1:
            proxy_errors += 1

def start_view():
    c, threads = 0, []
    start_scrap()
    for i in [http_proxies, socks4_proxies, socks5_proxies]:
        for j in i:
            thread = Thread(target=control, args=(j, PROXIES_TYPES[c]))
            threads.append(thread)
            while active_count() > THREADS:
                sleep(0.05)
            thread.start()
        c += 1
        sleep(2)
    for t in threads:
        t.join()

def start(update: Update, context: CallbackContext) -> None:
    global ALLOWED_CHAT_ID

    chat_id = update.message.chat_id
    user_input = update.message.text

    if ALLOWED_CHAT_ID is None:
        ALLOWED_CHAT_ID = chat_id
        update.message.reply_text("Привет! Сколько потоков вы хотите использовать для накрутки?")
    elif chat_id == ALLOWED_CHAT_ID:
        # Здесь остальной код функции start без изменений
        update.message.delete()  
        message = update.message.reply_text("Бот настроен для работы только с вами. Сколько потоков вы хотите использовать для накрутки?")
        context.user_data["asking_threads"] = True
        context.user_data["last_message_id"] = message.message_id  
    else:
        # Если чат с другим пользователем, игнорируем запрос
        update.message.reply_text("Этот бот настроен для работы только с определенным пользователем.")
        update.message.delete()

def is_valid_link(channel, post):
    try:
        response = requests.get(f'https://t.me/{channel}/{post}', timeout=time_out)
        return response.status_code == 200 and 'tgme_page_post' in response.text
    except Exception as e:
        print(f"Error checking link validity: {e}")
        return False
    

def handle_message(update: Update, context: CallbackContext) -> None:
    global THREADS, channel, post

    chat_id = update.message.chat_id
    user_input = update.message.text

    if context.user_data.get("asking_threads", False):
        try:
            THREADS = int(user_input)
            update.message.delete()
            context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data["last_message_id"], text="Принято! Теперь отправьте мне ссылку на сообщение, на которое хотите накрутить просмотры.")
            context.user_data["asking_threads"] = False
            context.user_data["asking_link"] = True
        except ValueError:
            # В случае ввода некорректного числа потоков, редактируем предыдущее сообщение
            context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data["last_message_id"], text="Пожалуйста, введите корректное число потоков.")
            update.message.delete()  # Удаляем сообщение пользователя
        except BadRequest as e:
            # Обработка ошибки BadRequest
            if "Message is not modified" not in str(e):
                try:
                    context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data["last_message_id"], text="Произошла ошибка. Пожалуйста, повторите попытку.")
                except BadRequest:
                    # В случае ошибки при редактировании сообщения, отправим новое
                    context.bot.send_message(chat_id=chat_id, text="Произошла ошибка. Пожалуйста, повторите попытку.")
                pass  # Добавленный блок для закрытия исключения SyntaxError
    elif context.user_data.get("asking_link", False):
        link = user_input
        match = re.match(r'https://t.me/([^/]+)/(\d+)', link)
        if match:
            channel, post = match.groups()
            if is_valid_link(channel, post):
                update.message.delete()  # Удаляем сообщение пользователя
                context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data["last_message_id"], text=f"Принято! Начинаю просмотры для {channel}/{post}. Использую {THREADS} потоков.\n\nДля ценителей скриптов - https://t.me/top1bots - сюда сливаю много софта, который попадает мне в руки")
                Thread(target=start_view).start()
                # Очищаем флаги после успешного ввода
                context.user_data["asking_threads"] = False
                context.user_data["asking_link"] = False
            else:
                # Неверная ссылка - удаляем сообщение пользователя
                context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data["last_message_id"], text="Указанная ссылка не является валидной. Пожалуйста, проверьте её корректность.\n\nВведите /start")
                update.message.delete()
        else:
            # Неверная ссылка - удаляем сообщение пользователя
            context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data["last_message_id"], text="Пожалуйста, укажите корректную ссылку на сообщение в формате 'https://t.me/канал/идентификатор'.\n\nВведите /start")
            update.message.delete()

        # Очищаем флаги после обработки ввода
        context.user_data["asking_threads"] = False
        context.user_data["asking_link"] = False

def main() -> None:
    updater = Updater(BOT_TOKEN)  # Замените на фактический токен вашего бота

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()