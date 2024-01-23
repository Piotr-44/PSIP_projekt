import psycopg2 as pcg
import requests
from bs4 import BeautifulSoup
import folium
from opencage.geocoder import OpenCageGeocode

db_params = pcg.connect(
    user="postgres",
    password="Psip2023",
    host="localhost",
    database="postgres",
    port=5433
)

cursor = db_params.cursor()

########### STACJE POGOTOWIA ###############
def add_med_station():
    station = input("Podaj nazwę stacji:  ")
    location = input("Podaj adres stacji (ulica nr budynku, kod pocztowy Miejscowość):  ")

    insert_query = f"INSERT INTO public.stacje_pogotowia(nazwa, lokalizacja) VALUES ('{station}', '{location}');"
    cursor.execute(insert_query)
    db_params.commit()
    print(f"Dodano informacje o stacji pogotowia - {station}.")
# add_med_station()

##########################################################

def remove_med_station():
    sql_query_1 = f" SELECT * FROM public.stacje_pogotowia;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print(f'Znaleziono następujące stacje: ')

    for numer_stacji, station_to_be_removed in enumerate(query_result):
        print(f'{numer_stacji + 1}: {station_to_be_removed}')
    numer = int(input(f'Wybierz stację do usunięcia: '))
    print(numer)
    sql_query_2 = f"DELETE FROM public.stacje_pogotowia WHERE id='{query_result[numer - 1][0]}';"
    cursor.execute(sql_query_2)
    db_params.commit()
    print(f'Usunięto informacje dotyczące wybranej stacji')

# remove_med_station()

##########################################################

def show_all_stations():
    sql_query_1 = f' SELECT * FROM public.stacje_pogotowia'
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    for row in query_result:
        print(f'{row[0]} - {row[1]}')
# show_all_stations()

############################################################

def update_station_name():
    sql_query_1 = f" SELECT * FROM public.stacje_pogotowia;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print(f'Znaleziono następujące stacje: ')

    for numer_stacji, station_to_be_removed in enumerate(query_result):
        print(f'{numer_stacji + 1}: {station_to_be_removed}')
    numer = int(input(f'Wybierz stację do modyfikacji: '))
    print(numer)
    station = input('Podaj nową nazwę stacji: ')
    sql_query_2 = (f"UPDATE public.stacje_pogotowia SET nazwa ='{station}' WHERE id ='{query_result[numer - 1][0]}';")
    cursor.execute(sql_query_2)
    db_params.commit()
    print(f'Zmieniono nazwę wybranej stacji')


###########################################################
############################ PRACOWNICY ###############################
def add_new_employee():
    name = input("Podaj imię:  ")
    surname = input("Podaj nazwisko:  ")
    location = input("Podaj adres pracownika (ulica nr budynku, kod pocztowy Miejscowość):  ")
    specialization = input("Podaj funkcję pracownika:  ")
    station_id = input("Podaj numer stacji, której podlega:  ")

    insert_query = f"INSERT INTO public.pracownicy(imie, nazwisko, lokalizacja, funkcja, id_stacji) VALUES ('{name}', '{surname}', '{location}', '{specialization}', '{station_id}');"
    cursor.execute(insert_query)
    db_params.commit()
    print(f"Dodano informacje o pracowniku - {name} {surname}.")


###########################################################

def show_all_employees():
    sql_query_1 = f' SELECT * FROM public.pracownicy'
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    for row in query_result:
        print(f'Nr pracownika: {row[0]} - {row[1]} {row[2]} ({row[4]}), adres: {row[3]}')


###########################################################

def update_employee():
    sql_query_1 = f" SELECT * FROM public.pracownicy;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print(f'Znaleziono następujących pracowników: ')

    for numer_stacji, station_to_be_removed in enumerate(query_result):
        print(f'{numer_stacji + 1}: {station_to_be_removed}')
    numer = int(input(f'Wybierz pracownika do modyfikacji: '))
    print(numer)
    name = input("Podaj imię:  ")
    surname = input("Podaj nazwisko:  ")
    location = input("Podaj adres pracownika (ulica nr budynku, kod pocztowy Miejscowość):  ")
    specialization = input("Podaj funkcję pracownika:  ")
    station_id = input("Podaj numer stacji, której podlega:  ")

    sql_query_2 = (f"UPDATE public.pracownicy SET imie ='{name}', nazwisko = '{surname}', lokalizacja = '{location}', funkcja = '{specialization}', id_stacji = '{station_id}' WHERE id ='{query_result[numer - 1][0]}';")
    cursor.execute(sql_query_2)
    db_params.commit()
    print(f'Zmieniono dane wybranego pracownika')

###########################################################

def remove_employee():
    sql_query_1 = f" SELECT * FROM public.stacje_pogotowia;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print(f'Znaleziono następujące stacje: ')

    for numer_pracownika, station_to_be_removed in enumerate(query_result):
        print(f'{numer_pracownika + 1}: {station_to_be_removed}')
    numer = int(input(f'Wybierz stację do usunięcia: '))
    print(numer)
    sql_query_2 = f"DELETE FROM public.stacje_pogotowia WHERE id='{query_result[numer - 1][0]}';"
    cursor.execute(sql_query_2)
    db_params.commit()
    print(f'Usunięto informacje dotyczące wybranej stacji')

###########################################################
########################## PRACOWNICY WYBRANEJ STACJI #################################
# def add_new_employee_by_station():
#     sql_query_1 = f"SELECT id, nazwa, lokalizacja FROM public.stacje_pogotowia;"
#     print (f'Znaleziono następujące stacje: ')
#
#     name = input("Podaj imię:  ")
#     surname = input("Podaj nazwisko:  ")
#     location = input("Podaj adres pracownika (ulica nr budynku, kod pocztowy Miejscowość):  ")
#     specialization = input("Podaj funkcję pracownika:  ")
#     station_id = input("Podaj numer stacji, której podlega:  ")
#
#     insert_query = f"INSERT INTO public.pracownicy_stacji(imie, nazwisko, lokalizacja, funkcja, id_stacji) VALUES ('{name}', '{surname}', '{location}', '{specialization}', '{station_id}');"
#     cursor.execute(insert_query)
#     db_params.commit()
#     print(f"Dodano informacje o pracowniku - {name} {surname}.")

# add_new_employee_by_station()


###########################################################
########################## WEZWANIA #################################

def add_new_call():
    name = input("Podaj imię pacjenta:  ")
    surname = input("Podaj nazwisko pacjenta:  ")
    location = input("Podaj adres pacjenta (ulica nr budynku, kod pocztowy Miejscowość):  ")
    incident = input("Podaj rodzaj incydentu:  ")
    station_id = input("Podaj numer stacji, której pacjent podlega:  ")

    insert_query = f"INSERT INTO public.pacjenci(imie, nazwisko, lokalizacja, incydent, id_stacji) VALUES ('{name}', '{surname}', '{location}', '{incident}', '{station_id}');"
    cursor.execute(insert_query)
    db_params.commit()
    print(f"Dodano informacje o wezwaniu pacjenta - {name} {surname}.")


###########################################################
def show_all_calls():
    sql_query_1 = f' SELECT * FROM public.pacjenci'
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    for row in query_result:
        print(f'Nr pacjenta: {row[0]} - {row[1]} {row[2]} ({row[4]}), adres: {row[3]}')


###########################################################

def update_call():
    sql_query_1 = f" SELECT * FROM public.pacjenci;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print(f'Znaleziono następujących pacjentów: ')

    for numer_pacjenta, station_to_be_removed in enumerate(query_result):
        print(f'{numer_pacjenta + 1}: {station_to_be_removed}')
    numer = int(input(f'Wybierz pacjenta do modyfikacji: '))
    print(numer)
    name = input("Podaj imię pacjenta:  ")
    surname = input("Podaj nazwisko pacjenta:  ")
    location = input("Podaj adres pacjenta (ulica nr budynku, kod pocztowy Miejscowość):  ")
    incident = input("Podaj rodzaj incydentu:  ")
    station_id = input("Podaj numer stacji, której pacjent podlega:  ")

    sql_query_2 = (f"UPDATE public.pacjenci SET imie ='{name}', nazwisko = '{surname}', lokalizacja = '{location}', incydent = '{incident}', id_stacji = '{station_id}' WHERE id ='{query_result[numer - 1][0]}';")
    cursor.execute(sql_query_2)
    db_params.commit()
    print(f'Zmieniono informacje o wezwaniu wybranego pacjenta')


###########################################################

def remove_call():
    sql_query_1 = f" SELECT * FROM public.pacjenci;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print(f'Znaleziono następujące wezwania pacjentów: ')

    for numer_pacjenta, station_to_be_removed in enumerate(query_result):
        print(f'{numer_pacjenta + 1}: {station_to_be_removed}')
    numer = int(input(f'Wybierz wezwanie do usunięcia: '))
    print(numer)
    sql_query_2 = f"DELETE FROM public.pacjenci WHERE id='{query_result[numer - 1][0]}';"
    cursor.execute(sql_query_2)
    db_params.commit()
    print(f'Usunięto informacje dotyczące wybranego wezwania')









# WSZYSCY PRACOWNICY
def show_all_employees():
    sql_query_1 = f' SELECT * FROM public.zabezpieczenie_medyczne'
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    for row in query_result:
        print(f'Ratownik -  {row[3]}, adres: {row[2]}')

# show_all_employees()

############################################################

def remove_all_employees():
    sql_query_1 = f'UPDATE public.zabezpieczenie_medyczne SET dane_ratownika = NULL WHERE id>0'
    cursor.execute(sql_query_1)
    db_params.commit()
    sql_query_2 = f' SELECT * FROM public.zabezpieczenie_medyczne'
    cursor.execute(sql_query_2)
    query_result = cursor.fetchall()
    for row in query_result:
        print(f'')

# remove_all_employees()