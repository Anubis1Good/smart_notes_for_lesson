from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit, QListWidget, QLineEdit, QInputDialog
import json

notes = {
    "О планетах" : 
             {
                    "текст" : "Что если вода на Марсе это признак жизни?",
                    "теги" : ["Марс", "гипотезы"]
                },
    "О чёрных дырах" : 
             {
                    "текст" : "Сингулярность на горизонте событий отсутствует",
                    "теги" : ["чёрные дыры", "факты"]
                }
    }
def json_write():
    with open('notes_data.json','w',encoding='utf-8') as file:
        json.dump(notes, file)

json_write()

app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Умные заметки')
input_text = QTextEdit()
note_ll = QLabel('Список заметок')
list_notes = QListWidget()
create_note_btn = QPushButton('Создать заметку')
delete_note_btn = QPushButton('Удалить заметку')
save_note_btn = QPushButton('Сохранить заметку')
tag_ll = QLabel('Список тегов')
list_tags = QListWidget()
search_string = QLineEdit()
search_string.setPlaceholderText('Введите тег ...')
add_to_hote = QPushButton('Добавить к заметке')
uppin_to_note = QPushButton('Открепить от заметки')
search_by_tag = QPushButton('Искать заметки по тегу')

vlout1 = QVBoxLayout()
vlout1.addWidget(input_text)
vlout2 = QVBoxLayout()
vlout2.addWidget(note_ll,alignment=Qt.AlignmentFlag.AlignLeft)
vlout2.addWidget(list_notes)
vl2_hl1 = QHBoxLayout()
vl2_hl1.addWidget(create_note_btn)
vl2_hl1.addWidget(delete_note_btn)
vlout2.addLayout(vl2_hl1)
vlout2.addWidget(save_note_btn)
vlout2.addWidget(tag_ll,alignment=Qt.AlignmentFlag.AlignLeft)
vlout2.addWidget(list_tags)
vlout2.addWidget(search_string)
vl2_hl2 = QHBoxLayout()
vl2_hl2.addWidget(add_to_hote)
vl2_hl2.addWidget(uppin_to_note)
vlout2.addLayout(vl2_hl2)
vlout2.addWidget(search_by_tag)


main_layout = QHBoxLayout()
main_layout.addLayout(vlout1)
main_layout.addLayout(vlout2)


main_win.setLayout(main_layout)
main_win.show()

add_note_win = QWidget()

def update_json():
    json_write()
    list_notes.clear()
    json_load()


def show_note():
    name = list_notes.selectedItems()[0].text()
    input_text.setText(notes[name]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[name]["теги"])

def add_note():
    note_name, result = QInputDialog.getText(add_note_win,'Добавить заметку','Название заметки:')
    print(note_name)
    notes.update({note_name:{'текст':'','теги':[]}})
    update_json()

def del_note():
    name = list_notes.selectedItems()[0].text()
    notes.pop(name)
    update_json()

def save_note():
    name = list_notes.selectedItems()[0].text()
    notes[name]['текст'] = input_text.toPlainText()
    update_json()


def search_note():
    tag = search_string.text()
    if search_by_tag.text() == 'Искать заметки по тегу' and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note] = notes[note]
        search_by_tag.setText('Сбросить поиск')
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif search_by_tag.text() == 'Сбросить поиск':
        search_string.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        search_by_tag.setText('Искать заметки по тегу')
    else:
        pass

list_notes.itemClicked.connect(show_note)
create_note_btn.clicked.connect(add_note)
delete_note_btn.clicked.connect(del_note)
save_note_btn.clicked.connect(save_note)
search_by_tag.clicked.connect(search_note)

def json_load():
    with open('notes_data.json','r') as file:
        notes = json.load(file)
        # list_notes.addItems(data.keys())
        for note in notes:
            list_notes.addItem(note)
    
json_load()  


app.exec_()