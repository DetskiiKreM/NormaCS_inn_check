'''
Данный скрипт предназначен для проверки ИНН на портале разработчика.
ИНН считываются построчно из файла to_check.txt, и после проверки результат построчно записывается в выходной файл
дата_время_inn.txt в формате: ИНН -  Результат проверки.
'''


import requests
from datetime import datetime
# import maskpass


current_datetime = str(datetime.now())
sess = requests.Session()
name = input('Введите логин и нажмите enter: ')
# password = maskpass.askpass(prompt='Введите пароль и нажмите enter: ')
password = input('Введите пароль и нажмите enter: ')

# Функция аутентификации на портале
def login(name, password):
    url = 'https://normacs.ru/Dealers/login.jsp?action=login'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        'j_username': name,
        'j_password': password
    }
    response = sess.post(url, data=payload, headers=headers)
    response.status_code
    return sess

# Функция проверки ИНН через форму на портале
def check_inn(sess,inn):
    resp = sess.get(f'https://normacs.ru/Dealers/innstatus.jsp?newprk&inn={inn}')
    print(f'{inn} - {resp.text}')
    print('*' * 100)
    result = resp.text
    message = result
    if result == '-1':
        message = "Ошибка выполнения запроса-проверки ИНН."
    elif result == '-2':
        message = "Неверное значение ИНН"
    elif result == '-3':
        message = "Ошибка выполнения запроса-проверки ИНН. Попробуйте позже."
    elif len(result) == 6:
        if result[0] == '0':
            message = "Резервирование и заказ временной лицензии по данному ИНН запрещены."
        elif result[0] == '1':
            message = "Резервирование и заказ временной лицензии по данному ИНН разрешены."
        elif result[0] == '2':
            message = "Резервирование по данному ИНН разрешено."
        elif result[0] not in ('0', '1', '2'):
            message = "Заказ временной лицензии по данному ИНН разрешен."

        if result[3] in ('2', '3', '6'):
            can_you = "выписать еще временную версию для тестирования других разделов, но технологическое" \
                      " резервирование запрещено, поскольку клиент зарегистрирован также и в Техэксперте," \
                      " для смены версии или работы"
        else:
            can_you = "закрепить его повторно для смены версии (или осуществления другой технологической операции)" \
                      " у этого же клиента. Если вы хотите начать работу"

        match result[1]:
            case '1':
                message += " Клиент уже является вашим РК, вы можете " + can_you + " с филиалом данной организации," \
                          " необходимо согласовать данную возможность, отправив запрос на prioritet@normacs.ru"
            case '2':
                message += " Клиент уже закреплен за вами. Можно выписать еще временную версию."
            case '3':
                message += " Клиент уже закреплен за вами и поставлен на контроль. Можно выписать еще временную версию."
            case '4':
                message += " Клиент уже закреплен за вами по допоставке. Можно выписать еще временную версию."
            case '5':
                message += " Клиент был закреплен за вами менее месяца назад. Действует мораторий на повторное " \
                          "закрепление."
            case '6':
                message += " Клиент уже является вашим РК, вы можете " + can_you + " с филиалом данной организации," \
                       " необходимо согласовать данную возможность, отправив запрос на prioritet@normacs.ru. " \
                       "Клиент уже закреплен за вами по допоставке."
            case '7':
                message += " Клиент еще является вашим РК, но период оплаченных обновлений уже закончился." \
                       " Вы можете " + can_you + " с филиалом данной организации, необходимо согласовать данную" \
                       " возможность, отправив запрос на prioritet@normacs.ru."

        match result[2]:
            case '1':
                message += " Клиент находится на обслуживании у другого дилера по NormаCS."
            case '2':
                message += " Клиент зарезервирован другим дилером по NormаCS."
            case '3':
                message += ' Клиент находится на на контроле АО "Нанософт" по NormаCS.'
            case '4':
                message += " Клиент закреплен за другим дилером по NormаCS по допоставке."
            case '5':
                message += " Клиент был закреплен за другим дилером по NormаCS менее месяца назад. " \
                           "Действует мораторий на повторное закрепление."
            case '6':
                message += " Клиент находится на обслуживании у другого дилера по NormаCS и закреплен " \
                           "за ним по допоставке."
            case '7':
                message += ' Клиент является пользователем nanoCAD, зарезервирован по NormаCS ООО' \
                           ' "Нанософт Разработка".'
        match result[3]:
            case '2':
                message += " Клиент обслуживается в Техэксперте."
            case '3':
                message += " Клиент закреплен в Техэксперте."
            case '4':
                message += " Особая ситуация. Отправьте запрос на prioritet@normacs.ru для уточнения статуса клиента."
            case '5':
                message += " ЕРГЮЛ сообщает, что организация по данному ИНН ликвидирована или не существует. " \
                           "Проверьте ИНН или отправьте запрос на prioritet@normacs.ru для уточнения статуса клиента."
            case '6':
                message += " Клиент был закреплен в Техэксперте менее месяца назад. Действует мораторий на " \
                           "повторное закрепление."

        if result[4] == '1':
            message += " Обратите внимание, это корпоративный клиент -  ценообразование будет строиться по рабочим " \
                       "местам и только по согласованию с координационным советом."

        if result[5] == '1':
            message += " Клиент из запрещенного региона."
    else:
        message = "Ошибка выполнения запроса-проверки ИНН!"
    return message


session = login(name, password)
inn = 0
# Создаем красивый формат имени выходного файла
date_time = current_datetime.replace('-', ' ').replace(':', ' ')
date_lst = date_time.split(' ', 5)
file_date = date_lst[2] + date_lst[1] + date_lst[0] + '_' + date_lst[3] + date_lst[4]
file_name = file_date + '_inn.txt'

# Построчно считываем ИНН и записываем результат проверки в новый файл
with open('to_check.txt', 'r', encoding='utf-8') as in_file:
    for line in in_file:
        inn = line.replace(' ', '').replace('\n', '')
        check = check_inn(sess, inn)
        with open(file_name, 'a', encoding='utf-8') as out_file:
            out_file.writelines(inn + ' - ' + check + '\n')

print(f'ИНН проверены, результат записан в файл {file_name}')
