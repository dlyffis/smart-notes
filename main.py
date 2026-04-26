from pprint import pprint #PRETTY PRINT
from PyQt5.QtWidgets import *
import json 

def show_note():
    name = list_of_notes.selectedItems()[0].text()
    note_text.setText(data[name]['текст'])
    list_of_tags.clear()
    list_of_tags.addItems(data[name]['теги'])


def save_note():
    notes = list_of_notes.selectedItems()
    if notes:
        name = notes[0].text()
        data[name]['текст'] = notes.toPlainText()
        with open('notes.json','w',encoding='UTF-8') as file:
            json.dump(data, file)


def delete_note():
    notes = list_of_notes.selectedItems()
    if notes:
        name = notes[0].text()
        data.pop(name)
        with open('notes.json','w',encoding='UTF-8') as file:
            json.dump(data, file)
        list_of_notes.clear()
        list_of_notes.addItems(data)


def create_note():
    name, ok = QInputDialog.getText(window, 'Добавить заметку', 'Название заметки:')
    if ok and name != '':
        data[name] = {'текст': '', 'теги': []}
        list_of_notes.addItem(name)


def add_tag():
    notes = list_of_notes.selectedItems()
    if notes:
        name = notes[0].text()
        tag = tag_enter.text()
        if tag not in data[name]['теги']:
            data[name]['теги'].append(tag)
            list_of_tags.addItem(tag)
            tag_enter.clear()
            with open('notes.json','w',encoding='UTF-8') as file:
                json.dump(data, file)


def unpin_tag():
    notes = list_of_notes.selectedItems()
    if notes:
        name = notes[0].text()
        tag = tag_enter.text()
        if tag in data[name]['теги']:
            data[name]['теги'].remove(tag)
            list_of_tags.clear()
            list_of_tags.addItems(data[name]['теги'])
            with open('notes.json','w',encoding='UTF-8') as file:
                json.dump(data, file)
            tag_enter.clear()


def search_notes():
    tag = tag_enter.text() 
    notes = []
    for key, value in data.items(): #метод items возвращает ключи и значения
        if tag in value['теги']:
            notes.append(key)
    if notes:
        list_of_tags.clear()
        list_of_notes.clear()
        note_text.clear()
        list_of_notes.addItems(notes)
    

def reset_search():
    list_of_tags.clear()
    list_of_notes.clear()
    note_text.clear()
    list_of_notes.addItems(data)


def click():
    if b_search_notes.text() == 'Искать заметки по тегу':
        search_notes()
        b_search_notes.setText('Сбросить поиск')
    else:
        reset_search()
        b_search_notes.setText('Искать заметки по тегу')
    



if input('Переписать словарь?') == 'да':
    data = {
        'Расписание уроков': {
            'текст':'Понедельник\nалгебра, физика, химия',
            'теги':['Расписание','Школа']
        },
        'Покупки': {
            'текст':'Нужно купить:\n-Молоко \n-Хлеб',
            'теги':['Магазин','Покупки']
        }
    }
    with open('notes.json','w',encoding='UTF-8') as file:
        json.dump(data, file) #сохранить в файле данные всё

with open('notes.json','r',encoding='UTF-8') as file:
    data = json.load(file) #загрузить из файла в словарь
    pprint(data)



app = QApplication([])
window = QWidget()
window.setWindowTitle('Умные заметки')
window.resize(800, 600)

note_text = QTextEdit()

list_of_notes = QListWidget()
list_of_notes.itemClicked.connect(show_note)
note_label = QLabel('Список заметок')
b_make_notes = QPushButton('Создать заметку')
b_make_notes.clicked.connect(create_note)

b_delete_notes = QPushButton('Удалить заметку')
b_delete_notes.clicked.connect(delete_note)

b_save_notes = QPushButton('Сохранить заметку')
b_save_notes.clicked.connect(save_note)

list_of_tags = QListWidget()
tag_label = QLabel('Список тегов')
tag_enter = QLineEdit()
b_add_to_note = QPushButton('Добавить к заметке')
b_add_to_note.clicked.connect(add_tag)
b_pin_from_note = QPushButton('Открепить от заметки')
b_pin_from_note.clicked.connect(unpin_tag)
b_search_notes = QPushButton('Искать заметки по тегу')
b_search_notes.clicked.connect(click)
line = QHBoxLayout()
line1 = QVBoxLayout()
h_line1 = QHBoxLayout()
h_line2 = QHBoxLayout()

line.addWidget(note_text)
line.addLayout(line1)

h_line1.addWidget(b_make_notes)
h_line1.addWidget(b_delete_notes)

h_line2.addWidget(b_add_to_note)
h_line2.addWidget(b_pin_from_note)

line1.addWidget(note_label)
line1.addWidget(list_of_notes)
line1.addLayout(h_line1)
line1.addWidget(b_save_notes)

line1.addWidget(tag_label)
line1.addWidget(list_of_tags)
line1.addWidget(tag_enter)
line1.addLayout(h_line2)
line1.addWidget(b_search_notes)

window.setLayout(line)
list_of_notes.addItems(data)
window.show()
app.exec()
