import psycopg2

from config import config
from utils import get_companies, get_vacancies, create_db, save_data_to_db
from db_manager import DBManager


def main():
    # Получааем компании
    companies_data = get_companies()

    # Получаем вакансии
    vacancies_data = get_vacancies(companies_data)
    params = config()

    # Создаём базу данных
    # create_db( **params) # hh_info_bd,
    create_db("hh_info_db", **params)

    # Осуществляем подключение к базе данных
    conn = psycopg2.connect(dbname='hh_info_bd', **params) # vacancies_hh
    save_data_to_db(companies_data, vacancies_data, 'hh_info_bd', **params)
    conn.close()

    # Подключение к базе данных
    conn = psycopg2.connect(dbname='hh_info_bd', **params)

    # Работа DBManager
    db_m = DBManager(conn)

    print("""Введите ваш запрос:
          1 - Список всех компаний и количество вакансий у каждой компании
          2 - Cписок всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию          
          3 - Средняя зарплата по вакансиям
          4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям
          5 - Список всех вакансий, в названии которых содержатся ключевые слова""")

    user_input = input()
    if user_input == '1':
        companies_and_vacancies_count = db_m.get_companies_and_vacancies_count()
        print("Компании и количество доступных вакансий:")
        for company_name, vacancy_counter in companies_and_vacancies_count:
            print(f"{company_name}: {vacancy_counter}")
    elif user_input == '2':
        all_vacancies = db_m.get_all_vacancies()
        print("Все вакансии:")
        for vacancy in all_vacancies:
            company_name, vacancy_name, salary_min, salary_max, vacancy_url = vacancy
            print(f"Компания: {company_name}, Вакансия: {vacancy_name}, Зарплата: {salary_min}-{salary_max}, "
                  f"Ссылка на вакансию: {vacancy_url}")
    elif user_input == '3':
        avg_salary = db_m.get_avg_salary()
        print(f"Средняя зарплата по всем вакансиям: {avg_salary}")
    elif user_input == '4':
        higher_salary_vacancies = db_m.get_vacancies_with_higher_salary()
        print("Вакансии с зарплатой выше средней:")
        for vacancy in higher_salary_vacancies:
            company_name, vacancy_name, salary_min, salary_max, vacancy_url = vacancy
            print(f"Компания: {company_name}, Вакансия: {vacancy_name}, Зарплата: {salary_min}-{salary_max},"
                  f"Ссылка на вакансию: {vacancy_url}")
    elif user_input == '5':
        keyword = input("Введите ключевое слово для поиска вакансий: ")
        vacancies_with_keyword = db_m.get_vacancies_with_keyword(keyword)
        print(f"Все вакансии с ключевым словом '{keyword}':")
        for vacancy in vacancies_with_keyword:
            company_name, vacancy_name, salary_min, salary_max, vacancy_url = vacancy
            print(f"Компания: {company_name}, Вакансия: {vacancy_name}, Зарплата: {salary_min}-{salary_max},"
                  f"Ссылка на вакансию: {vacancy_url}")
    else:
        print("Некорректный ввод")

    db_m.__del__()
    conn.close()


if __name__ == '__main__':
    main()

# TODO: Заметки
## Дата: 19/07/2024