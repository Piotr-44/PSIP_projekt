import psycopg2 as pcg
import requests
from bs4 import BeautifulSoup
import folium

db_params = pcg.connect(
    user="postgres",
    password="Psip2023",
    host="localhost",
    database="postgres",
    port=5433
)

cursor = db_params.cursor()


#####################################


def add_user():
    name = input("Podaj imię:  ")
    nick = input("Podaj nick:  ")
    city = input("Podaj miasto:  ")
    posts = input("Podaj liczbę postów:  ")

    # Check if the user with the same nickname already exists
    check_query = f"SELECT * FROM public.tabela_psip WHERE nick = '{nick}';"
    cursor.execute(check_query)
    existing_user = cursor.fetchone()

    if existing_user:
        print("Taki nick już istnieje.")
        add_user()
    else:
        # Insert the new user
        insert_query = f"INSERT INTO public.tabela_psip(city, nick, name, posts) VALUES ('{city}', '{nick}', '{name}', '{posts}');"
        cursor.execute(insert_query)
        db_params.commit()
        print("Użytkownik dodany pomyślnie.")



#####################################


def remove_user():
    name = input("Podaj imię użytkownika do usunięcia  ")
    sql_query_1 = f" SELECT * FROM public.tabela_psip WHERE name='{name}';"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print('0: Usuń wszystkich użytkowników z bazy ')
    print(f'Znaleziono następujących użytkowników: ')

    for numer_uzytkownika, user_to_be_removed in enumerate(query_result):
        print(f'{numer_uzytkownika + 1}: {user_to_be_removed}')
    numer = int(input(f'Wybierz użytkownika do usunięcia: '))
    print(numer)
    if numer == 0:
        sql_query_2 = f"DELETE * FROM public.tabela_psip: "
        cursor.execute(sql_query_2)
        db_params.commit()
    else:
        sql_query_2 = f"DELETE FROM public.tabela_psip WHERE id='{query_result[numer-1][0]}';"
        cursor.execute(sql_query_2)
        db_params.commit()



#####################################



def update_user():
    nick_of_user = input('Podaj nick uzytkownika do modyfikacji ')
    sql_query_1 = f" SELECT * FROM public.tabela_psip WHERE nick =  '{nick_of_user}';"
    cursor.execute(sql_query_1)
    print('Znaleziono !!!')
    city = input('Podaj nową nazwę miasta: ').strip()
    nick = input('Podaj nowy nick: ').strip()
    name = input('Podaj nowe imię: ').strip()
    posts = int(input('Podaj nową liczbę postów: '))
    sql_query_2 = f"UPDATE public.tabela_psip SET city ='{city}', nick ='{nick}',name ='{name}',posts = '{posts}' WHERE nick = '{nick_of_user}';"
    cursor.execute(sql_query_2)
    db_params.commit()



#####################################



def show_users_from():
    sql_query_1 = f' SELECT * FROM public.tabela_psip'
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    for row in query_result:
        print(f'Twój znajomy {row[3]} mieszka w mieście {row[1]} i opublikował {row[4]} postów')




#####################################



def get_coordinates_of(city: str) -> list[float, float]:
    # pobranie współrzędnych z treści strony internetowej
    adres_URL = f'https://pl.wikipedia.org/wiki/{city}'

    response = requests.get(url=adres_URL)
    response_html = BeautifulSoup(response.text, 'html.parser')

    response_html_latitude = response_html.select('.latitude')[1].text
    response_html_latitude = float(response_html_latitude.replace(',', '.'))
    response_html_longitude = response_html.select('.longitude')[1].text
    response_html_longitude = float(response_html_longitude.replace(',', '.'))

    return [response_html_latitude, response_html_longitude]



#####################################



def get_map_one_user():
    city_name = input('Podaj miasto użytkownika: ')
    sql_query_1 = f" SELECT * FROM public.tabela_psip WHERE city ='{city_name}';"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print("W przypadku braku wygenerowanej mapy - zakończ program, aby wyświetlić wynik")
    map = folium.Map(
        location=get_coordinates_of(city_name),
        tiles="OpenStreetMap",
        zoom_start=14
    )
    for user in query_result:
        folium.Marker(
            location=get_coordinates_of(city_name),
            popup=f'Tu rządzi {user[3]}\n'f'Liczba postów: {user[4]} ').add_to(map)
    map.save(f'mapka_{user[1]}_{user[2]}.html')



#####################################



def get_map_of():
    map = folium.Map(location=[52.3,21.0], tiles="OpenStreetMap", zoom_start=7)
    sql_query_1 = f"SELECT * FROM public.tabela_psip;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    for user in query_result:
        folium.Marker(
            location=get_coordinates_of(city=user[1]),
            popup=f'Użytkownik: {user[3]} \n'f'Liczba postów {user[4]}').add_to(map)
    map.save(f'mapka.html')
    print("W przypadku braku wygenerowanej mapy - zakończ program, aby wyświetlić wynik")



#####################################



def gui() -> None:
    while True:
        print(f' MENU: \n'
              f'0: Zakończ program \n'
              f'1: Wyświetl użytkowników \n'
              f'2: Dodaj użytkownika \n'
              f'3: Usuń użytkownika \n'
              f'4: Modyfikuj użytkowników \n'
              f'5: Wygeneruj mapę z użytkownikiem \n'
              f'6: Wygeneruj mapę z użytkownikami'
              )

        menu_option = input('Podaj funkcję do wywołania ')
        print(f'Wybrano funkcję {menu_option}')

        match menu_option:
            case '0':
                print('Kończę pracę')
                break
            case '1':
                show_users_from()
            case '2':
                print('Dodaję użytkownika')
                add_user()
            case '3':
                print('Usuwam użytkownika')
                remove_user()
            case '4':
                print('Modyfikuję użytkownika')
                update_user()
            case '5':
                print('Rysuj mape z uzytkownikiem')
                get_map_one_user()
            case '6':
                print('Rysuję mapę z wszystkimi użytkownikami')
                get_map_of()




#####################################
#####################################



