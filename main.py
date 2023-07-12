import re
import csv

raw_file_name = "phonebook_raw.csv"
transform_file_name = "phonebook.csv"


# Читаем адресную книгу в формате CSV в список contacts_list:

def read_file(name):
    with open(name, encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        return contacts_list


# Проверка длины строки (убираем лишние колонки)
def length_check(contacts_list):
    for row in contacts_list:
        while len(row) > 7:
            row.pop()


# Ставим ФИО на свои места

def group_names(contacts_list):
    for i, val in enumerate(contacts_list[1:], start=1):
        full_name_list = ' '.join(val[:3]).strip().split()
        while len(full_name_list) < 3:
            full_name_list.append('')
        contacts_list[i][:3] = full_name_list


# Преобразуем номера телефонов
def phones_transformation(contacts_list):
    for row in contacts_list:
        for i, el in enumerate(row):
            pattern = r"(\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(\s\(?доб.\s)?(\d+)?\)?"
            pattern_repl_1 = r"+7(\2)\3-\4-\5"
            pattern_repl_2 = r"+7(\2)\3-\4-\5 доб.\7"
            phone = re.findall(pattern, el)
            if phone:
                if phone[0][-1] == '':
                    repl_res = re.sub(pattern, pattern_repl_1, el)
                else:
                    repl_res = re.sub(pattern, pattern_repl_2, el)
                row[i] = repl_res


# Делаем новый список без дублей

def join_repeats(contacts_list):
    contacts_list_copy = contacts_list.copy()

    good_list = []

    # Сравниваем список контактов с его копией, формируем новый хороший список

    for row_copy in contacts_list_copy:
        flag = False                            # флаг = Ложь, когда строки с контактом еще нет
        for row in contacts_list:
            if row[0] == row_copy[0] and row[1] == row_copy[1] and \
                    (row[2] == row_copy[2] or row[2] == '' or row_copy[2] == ''):
                if flag is False:               # совпали ФИО, но записей в good_list еще нет
                    good_list.append(row)       # добавляем в хороший список первую запись
                    flag = True                 # выставляем флаг
                else:                           # совпали ФИО и такая запись уже есть
                    for i, el in enumerate(good_list[-1]):
                        if el == '':
                            good_list[-1][i] = row[i]       # заполняем пробелы новыми данными
                    contacts_list_copy.remove(row)          # удаляем из списка сравнения совпавшую запись
    return good_list


# Сохраняем получившиеся данные в другой файл.
def write_file(name, good_list):
    with open(name, "w", encoding='utf-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')

        datawriter.writerows(good_list)


def main():
    contacts_list = read_file(raw_file_name)

    # Исправляем перевод "отчество"

    contacts_list[0][2] = 'patronymic'

    length_check(contacts_list)
    group_names(contacts_list)
    phones_transformation(contacts_list)
    result = join_repeats(contacts_list)
    write_file(transform_file_name, result)


if __name__ == '__main__':
    main()
