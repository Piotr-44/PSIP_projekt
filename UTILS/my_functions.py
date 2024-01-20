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

# DATABASE
def add_med_station():
    station = input("Podaj nazwę stacji:  ")
    location = input("Podaj adres stacji:  ")
    employee = input("Podaj imię i nazwisko ratownika:  ")
    patient = input("Podaj imię i nazwisko pacjenta: ")
    patient_location = input("Podaj lokalizację pacjenta:  ")
    accident = input("Podaj rodza incydentu: ")

    insert_query = f"INSERT INTO public.zabezpieczenie_medyczne(nazwa_stacji, lokalizacja_stacji, dane_ratownika, dane_pacjenta, lokalizacja_pacjenta, rodzaj_incydentu) VALUES ('{station}', '{location}', '{employee}', '{patient}', '{patient_location}', '{accident}');"
    cursor.execute(insert_query)
    db_params.commit()
    print(f"Dodano informacje o stacji pogotowia - {station}.")


##########################################################

# def remove_med_station():
#     station = input("Podaj nazwę stacji do usunięcia:  ")
#     sql_query_1 = f" SELECT * FROM public.tabela_psip WHERE name='{station}';"
#     cursor.execute(sql_query_1)
#     query_result = cursor.fetchall()
#     print(f'Znaleziono następujące stacje: ')
# 
#     for numer_stacji, station_to_be_removed in enumerate(query_result):
#         print(f'{numer_stacji + 1}: {station_to_be_removed}')
#     numer = int(input(f'Wybierz stację do usunięcia: '))
#     print(numer)
#     sql_query_2 = f"DELETE FROM public.zabezpieczenie_medyczne WHERE id='{query_result[numer - 1][0]}';"
#     cursor.execute(sql_query_2)
#     db_params.commit()
#
# remove_med_station()

##########################################################

def show_all_stations():
    sql_query_1 = f' SELECT * FROM public.zabezpieczenie_medyczne'
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    for row in query_result:
        print(f'{row[0]} - {row[1]}')

###########################################################

def update_station_name():
    station_name = input('Podaj nazwę stacji do modyfikacji: ')
    sql_query_1 = f" SELECT * FROM public.zabezpieczenie_medyczne WHERE nazwa_stacji =  '{station_name}';"
    cursor.execute(sql_query_1)
    print('Znaleziono !!!')
    station = input('Podaj nową nazwę stacji: ').strip()
    sql_query_2 = f"UPDATE public.zabezpieczenie_medyczne SET nazwa_stacji ='{station}' WHERE nazwa_stacji = '{station_name}';"
    cursor.execute(sql_query_2)
    db_params.commit()


###########################################################

