from pprint import pprint
from PyQt5.QtWidgets import *


import json 

def show_note():
    name = list_of_notes.selectedItems()[0].text()
    notes.setText(data[name]['текст'])
    list_of_tags.clear()
    list_of_tags.addItems(data[name]['теги'])


def save_note():
    note = list_of_notes.selectedItems()
    if notes:
        name = note[0].text()
        data[name]['текст'] = notes.toPlainText()
        with open('notes.json','w',encoding='UTF-8') as file:
            json.dump(data, file)


def delete_note():
    note = list_of_notes.selectedItems()
    if notes:
        name = note[0].text()
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
        json.dump(data, file)

with open('notes.json','r',encoding='UTF-8') as file:
    data = json.load(file)
    pprint(data)



app = QApplication([])
window = QWidget()
window.setWindowTitle('Умные заметки')
window.resize(800, 600)

notes = QTextEdit()

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
b_find_note = QPushButton('Искать заметки по тегу')

line = QHBoxLayout()
line1 = QVBoxLayout()
h_line1 = QHBoxLayout()
h_line2 = QHBoxLayout()

line.addWidget(notes)
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
line1.addWidget(b_find_note)

window.setLayout(line)
list_of_notes.addItems(data)
window.show()
app.exec()

