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

    for numer_stacji, station_to_be_removed in enumerate(query_result, start=1):
        print(f'{numer_stacji}: {station_to_be_removed}')
    numer = int(input(f'Wybierz stację do usunięcia: '))
    print(numer)
    sql_query_2 = f"DELETE FROM public.stacje_pogotowia WHERE id='{query_result[numer - 1][0]}';"
    cursor.execute(sql_query_2)
    db_params.commit()
    print(f'Usunięto informacje dotyczące wybranej stacji')


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

    for numer_stacji, station_to_be_removed in enumerate(query_result, start=1):
        print(f'{numer_stacji}: {station_to_be_removed}')
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

    for numer_stacji, station_to_be_removed in enumerate(query_result, start=1):
        print(f'{numer_stacji}: {station_to_be_removed}')
    numer = int(input(f'Wybierz pracownika do modyfikacji: '))
    print(numer)
    name = input("Podaj imię:  ")
    surname = input("Podaj nazwisko:  ")
    location = input("Podaj adres pracownika (ulica nr budynku, kod pocztowy Miejscowość):  ")
    specialization = input("Podaj funkcję pracownika:  ")
    station_id = input("Podaj numer stacji, której podlega:  ")

    sql_query_2 = (
        f"UPDATE public.pracownicy SET imie ='{name}', nazwisko = '{surname}', lokalizacja = '{location}', funkcja = '{specialization}', id_stacji = '{station_id}' WHERE id ='{query_result[numer - 1][0]}';")
    cursor.execute(sql_query_2)
    db_params.commit()
    print(f'Zmieniono dane wybranego pracownika')


###########################################################

def remove_employee():
    sql_query_1 = f" SELECT * FROM public.pracownicy;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print(f'Znaleziono następujących pracowników: ')

    for numer_pracownika, employee_to_be_removed in enumerate(query_result, start=1):
        print(f'{numer_pracownika}: {employee_to_be_removed}')
    numer = int(input(f'Wybierz pracownika do usunięcia: '))
    print(numer)
    sql_query_2 = f"DELETE FROM public.pracownicy WHERE id='{query_result[numer - 1][0]}';"
    cursor.execute(sql_query_2)
    db_params.commit()
    print(f'Usunięto wybranego użytkownika')


###########################################################
########################## PRACOWNICY WYBRANEJ STACJI #################################

def add_new_employee_by_station():
    sql_query_1 = "SELECT id, nazwa, lokalizacja FROM public.stacje_pogotowia;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print("Znaleziono następujące stacje: ")
    for numer_stacji, stacja in enumerate(query_result, start=1):
        print(f'{numer_stacji}: {stacja[1]} - {stacja[2]}')

    numer = int(input("Wybierz numer stacji, dla której chcesz dodać pracownika: "))
    selected_station_id = query_result[numer - 1][0]  # ID wybranej stacji

    name = input("Podaj imię: ")
    surname = input("Podaj nazwisko: ")
    location = input("Podaj adres pracownika (ulica nr budynku, kod pocztowy Miejscowość): ")
    specialization = input("Podaj funkcję pracownika: ")

    insert_query = f"INSERT INTO public.pracownicy(imie, nazwisko, lokalizacja, funkcja, id_stacji) " \
                   f"VALUES ('{name}', '{surname}', '{location}', '{specialization}', " \
                   f"(SELECT id FROM public.stacje_pogotowia WHERE id = {selected_station_id}));"
    cursor.execute(insert_query)
    db_params.commit()
    print(f"Dodano informacje o pracowniku - {name} {surname} dla stacji o numerze {numer}.")


###########################################################
def show_employees_by_station():
    sql_query_1 = "SELECT id, nazwa, lokalizacja FROM public.stacje_pogotowia;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print("Znaleziono następujące stacje: ")
    for numer_stacji, stacja in enumerate(query_result, start=1):
        print(f'{numer_stacji}: {stacja[1]} - {stacja[2]}')

    numer = int(input("Wybierz numer stacji, dla której chcesz wyświetlić pracowników: "))
    selected_station_id = query_result[numer - 1][0]  # ID wybranej stacji

    # Zapytanie SQL do pobrania pracowników dla wybranej stacji
    sql_query_2 = f"SELECT imie, nazwisko, lokalizacja, funkcja " \
                  f"FROM public.pracownicy " \
                  f"WHERE id_stacji = {selected_station_id};"
    cursor.execute(sql_query_2)
    employees = cursor.fetchall()

    print(f"\nPracownicy dla stacji {query_result[numer - 1][1]}:")
    if employees:
        for indeks, employee in enumerate(employees, start=1):
            print(f'{indeks}: {employee[0]} {employee[1]} - {employee[3]} ({employee[2]})')
    else:
        print("Brak pracowników dla wybranej stacji.")


###########################################################

def update_employees_by_station():
    sql_query_1 = "SELECT id, nazwa, lokalizacja FROM public.stacje_pogotowia;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print("Znaleziono następujące stacje: ")
    for numer_stacji, stacja in enumerate(query_result, start=1):
        print(f'{numer_stacji}: {stacja[1]} - {stacja[2]}')

    numer = int(input("Wybierz numer stacji, dla której chcesz aktualizować dane pracowników: "))
    selected_station_id = query_result[numer - 1][0]  # ID wybranej stacji

    # Zapytanie SQL do pobrania pracowników dla wybranej stacji
    sql_query_2 = f"SELECT id, imie, nazwisko, lokalizacja, funkcja " \
                  f"FROM public.pracownicy " \
                  f"WHERE id_stacji = {selected_station_id};"
    cursor.execute(sql_query_2)
    employees = cursor.fetchall()

    if employees:
        print(f"\nPracownicy dla stacji {query_result[numer - 1][1]} - {query_result[numer - 1][2]}:")
        for indeks, employee in enumerate(employees, start=1):
            print(f'{indeks}: {employee[1]} {employee[2]} - {employee[4]} ({employee[3]})')

        employee_id = int(input("\nWybierz numer pracownika, którego dane chcesz zaktualizować: "))
        if 1 <= employee_id <= len(employees):
            new_name = input("Podaj nowe imię: ")
            new_surname = input("Podaj nowe nazwisko: ")
            new_location = input("Podaj nowy adres pracownika (ulica nr budynku, kod pocztowy Miejscowość): ")
            new_specialization = input("Podaj nową funkcję pracownika: ")

            update_query = f"UPDATE public.pracownicy " \
                           f"SET imie = '{new_name}', " \
                           f"nazwisko = '{new_surname}', " \
                           f"lokalizacja = '{new_location}', " \
                           f"funkcja = '{new_specialization}' " \
                           f"WHERE id = {employees[employee_id - 1][0]};"
            cursor.execute(update_query)
            db_params.commit()
            print("Dane pracownika zaktualizowane pomyślnie.")
        else:
            print("Podano niepoprawny numer pracownika.")
    else:
        print("Brak pracowników dla wybranej stacji.")

# update_employees_by_station()

##########################################################

def delete_employees_by_station():
    sql_query_1 = "SELECT id, nazwa, lokalizacja FROM public.stacje_pogotowia;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print("Znaleziono następujące stacje: ")
    for numer_stacji, stacja in enumerate(query_result, start=1):
        print(f'{numer_stacji}: {stacja[1]} - {stacja[2]}')

    numer = int(input("Wybierz numer stacji, dla której chcesz usunąć pracowników: "))
    selected_station_id = query_result[numer - 1][0]  # ID wybranej stacji

    # Zapytanie SQL do pobrania pracowników dla wybranej stacji
    sql_query_2 = f"SELECT id, imie, nazwisko, lokalizacja, funkcja " \
                  f"FROM public.pracownicy " \
                  f"WHERE id_stacji = {selected_station_id};"
    cursor.execute(sql_query_2)
    employees = cursor.fetchall()

    if employees:
        print(f"\nPracownicy dla stacji {query_result[numer - 1][1]}:")
        for indeks, employee in enumerate(employees, start=1):
            print(f'{indeks}: {employee[1]} {employee[2]} - {employee[4]} ({employee[3]})')

        employee_id = int(input("\nWybierz numer pracownika, którego chcesz usunąć: "))
        if 1 <= employee_id <= len(employees):
            delete_query = f"DELETE FROM public.pracownicy WHERE id = {employees[employee_id-1][0]};"
            cursor.execute(delete_query)
            db_params.commit()
            print("Pracownik został pomyślnie usunięty.")
        else:
            print("Podano niepoprawny numer pracownika.")
    else:
        print("Brak pracowników dla wybranej stacji.")

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

    for numer_pacjenta, call_to_be_removed in enumerate(query_result, start=1):
        print(f'{numer_pacjenta}: {call_to_be_removed}')
    numer = int(input(f'Wybierz pacjenta do modyfikacji: '))
    print(numer)
    name = input("Podaj imię pacjenta:  ")
    surname = input("Podaj nazwisko pacjenta:  ")
    location = input("Podaj adres pacjenta (ulica nr budynku, kod pocztowy Miejscowość):  ")
    incident = input("Podaj rodzaj incydentu:  ")
    station_id = input("Podaj numer stacji, której pacjent podlega:  ")

    sql_query_2 = (
        f"UPDATE public.pacjenci SET imie ='{name}', nazwisko = '{surname}', lokalizacja = '{location}', incydent = '{incident}', id_stacji = '{station_id}' WHERE id ='{query_result[numer - 1][0]}';")
    cursor.execute(sql_query_2)
    db_params.commit()
    print(f'Zmieniono informacje o wezwaniu wybranego pacjenta')


###########################################################

def remove_call():
    sql_query_1 = f" SELECT * FROM public.pacjenci;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print(f'Znaleziono następujące wezwania pacjentów: ')

    for numer_pacjenta, call_to_be_removed in enumerate(query_result, start=1):
        print(f'{numer_pacjenta}: {call_to_be_removed}')
    numer = int(input(f'Wybierz wezwanie do usunięcia: '))
    print(numer)
    sql_query_2 = f"DELETE FROM public.pacjenci WHERE id='{query_result[numer - 1][0]}';"
    cursor.execute(sql_query_2)
    db_params.commit()
    print(f'Usunięto informacje dotyczące wybranego wezwania')


###########################################################
########################## INCYDENTY WYBRANEJ STACJI #################################

def add_new_call_by_station():
    sql_query_1 = "SELECT id, nazwa, lokalizacja FROM public.stacje_pogotowia;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print("Znaleziono następujące stacje: ")
    for numer_stacji, stacja in enumerate(query_result, start=1):
        print(f'{numer_stacji}: {stacja[1]} - {stacja[2]}')

    numer = int(input("Wybierz numer stacji, dla której chcesz dodać incydent: "))
    selected_station_id = query_result[numer - 1][0]  # ID wybranej stacji

    name = input("Podaj imię pacjenta:  ")
    surname = input("Podaj nazwisko pacjenta:  ")
    location = input("Podaj adres pacjenta (ulica nr budynku, kod pocztowy Miejscowość):  ")
    incident = input("Podaj rodzaj incydentu:  ")

    insert_query = f"INSERT INTO public.pacjenci(imie, nazwisko, lokalizacja, incydent, id_stacji) " \
                   f"VALUES ('{name}', '{surname}', '{location}', '{incident}', " \
                   f"(SELECT id FROM public.stacje_pogotowia WHERE id = {selected_station_id}));"
    cursor.execute(insert_query)
    db_params.commit()
    print(f"Dodano informacje o wezwaniu osoby - {name} {surname} dla stacji o numerze {numer}.")


###########################################################

