import psycopg2 as pcg
import requests
import folium


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
        print(f'Nr stacji: {row[0]} - {row[1]}')


############################################################
def update_station():
    sql_query_1 = f" SELECT * FROM public.stacje_pogotowia;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print(f'Znaleziono następujące stacje: ')

    for numer_stacji, station_to_be_removed in enumerate(query_result, start=1):
        print(f'{numer_stacji}: {station_to_be_removed}')
    numer = int(input(f'Wybierz stację do modyfikacji: '))
    print(numer)
    station = input('Podaj nową nazwę stacji: ')
    location = input('Podaj nowy adres stacji (ulica nr budynku, kod pocztowy Miejscowość): ')
    sql_query_2 = (f"UPDATE public.stacje_pogotowia SET nazwa ='{station}', lokalizacja ='{location}' WHERE id ='{query_result[numer - 1][0]}';")
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


##########################################################
def remove_employees_by_station():
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
    sql_query_1 = f" SELECT id, imie, nazwisko, lokalizacja, incydent FROM public.pacjenci;"
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
def show_calls_by_station():
    sql_query_1 = "SELECT id, nazwa, lokalizacja FROM public.stacje_pogotowia;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print("Znaleziono następujące stacje: ")
    for numer_stacji, stacja in enumerate(query_result, start=1):
        print(f'{numer_stacji}: {stacja[1]} - {stacja[2]}')

    numer = int(input("Wybierz numer stacji, dla której chcesz wyświetlić incydenty: "))
    selected_station_id = query_result[numer - 1][0]  # ID wybranej stacji

    # Zapytanie SQL do pobrania pracowników dla wybranej stacji
    sql_query_2 = f"SELECT imie, nazwisko, lokalizacja, incydent " \
                  f"FROM public.pacjenci " \
                  f"WHERE id_stacji = {selected_station_id};"
    cursor.execute(sql_query_2)
    patients = cursor.fetchall()

    print(f"\nIncydenty zgłoszone dla stacji {query_result[numer - 1][1]}:")
    if patients:
        for indeks, patient in enumerate(patients, start=1):
            print(f'{indeks}: {patient[0]} {patient[1]} - {patient[3]} ({patient[2]})')
    else:
        print("Brak zgłoszonych incydentów.")


###########################################################
def update_call_by_station():
    sql_query_1 = "SELECT id, nazwa, lokalizacja FROM public.stacje_pogotowia;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print("Znaleziono następujące stacje: ")
    for numer_stacji, stacja in enumerate(query_result, start=1):
        print(f'{numer_stacji}: {stacja[1]} - {stacja[2]}')

    numer = int(input("Wybierz numer stacji, dla której chcesz aktualizować incydent: "))
    selected_station_id = query_result[numer - 1][0]  # ID wybranej stacji

    # Zapytanie SQL do pobrania pracowników dla wybranej stacji
    sql_query_2 = f"SELECT id, imie, nazwisko, lokalizacja, incydent " \
                  f"FROM public.pacjenci " \
                  f"WHERE id_stacji = {selected_station_id};"
    cursor.execute(sql_query_2)
    calls = cursor.fetchall()

    if calls:
        print(f"\nIncydenty zgłoszone dla stacji {query_result[numer - 1][1]} - {query_result[numer - 1][2]}:")
        for indeks, call in enumerate(calls, start=1):
            print(f'{indeks}: {call[1]} {call[2]} - {call[4]} ({call[3]})')

        call_id = int(input("\nWybierz numer incydentu do aktualizacji: "))
        if 1 <= call_id <= len(calls):
            new_name = input("Podaj nowe imię pacjenta: ")
            new_surname = input("Podaj nowe nazwisko pacjenta: ")
            new_location = input("Podaj nowy adres pacjenta (ulica nr budynku, kod pocztowy Miejscowość): ")
            incident = input("Podaj rodzaj incydentu: ")

            update_query = f"UPDATE public.pacjenci " \
                           f"SET imie = '{new_name}', " \
                           f"nazwisko = '{new_surname}', " \
                           f"lokalizacja = '{new_location}', " \
                           f"incydent = '{incident}' " \
                           f"WHERE id = {calls[call_id - 1][0]};"
            cursor.execute(update_query)
            db_params.commit()
            print("Dane pacjenta zaktualizowane pomyślnie.")
        else:
            print("Podano niepoprawny numer incydentu.")
    else:
        print("Brak zgłoszonych incydentów dla wybranej stacji.")


###########################################################
def remove_call_by_station():
    sql_query_1 = "SELECT id, nazwa, lokalizacja FROM public.stacje_pogotowia;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print("Znaleziono następujące stacje: ")
    for numer_stacji, stacja in enumerate(query_result, start=1):
        print(f'{numer_stacji}: {stacja[1]} - {stacja[2]}')

    numer = int(input("Wybierz numer stacji, dla której chcesz usunąć incydent: "))
    selected_station_id = query_result[numer - 1][0]  # ID wybranej stacji

    # Zapytanie SQL do pobrania pracowników dla wybranej stacji
    sql_query_2 = f"SELECT id, imie, nazwisko, lokalizacja, incydent " \
                  f"FROM public.pacjenci " \
                  f"WHERE id_stacji = {selected_station_id};"
    cursor.execute(sql_query_2)
    calls = cursor.fetchall()

    if calls:
        print(f"\nIncydenty zgłoszone dla stacji {query_result[numer - 1][1]}:")
        for indeks, call in enumerate(calls, start=1):
            print(f'{indeks}: {call[1]} {call[2]} - {call[4]} ({call[3]})')

        call_id = int(input("\nWybierz numer incydentu, którego chcesz usunąć: "))
        if 1 <= call_id <= len(calls):
            delete_query = f"DELETE FROM public.pacjenci WHERE id = {calls[call_id-1][0]};"
            cursor.execute(delete_query)
            db_params.commit()
            print("Incydent został pomyślnie usunięty.")
        else:
            print("Podano niepoprawny numer incydentu.")
    else:
        print("Brak zgłoszonych incydentów dla wybranej stacji.")


###########################################################
cursor = db_params.cursor()
sql_query_1 = "SELECT lokalizacja FROM public.stacje_pogotowia;"
cursor.execute(sql_query_1)
station_address = cursor.fetchall()

cursor = db_params.cursor()
sql_query_2 = "SELECT lokalizacja FROM public.pracownicy;"
cursor.execute(sql_query_2)
employees_address = cursor.fetchall()

cursor = db_params.cursor()
sql_query_2 = "SELECT lokalizacja FROM public.pacjenci;"
cursor.execute(sql_query_2)
call_address = cursor.fetchall()

def get_coordinates_of_stations(station_addres)->list[float,float]:
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {"q": station_addres, "format": "json"}

    response = requests.get(base_url, params)

    if response.status_code == 200:
        data = response.json()
        if data:
            latitude = data[0]["lat"]
            longitude = data[0]["lon"]
            return [latitude, longitude]


##########################################################
def get_coordinates_of_employees(employees_address)->list[float,float]:
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {"q": employees_address, "format": "json"}

    response = requests.get(base_url, params)

    if response.status_code == 200:
        data = response.json()
        if data:
            latitude = data[0]["lat"]
            longitude = data[0]["lon"]
            return [latitude, longitude]


##########################################################
def get_coordinates_of_calls(call_address)->list[float,float]:
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {"q": call_address, "format": "json"}

    response = requests.get(base_url, params)

    if response.status_code == 200:
        data = response.json()
        if data:
            latitude = data[0]["lat"]
            longitude = data[0]["lon"]
            return [latitude, longitude]

##########################################################
def get_all_stations_map():
    map = folium.Map(location=[52.23, 21.01],
                     tiles='OpenStreetMap',
                     zoom_start=10
                     )
    cursor.execute("SELECT nazwa, lokalizacja FROM public.stacje_pogotowia;")
    query_result = cursor.fetchall()
    for row in query_result:
        name = row[0]
        address = row[1]
        coordinates = get_coordinates_of_stations(address)
        if coordinates:
            folium.Marker(location=coordinates,
                          popup=f'{name}\n'
                                f'Lokalizacja: {address}\n'
                                f'Współrzędne: {coordinates[0]}, {coordinates[1]}'
                          ).add_to(map)

        else:
            print(f"Nie można znaleźć współrzędnych dla stacji: {name}")
            break
    map.save('mapa_stacji_pogotowia.html')
    print("Pomyślnie wygenerowano mapę wszystkich stacji pogotowia.")


##########################################################
def get_all_employees_map():
    map = folium.Map(location=[52.23, 21.01],
                     tiles='OpenStreetMap',
                     zoom_start=10
                     )
    cursor.execute("SELECT imie, nazwisko, funkcja, lokalizacja FROM public.pracownicy;")
    query_result = cursor.fetchall()
    for row in query_result:
        name = row[0]
        surname = row[1]
        function = row[2]
        address = row[3]
        coordinates = get_coordinates_of_stations(address)
        if coordinates:
            folium.Marker(location=coordinates,
                          popup=f'Imię: {name}\n'
                                f'Nazwisko: {surname}\n'
                                f'Stanowisko: {function}\n'
                                f'Lokalizacja: {address}\n'
                                f'Współrzędne: {coordinates[0]}, {coordinates[1]}'
                          ).add_to(map)

        else:
            print(f"Nie można znaleźć współrzędnych dla pacjenta: {name} {surname}")
            break
    map.save('mapa_pracowników.html')
    print("Pomyślnie wygenerowano mapę wszystkich pracowników.")


##########################################################
def get_employees_by_station_map():
    map = folium.Map(location=[52.23, 21.01],
                     tiles='OpenStreetMap',
                     zoom_start=10
                     )

    sql_query_1 = "SELECT id, nazwa, lokalizacja FROM public.stacje_pogotowia;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print("Znaleziono następujące stacje: ")
    for numer_stacji, stacja in enumerate(query_result, start=1):
        print(f'{numer_stacji}: {stacja[1]} - {stacja[2]}')

    numer = int(input("Wybierz numer stacji, dla której chcesz wygenerowac mapę pracowników: "))
    selected_station_id = query_result[numer - 1][0]  # ID wybranej stacji

    # Zapytanie SQL do pobrania pracowników dla wybranej stacji
    sql_query_2 = f"SELECT imie, nazwisko, lokalizacja, funkcja " \
                  f"FROM public.pracownicy " \
                  f"WHERE id_stacji = {selected_station_id};"
    cursor.execute(sql_query_2)
    employees = cursor.fetchall()

    for row in employees:
        name = row[0]
        surname = row[1]
        address = row[2]
        function = row[3]
        coordinates = get_coordinates_of_employees(address)

        if coordinates:
            folium.Marker(location=coordinates,
                          popup=f'Imię: {name}\n'
                                f'Nazwisko: {surname}\n'
                                f'Stanowisko: {function}\n'
                                f'Lokalizacja: {address}\n'
                                f'Współrzędne: {coordinates[0]}, {coordinates[1]}'
                          ).add_to(map)
        else:
            print(f"Nie można znaleźć współrzędnych dla pracownika: {name} {surname}")
            break
    map.save('mapa_pracowników_danej_stacji.html')
    print("Pomyślnie wygenerowano mapę pracowników dla wybranej stacji.")


##########################################################
def get_calls_by_station_map():
    map = folium.Map(location=[52.23, 21.01],
                     tiles='OpenStreetMap',
                     zoom_start=10
                     )

    sql_query_1 = "SELECT id, nazwa, lokalizacja FROM public.stacje_pogotowia;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print("Znaleziono następujące stacje: ")
    for numer_stacji, stacja in enumerate(query_result, start=1):
        print(f'{numer_stacji}: {stacja[1]} - {stacja[2]}')

    numer = int(input("Wybierz numer stacji, dla której chcesz wygenerowac mapę incydentów: "))
    selected_station_id = query_result[numer - 1][0]  # ID wybranej stacji

    # Zapytanie SQL do pobrania pracowników dla wybranej stacji
    sql_query_2 = f"SELECT imie, nazwisko, lokalizacja, incydent " \
                  f"FROM public.pacjenci " \
                  f"WHERE id_stacji = {selected_station_id};"
    cursor.execute(sql_query_2)
    calls = cursor.fetchall()

    for row in calls:
        name = row[0]
        surname = row[1]
        address = row[2]
        incident = row[3]
        coordinates = get_coordinates_of_calls(address)

        if coordinates:
            folium.Marker(location=coordinates,
                          popup=f'Imię: {name}\n'
                                f'Nazwisko: {surname}\n'
                                f'Incydent: {incident}\n'
                                f'Lokalizacja: {address}\n'
                                f'Współrzędne: {coordinates[0]}, {coordinates[1]}'
                          ).add_to(map)
        else:
            print(f"Nie można znaleźć współrzędnych dla pacjenta: {name} {surname}")
            break
    map.save('mapa_incydentów_danej_stacji.html')
    print("Pomyślnie wygenerowano mapę incydentów dla wybranej stacji.")

###########################################################
########################## GUI #################################
def gui() -> None:
    while True:
        print(f' MENU: \n'
              f'0: Zakończ program \n\n'
              'I. STACJE POGOTOWIA \n'
              f'1: Wyświetl listę stacji pogotowia \n'
              f'2: Dodaj stację pogotowia \n'
              f'3: Usuń stację pogotowia \n'
              f'4: Modyfikuj stację pogotowia \n\n'
              'II. PRACOWNICY STACJI POGOTOWIA \n'
              f'5: Wyświetl listę wszystkich pracowników \n'
              f'6: Dodaj pracownika \n'
              f'7: Usuń pracownika \n'
              f'8: Modyfikuj pracownika \n'
              f'9: Wyświetl listę pracowników wybranej stacji \n'
              f'10: Dodaj pracownika dla wybranej stacji \n'
              f'11: Usuń pracownika dla wybranej stacji \n'
              f'12: Modyfikuj pracownika wybranej stacji \n\n'
              'III. INCYDENTY \n'
              f'13: Wyświetl listę wszystkich incydentów \n'
              f'14: Dodaj dane o incydencie \n'
              f'15: Usuń dane o incydencie \n'
              f'16: Modyfikuj dane o incydencie \n'
              f'17: Wyświetl listę incydentów dla wybranej stacji \n'
              f'18: Dodaj dane o incydencie dla wybranej stacji \n'
              f'19: Usuń dane o incydencie dla wybranej stacji \n'
              f'20: Modyfikuj dane o incydencie dla wybranej stacji \n\n'
              'IV. GENEROWANIE MAPY \n'
              f'21: Wygeneruj mapę wszystkich stacji pogotowia \n'
              f'22: Wygeneruj mapę wszystkich pracowników \n'
              f'23: Wygeneruj mapę pracowników wybranej stacji \n'
              f'24: Wygeneruj mapę incydentów wybranej stacji \n\n'
              )

        menu_option = input('Podaj funkcję do wywołania ')
        print(f'Wybrano funkcję {menu_option}')

        match menu_option:
            case '0':
                print('Kończę pracę')
                break
            case '1':
                print('Wyświetlam listę stacji pogotowia')
                show_all_stations()
            case '2':
                print('Dodaję stację pogotowia')
                add_med_station()
            case '3':
                print('Usuwam stację pogotowia')
                remove_med_station()
            case '4':
                print('Modyfikuję stację pogotowia')
                update_station()
            case '5':
                print('Wyświetlam listę stacji pogotowia')
                show_all_employees()
            case '6':
                print('Dodaję pracownika')
                add_new_employee()
            case '7':
                print('Usuwam pracownika')
                remove_employee()
            case '8':
                print('Modyfikuję pracownika')
                update_employee()
            case '9':
                print('Wyświetlam listę pracowników wybranej stacji')
                show_employees_by_station()
            case '10':
                print('Dodaję pracownika wybranej stacji')
                add_new_employee_by_station()
            case '11':
                print('Usuwam pracownika wybranej stacji')
                remove_employees_by_station()
            case '12':
                print('Modyfikuję pracownika wybranej stacji')
                update_employees_by_station()
            case '13':
                print('Wyświetlam listę wszystkich incydentów')
                show_all_calls()
            case '14':
                print('Dodaję informacje o incydencie')
                add_new_call()
            case '15':
                print('Usuwam informacje o incydencie')
                remove_call()
            case '16':
                print('Modyfikuję informacje o incydencie')
                update_call()
            case '17':
                print('Wyświetlam listę incydentów wybranej stacji')
                show_calls_by_station()
            case '18':
                print('Dodaję informacje o incydencie dla danej stacji')
                add_new_call_by_station()
            case '19':
                print('Usuwam informacje o incydencie danej stacji')
                remove_call_by_station()
            case '20':
                print('Modyfikuję informacje o incydencie danej stacji')
                update_call_by_station()
            case '21':
                print('Generuję mapę wszystkich stacji pogotowia')
                get_all_stations_map()
            case '22':
                print('Generuję mapę wszystkich pracowników')
                get_all_employees_map()
            case '23':
                print('Generuję mapę pracowników dla wybranej stacji')
                get_employees_by_station_map()
            case '24':
                print('Generuję mapę incydentów dla wybranej stacji')
                get_calls_by_station_map()


###########################################################
########################## LOGOWANIE #################################
def log_in():
    password = input('Podaj hasło dostępu: ')
    pswrd = "Medcall2024"
    if password == pswrd:
        print('Hasło poprawne')
        gui()

    else:
        print('Hasło niepoprawne. Spróbuj ponownie.')
        log_in()





