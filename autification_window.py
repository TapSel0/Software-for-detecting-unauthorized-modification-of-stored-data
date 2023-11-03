import PySimpleGUI as sg
from stribog_func import Str512


root_login = Str512(bytes("qwerty", encoding='utf8'))
root_password = Str512(bytes("qwerty", encoding='utf8'))
number_of_attempts = 3


layout = [
    [sg.Text('Логин'), sg.Push(), sg.Input(s=15)],
    [sg.Text('Пароль'), sg.Push(), sg.Input(s=15, password_char="*")],
    [sg.Push(), sg.Button('Войти')]
]


def authentication() -> bool:
    global number_of_attempts
    window = sg.Window('Аутентификация пользователя', layout)
    while True:
        event, values = window.read()
        if event == 'Войти':
            username = bytes(values[0], encoding='utf8')
            password = bytes(values[1], encoding='utf8')
            if Str512(username) == root_login and Str512(password) == root_password:
                window.close()
                return True
            else:
                number_of_attempts -= 1
                sg.popup('Неверный логин или пароль!')
                if number_of_attempts == 0:
                    sg.popup('Слишком много попыток!')
                    window.close()
                    return False

        if event == sg.WINDOW_CLOSED:
            window.close()
            return False
