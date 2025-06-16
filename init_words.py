from database import session, init_db
from models import Word

def add_words():
    init_db() #tworzy wszystkie tabele na podstawie pliku models.py jeżeli jeszcze nie są stworzone

    word_entries = [ #krotka zawierająca po 10 haseł do 10 kategorii

        ("POWIEDZENIA", "LEPIEJ PÓŹNO NIŻ WCALE"),
        ("POWIEDZENIA", "PIERWSZE KOTY ZA PŁOTY"),
        ("POWIEDZENIA", "GDZIE KUCHAREK SZEŚĆ TAM NIE MA CO JEŚĆ"),
        ("POWIEDZENIA", "CZYM CHATA BOGATA TYM RADA"),
        ("POWIEDZENIA", "JAKOŚ TO BĘDZIE NOWY"),
        ("POWIEDZENIA", "MĄDRY POLAK PO SZKODZIE"),
        ("POWIEDZENIA", "CO ZA DUŻO TO NIEZDROWO"),
        ("POWIEDZENIA", "JAK CIĘ WIDZĄ, TAK CIĘ PISZĄ"),
        ("POWIEDZENIA", "KTO PÓŹNO PRZYCHODZI SAM SOBIE SZKODZI"),
        ("POWIEDZENIA", "NIE MA RÓŻY BEZ KOLCÓW"),


        ("PRZYSŁOWIA", "DAROWANEMU KONIOWI W ZĘBY SIĘ NIE ZAGLĄDA"),
        ("PRZYSŁOWIA", "CO MA WISIEĆ NIE UTONIE"),
        ("PRZYSŁOWIA", "NIE CHWAL DNIA PRZED ZACHODEM SŁOŃCA"),
        ("PRZYSŁOWIA", "GŁODNEMU CHLEB NA MYŚLI"),
        ("PRZYSŁOWIA", "KAŻDY KOWAL SWOJEGO LOSU"),
        ("PRZYSŁOWIA", "CZŁOWIEK CZŁOWIEKOWI WILKIEM"),
        ("PRZYSŁOWIA", "APETYT ROŚNIE W MIARĘ JEDZENIA"),
        ("PRZYSŁOWIA", "KTO POD KIM DOŁKI KOPIE SAM W NIE WPADA"),
        ("PRZYSŁOWIA", "NIE WSZYSTKO ZŁOTO CO SIĘ ŚWIECI"),
        ("PRZYSŁOWIA", "ZŁE PIENIĄDZE WYPIERAJĄ DOBRE"),


        ("RZECZ", "ELEKTRYCZNA HULAJNOGA"),
        ("RZECZ", "MASZYNA DO PISANIA"),
        ("RZECZ", "ODKURZACZ AUTOMATYCZNY"),
        ("RZECZ", "TABLET EDUKACYJNY"),
        ("RZECZ", "SMARTFON Z FOLDINGIEM"),
        ("RZECZ", "KAMERA CYFROWA HD"),
        ("RZECZ", "ZEGAREK NA RĘKĘ"),
        ("RZECZ", "STRATEGICZNA GRA KOMPUTEROWA"),
        ("RZECZ", "OKULARY PRZECIWSŁONECZNE"),
        ("RZECZ", "KLIMATYZATOR ŚCIENNY"),


        ("MIEJSCE", "ZAMEK KRÓLEWSKI NA WAWELU"),
        ("MIEJSCE", "PARK NARODOWY BIAŁOWIESKI"),
        ("MIEJSCE", "KATEDRA W NOTRE DAME"),
        ("MIEJSCE", "UNIWERSYTET WARSZAWSKI"),
        ("MIEJSCE", "MUZEUM NARODOWE W KRAKOWIE"),
        ("MIEJSCE", "RATUSZ W POZNANIU"),
        ("MIEJSCE", "WIEŻA EIFFLA W PARYŻU"),
        ("MIEJSCE", "LOTNISKO CHOPINA"),
        ("MIEJSCE", "PAŁAC KULTURY I NAUKI"),
        ("MIEJSCE", "OPERA W SYDNEY"),


        ("NATURA", "WODOSPAD NIAGARA"),
        ("NATURA", "PUSZCZA AMAZOŃSKA"),
        ("NATURA", "OCEAN SPOKOJNY"),
        ("NATURA", "LASY TROPIKALNE AMAZONII"),
        ("NATURA", "DELTA RZEKI AMAZONKI"),
        ("NATURA", "PARK KRAJOBRAZOWY"),
        ("NATURA", "ŁAŃCUCH GÓRSKI ANDY"),
        ("NATURA", "WULKAN KILAUEA"),
        ("NATURA", "WYBRZEŻE ATLANTYCKIE"),
        ("NATURA", "GÓRY SKALISTE"),


        ("SPORT", "BIEGI DŁUGODYSTANSOWE"),
        ("SPORT", "WYŚCIGI FORMUŁY JEDEN"),
        ("SPORT", "TURNIEJ TENISOWY WIMBLEDON"),
        ("SPORT", "RZUT MŁOTEM OLIMPIJSKIM"),
        ("SPORT", "ZAWODY TRIATHLONOWE"),
        ("SPORT", "SZTAFETA OLIMPIJSKA"),
        ("SPORT", "MISTRZOSTWA ŚWIATA FIFA"),
        ("SPORT", "PUCHAR EUROPY W SIATKÓWCE"),
        ("SPORT", "SKOKI NARCIARSKIE"),
        ("SPORT", "PIŁKA NOŻNA KOBIET"),


        ("MODA", "SUKIENKA W KWIATY"),
        ("MODA", "BUTY NA OBCASIE"),
        ("MODA", "KURTKA SKÓRZANA DAMSKA"),
        ("MODA", "GARNITUR W KRATĘ"),
        ("MODA", "SPODNIE Z WYSOKIM STANEM"),
        ("MODA", "KAPELUSZ SŁOMKOWY LETNI"),
        ("MODA", "JEANSY RURKI DAMSKIE"),
        ("MODA", "KOSZULA W PASKI"),
        ("MODA", "BLUZA Z NADRUKIEM"),
        ("MODA", "SWETER WEŁNIANY MĘSKI"),


        ("MOTORYZACJA", "SAMOCHÓD ELEKTRYCZNY"),
        ("MOTORYZACJA", "UKŁAD HAMULCOWY ABS"),
        ("MOTORYZACJA", "PRZEKŁADNIA AUTOMATYCZNA"),
        ("MOTORYZACJA", "PASY BEZPIECZEŃSTWA"),
        ("MOTORYZACJA", "SILNIK DWUSUWOWY MOTOCYKLOWY"),
        ("MOTORYZACJA", "BLOKADA SKRZYNI BIEGÓW"),
        ("MOTORYZACJA", "REFLEKTOR KIERUNKOWY LED"),
        ("MOTORYZACJA", "FELGI ALUMINIOWE SPORTOWE"),
        ("MOTORYZACJA", "BATERIA LITOWO JONOWA"),
        ("MOTORYZACJA", "WYDECH SPORTOWY STALOWY"),


        ("ZDROWIE", "ZDROWE ODŻYWIANIE"),
        ("ZDROWIE", "AKTYWNOŚĆ FIZYCZNA"),
        ("ZDROWIE", "BADANIA KONTROLNE OKRESOWE"),
        ("ZDROWIE", "PROFILAKTYKA CHORÓB SERCA"),
        ("ZDROWIE", "ĆWICZENIA ODDECHOWE RELAKSACYJNE"),
        ("ZDROWIE", "LECZENIE NATURALNE ZIOŁOWE"),
        ("ZDROWIE", "SUPLEMENTACJA WITAMINOWA"),
        ("ZDROWIE", "TERAPIA BEHAWIORALNA"),
        ("ZDROWIE", "REHABILITACJA POOPERACYJNA"),
        ("ZDROWIE", "SEN ODPORNOŚĆ I ZDROWIE"),


        ("WYDARZENIE", "FESTIWAL FILMOWY KANNE"),
        ("WYDARZENIE", "DOMOWA IMPREZA URODZINOWA"),
        ("WYDARZENIE", "PLENEROWY KONCERT NA ŻYWO"),
        ("WYDARZENIE", "WYBORY PARLAMENTARNE"),
        ("WYDARZENIE", "MŁODZIEŻOWE ZAWODY SPORTOWE"),
        ("WYDARZENIE", "GALA ROZDANIA NAGRÓD"),
        ("WYDARZENIE", "WYSTAWA MALARSTWA W MUZEUM"),
        ("WYDARZENIE", "MECZ PIŁKI NOŻNEJ REPREZENTACJI"),
        ("WYDARZENIE", "KONFERENCJA NAUKOWA ONLINE"),
        ("WYDARZENIE", "WIECZÓR AUTORSKI W BIBLIOTECE"),
    ]


    session.bulk_save_objects([Word(category=cat, value=val) for cat, val in word_entries]) #Tworzy listę obiektów Word i zapisuje je do bazy danych za pomocą SQLAlchemy
    session.commit() #zatwierdza dane w bazie

if __name__ == "__main__": #Umożliwia uruchomienie tego pliku jako samodzielnego pliku
    add_words()
