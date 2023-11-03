import PySimpleGUI as sg


def create_window():
    # GUI
    # Разметка окна
    menu = sg.Menu
    sg.theme("DarkBlue12")
    layout_down = [
        [sg.Output(key="Output", s=(20, 20), expand_y=True, expand_x=True)]]
    layout_top = [
        [sg.T('Путь к отслеживаемому файлу/папке'), sg.Push(), sg.InputText(key="tracked_file")],
        [sg.T('Путь для записи выходных данных ПО'), sg.Push(), sg.InputText(key="recording_path")],
        [sg.Checkbox('Стрибог (ГОСТ Р 34.11-2012)'), sg.Checkbox('ГОСТ Р 34.11-94'), sg.Checkbox('MD5'),
         sg.Checkbox('SHA1'), sg.Checkbox('SHA256')]]
    layout = [
        [menu([['Файл', ['Сменить папку записи данных', 'Сохранить и выйти']],
               ['Действия', ['Начать отслеживание изменений по выбранному пути']],
               ['Хеш', ['Сохранить хеши файлов по выбранному пути', 'Провести сравнение файлов с помощью хеш-функций']]], p=0)],
        [sg.Pane([sg.Col(layout_top, vertical_alignment="top"), sg.Col(layout_down, p=0)], expand_x=True, expand_y=True,
                 border_width=0)]
    ]
    window = sg.Window('ПО для ВНМХД', layout, use_default_focus=False, finalize=True, resizable=True)
    return window
