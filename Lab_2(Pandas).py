
import pandas as pd
import matplotlib.pyplot as plt

# Эпизод 1
# В ваши руки попали данные о платежах некоторой глубоко законспирированной организации -
# вот они. Судя по всему, поля в данных следует воспринимать предельно просто: CONTRACTOR -
# кому платёж, STATUS - статус операции, SUM - сумма операции.
# Давайте попробуем посмотреть, что есть в этих данных.

df1 = pd.read_csv(r"C:\PythonLearn\transactions.csv")

print("\n========== ЭПИЗОД 1 ==========")
print("\nИсходные данные:")
print(df1)

# 1: найдите 3 самых крупных платежа из реально проведённых (статус OK).

target1 = df1.loc[df1['STATUS'] == 'OK', ['CONTRACTOR', 'SUM']]
target1 = target1.nlargest(3, 'SUM')

print("\n1. Три самых крупных проведённых платежа:")
print(target1)

# 2: определите полную сумму реально проведённых платежей в адрес Umbrella, Inc.

target2 = df1.loc[
    (df1['STATUS'] == 'OK') & (df1['CONTRACTOR'] == 'Umbrella, Inc'),
    'SUM'
]

print("\n2. Полная сумма проведённых платежей в адрес Umbrella, Inc:")
print(target2.sum())


# Эпизод 2
# У вас есть набор данных о грузовых рейсах - вот он. Поля в данных:
# CARGO - авиакомпания, PRICE - стоимость груза на борту, WEIGHT -
# масса груза на борту.
#
# Задача: посчитайте, сколько рейсов выполнила каждая авиакомпания,
# полную стоимость и полную массу перевезённых ей грузов. Постройте
# график уместного вида с результатами.

df2 = pd.read_csv(r"C:\PythonLearn\flights.csv")

print("\n========== ЭПИЗОД 2 ==========")
print("\nИсходные данные:")
print(df2)

number_of_flights = df2.groupby('CARGO').size()
print("\n1. Количество рейсов каждой авиакомпании:")
print(number_of_flights)

total_price = df2.groupby('CARGO')['PRICE'].sum()
print("\n2. Полная стоимость грузов каждой авиакомпании:")
print(total_price)

total_weight = df2.groupby('CARGO')['WEIGHT'].sum()
print("\n3. Полная масса грузов каждой авиакомпании:")
print(total_weight)

# Построение графика

plt.figure(figsize=(10, 6))

plt.subplot(1, 3, 1)
number_of_flights.plot(kind='bar')
plt.title('Number of Flights')
plt.xlabel('Airline')
plt.ylabel('Count')

plt.subplot(1, 3, 2)
total_price.plot(kind='bar')
plt.title('Total Price')
plt.xlabel('Airline')
plt.ylabel('Sum')

plt.subplot(1, 3, 3)
total_weight.plot(kind='bar')
plt.title('Total Weight')
plt.xlabel('Airline')
plt.ylabel('Sum')

plt.tight_layout()
plt.show()


# Эпизод 3
# Однажды один факультет 1-го сентября 1-го курса писал входное тестирование по информатике.
# Вот здесь лежит архив с данными. В архиве xlsx с данными групп от деканата и html-ная таблица
# результатов из ejudge. (Данные почти настоящие - в жизни они более сумбурные и грязные, двумя
# файликами дело не ограничивается.)
#
# В xlsx-файле логины студентов (поле login), номера их факультетских групп (поле group_faculty),
# номера их групп после распределения на группы по информатике (поле group_out). Как воспринимать
# таблицу результатов ejudge, наверное, отдельно рассказывать не надо. Скажем только, что в ней по
# счастью используются те же логины (а не ФИО с опечатками).

df3 = pd.read_excel(r"C:\PythonLearn\students_info.xlsx")
df4 = pd.read_html(r"C:\PythonLearn\results_ejudge.html")[0]

print("\n========== ЭПИЗОД 3 ==========")
print("\nТаблица студентов:")
print(df3)

print("\nТаблица результатов тестирования:")
print(df4)

df_merged = pd.merge(
    df3,
    df4,
    left_on='login',
    right_on='User',
    how='inner'
)

print("\nОбъединённая таблица:")
print(df_merged)

# Задача #1: постройте графики среднего количества решённых задач (а) по факультетским группам,
# (б) по группам по информатике. Формат графика - любой достаточно наглядный.

print("\n1. Среднее количество решённых задач по факультетским группам:")
MeanSolvedByFaculty = df_merged.groupby('group_faculty')['Solved'].mean()
print(MeanSolvedByFaculty)

print("\nСреднее количество решённых задач по группам информатики:")
MeanSolvedByGroup = df_merged.groupby('group_out')['Solved'].mean()
print(MeanSolvedByGroup)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
MeanSolvedByFaculty.plot(kind='bar')
plt.title('Mean Solved by Faculty Group')
plt.xlabel('Faculty Group')
plt.ylabel('Average Solved')

plt.subplot(1, 2, 2)
MeanSolvedByGroup.plot(kind='bar')
plt.title('Mean Solved by Informatics Group')
plt.xlabel('Informatics Group')
plt.ylabel('Average Solved')

plt.tight_layout()
plt.show()


# Задача #2: определите, из каких факультетских групп пришли и в какие группы по информатике
# попали люди, которые смогли пройти более одного теста в хотя бы одной из двух последних задач.
# (Задачи G и H в таблице, каждый тест даёт 10 баллов.) Рисовать график не обязательно, можно просто
# цифры посчитать.

print("\n2. Студенты, прошедшие более одного теста хотя бы в одной из задач G или H:")

successful = df_merged[(df_merged['G'] > 10) | (df_merged['H'] > 10)]

print(successful[['User', 'group_faculty', 'group_out', 'G', 'H']])

print("\nКоличество таких студентов по факультетским группам:")
print(successful.groupby('group_faculty')['User'].count())

print("\nКоличество таких студентов по группам информатики:")
print(successful.groupby('group_out')['User'].count())

print("\nРаспределение студентов одновременно по факультетским группам и группам информатики:")
print(successful.groupby(['group_faculty', 'group_out'])['User'].count())


# Дополнительное задание - найдите лёгкие проблемы и нестыковки в исходных данных.
# Они не мешают решить две поставленные задачи, но они там есть.

print("\n3. Проверка исходных данных на проблемы и нестыковки:")

print("\nСтуденты без логина в таблице Excel:")
print(df3[df3['login'].isna()])

print("\nЛогины из ejudge, которых нет в таблице Excel:")
missing_students = df4[~df4['User'].isin(df3['login'])]
print(missing_students[['User', 'Solved', 'Score']])

print("\nСтуденты из Excel, которых нет в таблице ejudge:")
no_results = df3[~df3['login'].isin(df4['User'])]
print(no_results)

print("\nПроверка завершена.")
