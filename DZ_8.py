import random
from datetime import timedelta, datetime


def rand(N):    #  Генерация списка сотрудников через random в виде {"name":имя, "birthday":ДР}
                #  N - колличество сотрудников

    now = datetime.now()
    list_workers = []   #  Список имён сотрудников для основного скрипта
        #[{"name":"Bill", "birthday":"1998-02-08"},{"name":"Giil", "birthday":"1999-02-10"}]
        #   "name" - type < str >    "birthday" - type < str >

        #  Список имен сотрудников для random
    list_names = ["John", "Vasja", "Ali", "Brain", "Kolya", "Maria", "Vika", "Harold", "Yui", "Li"]
    age_max = 35*365+int(35/4)      #  Возраст 35 лет ( в днях )
    age_min = 18*365+int(18/4)      #  Возраст 18 лет ( в днях )
    age_zenz = age_max - age_min    #  Возрастной диапазон ( в днях )
    time_max = now - timedelta(days=age_max)    #  Начало отчёта для формирование списка работников  
    random.seed(10)

    for i in range(0, N):       #  Наполнение списка сотрудников в колличестве N человек
            bd = random.randint(0, age_zenz)
            birthday = time_max + timedelta(bd)
            name = random.randint(0, len(list_names)-1)
            list_workers.append({"name":list_names[name], "birthday":birthday.strftime("%Y-%m-%d")})

    return list_workers

def days(date):         #  Колличество дней с 1 января текущего года
    dfy = date - datetime(date.year, 1, 1)

    return dfy.days


def new_list(total_list):   #  Из глобального списка делает список на неделю вперёд от текущего момента

    time_start = datetime.now()
    time_fin = time_start + timedelta(days=7)
    new_list = []

    for i in total_list:
        time_user = datetime.strptime(i['birthday'], "%Y-%m-%d")
        
        if days(time_start) < days(time_user) < days(time_fin):
            t = datetime.strptime(i['birthday'], "%Y-%m-%d")
            s = t.strftime("%A")
            new_list.append({"name":i['name'], "birthday":s})

    return new_list


def print_birthdays(list_p):        #  Приводит к нужной форме список (согласно заданию) и распечатывает его

    LP = {'Monday':[], 'Tuesday':[], 'Wednesday':[], 'Thursday':[], 'Friday':[], 'Saturday':[], 'Sunday':[]}

    for i in list_p:
        LP[i["birthday"]].append(i["name"]) 
    print(f'Именинники на неделю : {LP} \n')

    LP['Monday'] += [i for i in LP['Saturday']]
    LP['Monday'] += [i for i in LP['Sunday']]
    LP['Saturday'] = []
    LP['Sunday'] = []   

    for i in LP.keys():
        if not LP[i] == []:
            str = f'{i}   \t: '
            for j in LP[i]:
                str += f'{j}, ' 
            print(str)
    print('\n')


def get_birthdays_per_week():           #  Наш скрипт по выведению Дней рождений на неделю
 
    users = rand(300)                   #  Генерация списка сотрудников через random в виде {"name":имя, "birthday":ДР}
    list_to_print = new_list(users)     #  Из глобального списка делает список на неделю вперёд от текущего момента
    print_birthdays(list_to_print)      #  Приводит к нужной форме список (согласно заданию) и распечатывает его

def main() -> None:

    print("=================   Script   ==============================\n")
    get_birthdays_per_week()
    print("===========================================================\n")



if __name__ == "__main__":
    main()