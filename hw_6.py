import re, shutil, os
from os import path

#  Это всё для перевода кирилицы на латиницу
CYRILLIC = ('а','б','в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 
                    'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'є', 'і', 'ї', 'ґ')
LATIN = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
TRANS = {}
for c, l in zip(CYRILLIC, LATIN):  
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

#   Создание папок для сортировки файлов
geral_dir = 'F:/Razbor/'
images_dir = 'images/'
documents_dir = 'documents/'
audio_dir = 'audio/'
video_dir = 'video/'
archives_dir = 'archives/'
others_dir = 'others/'
dont_tach = {f'{geral_dir}{images_dir}', f'{geral_dir}{documents_dir}', f'{geral_dir}{audio_dir}', \
            f'{geral_dir}{video_dir}', f'{geral_dir}{archives_dir}', f'{geral_dir}{others_dir}', }

#  Для сортировки файлов по папкам по типу расширения (  images, documents, archives, audio, video, others  )
images_set = {'.jpeg', '.png', '.jpg', '.svg'}
documents_set = {'.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'}
audio_set = {'.mp3', '.ogg', '.wav', '.amr'}
video_set = {'.avi', '.mp4', '.mov', '.mkv'}
archives_set = {'.zip', '.gz', '.tar'}

def create_dir(path):

    os.mkdir(f'{path}{images_dir}')      
    os.mkdir(f'{path}{documents_dir}')
    os.mkdir(f'{path}{audio_dir}')
    os.mkdir(f'{path}{video_dir}') 
    os.mkdir(f'{path}{archives_dir}')  
    os.mkdir(f'{path}{others_dir}') 

    return True


def normalize(name):        #  Приводим название файла в божеский вид

    name_tempo = ''
    name = name.translate(TRANS)
    for i in range(len(name)):
        if name[i].isalnum():
            name_tempo += name[i]
        else:
            name_tempo += '_'

    return name_tempo

def archiv_unp(path):       #   Разархивация zip файлов

    list_zip = os.listdir(path)
    for i in list_zip:
        dir_unpack_name = os.path.splitext(i)
        shutil.unpack_archive(f'{geral_dir}{archives_dir}{i}', f'{geral_dir}{archives_dir}{dir_unpack_name[0]}')

    return True

def del_empty_dir(path):        #   Удаление пустых папок

    list_dir = os.listdir(path)
    for i in list_dir:
        if f'{path}{i}/' not in dont_tach:
            shutil.rmtree(f'{path}{i}/')

    return True

def list_f_and_ext(path):       #   Получение списков файлов по папкам и множества расширений

    list_ext = []               #   Список всех расширений которые встретятся при сортировке   
    folder = []         
    a = os.walk(path)           #  Получаем всю инфу о папке Razbor
    for i in a:
        folder.append(i)
    for address, dirs, files in folder:
        for file in files:
            file_name = os.path.splitext(file)
            list_ext.append(file_name[1])

    return set(list_ext), folder

def sort_f(path):       #   Сортировка всех файлов по папкам в зависимости от расширения 
                        #   (  images, documents, archives, audio, video, others  )
    folder = []         
    a = os.walk(path)       #  Получаем всю инфу о папке Razbor
    for i in a:
        folder.append(i)

    for address, dirs, files in folder: #  Проход по именам файлов
        if f'{address}/' not in dont_tach:  #  Проверка чтобы не просматривать папки (  images, documents, archives, audio, video, others  )
            for file in files:
                file_name = os.path.splitext(file)  #  file_name list из 2-х эл-ов ( 1 - имя  2 - расширение)
                file_n_tempo = normalize(file_name[0])    #  Изголяемся над именем файла (без расширения)

                if file_name[1] in images_set:
                    os.replace(f'{address}\{file}', f'{path}{images_dir}{file_n_tempo}{file_name[1]}')
                elif file_name[1] in documents_set:
                    os.replace(f'{address}\{file}', f'{path}{documents_dir}{file_n_tempo}{file_name[1]}')
                elif file_name[1] in audio_set:
                    os.replace(f'{address}\{file}', f'{path}{audio_dir}{file_n_tempo}{file_name[1]}')
                elif file_name[1] in video_set:
                    os.replace(f'{address}\{file}', f'{path}{video_dir}{file_n_tempo}{file_name[1]}')
                elif file_name[1] in archives_set:
                    os.replace(f'{address}\{file}', f'{path}{archives_dir}{file_n_tempo}{file_name[1]}')
                else:
                    os.replace(f'{address}\{file}', f'{path}{others_dir}{file_n_tempo}{file_name[1]}')
    return True

create_dir(geral_dir)
print("  Создание папок для сортировки всех файлов прошла корректно ")
sort_f(geral_dir)                          #   Сортировка всех файлов по папкам в зависимости от расширения
print("  Сортировка всех файлов по соответствующим папкам прошла корректно ")
del_empty_dir(geral_dir)              #   Удаление пустых папок
print("  Удаление пустых папок прошло корректно ")
exp, fol = list_f_and_ext(geral_dir)       #   Получение списков файлов по папкам и множества расширений
print('  Список встреченных расширений : ')
print(exp)
print('  Список папок и находящихся в них файлов : ')
print(fol)
archiv_unp(f'{geral_dir}{archives_dir}')   #   Разархивация zip файлов
print("  Разархивация архивов прошло корректно ")

print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")