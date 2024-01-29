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

