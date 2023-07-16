hello = (
    'Привет, {username}!\n\n'
    'Это бот для получения уведомлений о доступных проверках в БК. Бот будет присылать тебе новые доступные проверки, '
    'как только они появятся. Тебе остаётся только зайти на сайт и записаться на проверку.\n\n'
    '/help - помощь\n'
    '/profile - ваш профиль с настройками\n'
    '/news - новости проекта'
)

help_text = (
    ''
)

news = (
    ''
)

profile = (
    'Ваш профиль БК\n\n'
    'Имя: {name}\n'
    'Телефон: {phone}\n'
    'Город: {city}\n\n'
    'Рестораны:'
    '{restaurants}\n\n'
    'Рассылка: {mailing}'
)

start = (
    'Для использования бота нужно войти в ваш аккаунт БК. Это безопасно, все ваши личные данные будут зашифрованы. '
    'Даже если данные взломают, самое плохое что можно сделать - записаться на проверку от вашего имени.\n\n'
    'На вашем аккаунте должна быть заполнена анкета тайного покупателя - '
    'нужно выбрать город, рестораны для проверки и заполнить личные данные. Проверки из выбранных ресторанов будут тебе приходить.\n\n'
    'Личный кабинет тайного покупателя можно открыть прямо в Telegram по кнопке "BurgerKing" слева от ввода сообщения '
    'или по такой же кнопке под сообщением. Когда всё сделаешь - нажми "Начать вход" под сообщением'
)

phone_input = (
    'Отправьте сообщением номер телефона в формате, начиная с "7", на него придёт СМС с кодом'
)

code_input = (
    'Код отправлен на номер {phone}.\n\nОтправьте сообщением код из СМС'
)

something_went_wrong_with_api = (
    'Что-то пошло нет...\n\n'
    'Повторите попытку позже - /start'
)

bad_phone = (
    'Неверный телефон! Сообщение об ошибке: {error}\n\n'
    'Отправьте телефон ещё раз'
)

bad_code = (
    'Неверный код! Сообщение об ошибке: {error}\n\n'
    'Отправьте код ещё раз'
)

unlogin = (
    'На ваш аккаунт БК зашли с другого аккаунта Telegram, ботом можно пользоваться только с одного аккаунта Telegram.\n\n'
    'Если нужно, повторите вход - /start'
)

new_check = (
    'Новая проверка в ресторане {address}!\n\n'
    'Дата: {date}\n'
    'Время:\n'
    '{times}'
)


