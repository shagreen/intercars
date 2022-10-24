# Backend

Appka rekrutacyjna do Intercars

# Architecture

Powiedzieliście, żebym skupił się nie na widokach tylko na backendzie, dlatego postanowiłem napisać tą aplikacje jako
"headless" a jako główny framework wybrałem nie czyste django a django-rest-framework. Standardy oparłem na styleguide
stworzony przez HackSoftware dostępny tutaj:
https://github.com/HackSoftware/Django-Styleguide

Wybrałem ten styleguide z dwóch powodów:

1. Bardzo go lubię :) Chociaż lekko to zmodyfikałem pod siebie
2. Wasza appka działa lata i jest pisana na lata - ten styleguide jest bardzo "sztywny" i dobrze opisuje
   odpowiedzialność poszczególnych elementów, dlatego uważam, że do takich aplikacji nadaje się bardzo dobrze.

Moduł "intercars", potraktowałem jako common, nie wiem czy nie lepiej byłoby wydzielić tego do innej appki ale zostawiam
już tak jak jest. Znajdują się tam utilsy i commony pobrane z wyżej wymienionego style guide. Osobiście sama
implementacja średnio mi się podoba i jakbym miał więcej czasu to trochę bym te utilsy poprawił.

## Docker Images:

Redis = Chciałem wykorzystać do cache ale zabrakło mi czasu  
Postgres = Baza danych  
Backend = Server Django. Kod znajduje się w katalogu /app/

# Run

```bash
$ cd docker
$ docker-compose up --build
```

Serwer automatycznie "wstanie" ale nie ma napisanych fixtur. Należy stworzyć sobie użytkowników przez

```bash
./manage createsuperuser
```

# Tests

Skrypt run_test.sh

Skrypt automatycznie odpala testy oraz zwraca coverage do katalogu *htmlcov*. Jest to wygodne przy CI, bo zwraca output
z testów (przez co CI ładnie pokarze błąd) a jednocześnie katalog *htmlcov* przydaje się gdy jest wrzucone do
artefaktów.

Oprócz tego jest skonfigurowany i zainstalowany prospector, którego najprościej uruchomić z głównego katalogu projektu:

```bash
python3 -m prospector
```

# Swagger

końcówka: ```http://0.0.0.0:8000/swagger/```  
Na szybko jak używać:

Znajdź końcówke  ```/ login /``` i zaloguj się na użytkownika, którego wcześniej stworzysz za pomocą "createsuperuser".
W zwrotce dostaniesz token, który należy wpisać w okno które pojawi się po kliknięciu w przycisk ```Authenticate```
który jest na górze strony swaggera po prawej stronie. Token trzeba wpisać w formule:  ```Token xxxxxxxxx```. Od tej
pory header zostanie dodany do każdej ramki podczas używania swaggera. Jest to najwygodniejsza opcja korzystania z tego
API.

# TODO:

Jest kilka rzeczy które jeszcze chciałem zrobić ale zabrakło mi czasu. Z takich najbardziej oczywistych to:

1. IbanField - który by automatycznie określał i walidował pole iban
2. BaseSerializer - który posiadałby, chociażby Meta w ktorym ref_name=None byłby zawsze, tak by nie trzeba było pisać
   tego za każdym razem.
3. Chciałem wykorzystać redisa jako cache
4. Działające gitlab CI-CD
5. Więcej końcówek, ale myślę, że tego kodu już jest całkiem wystarczająco by pokazać, w jaki sposób rozumuję.
6. Można zrobić z pola iban primary key
7. Unity do serwisów - uznalem, ze testy dla usersow sa wystarczajace by pokazac ze potrafie je pisać :)
8. Logowanie - zwykle używam structloga, ale appka niewiele lobi więc ostatecznie pominąłem temat.
