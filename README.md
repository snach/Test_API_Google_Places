# Test_API_Google_Places #
тестирование команды **_nearbysearch_** API Google Places    
документация: https://developers.google.com/places/web-service/search?hl=ru
## Перед запуском ##
```
install python3
pip3 install pytest
export KEY=<your API KEY>
```
## Запуск ##
```
все тесты: py.test -v
отдельный тест-кейс: py.test -v -l -k <TEST_CLASS>
пример:  py.test -v -l -k TestKeysAPI
```
## Чеклист ##
```
1. Изменилось ли API
    1.1 первый уровень вложенности (results, status, html_attributions)
    1.2 второй уровень вложенности (keys results)
        a. блок results.geometry
        b. блок results.photos
2. Обязательные параметры
    2.1 <key>
        a. запрос без ключа
        b. запрос с неправильным ключом
        c. в параметрах запроса только правильный ключ
        d. smoke_test: апи завелось (правильные key, location, radius)
    2.2 <location>
        a. все обязательные параметры, кроме location
        b. location = 0,0 (нулевые результаты поиска)
        c. пограничные значения координат: location=a,b , где a=[-90,90], b=[-280,180]
        d. очень длинная координата в location
        f. целые координаты
    2.3 <radius>
        a. все обязательные параметры, кроме radius
        b. неправильные значения radius (-200, 0)
        c. чем больше radius, тем больше найдено мест
        d. в ответе запроса с бОльшим радиусом присутствуют места из ответа с меньшим радиусом при одинаковом location

3. Дополнительные параметры
    3.1 <keyword>
    3.2 <language>
    3.3 <minprice/maxprice>
    3.4 <name>
    3.5 <opennow>
    3.6 <rankby>
    3.7 <type>
    3.8 <pagetoken>
```
## Баги ##
```
1. Отсутствует место(place) из запроса с keyword в запросе без keyword (запросы с одинаковым radius)

    как воспроизвести:

        запрос без keyword: curl "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=<API_KEY>&location=55.797208,37.5355793&radius=100" | grep -E "name|next_page_token"
            "name" : "Moscow",
            "name" : "Кристалл+ Торгово-сервисная Компания",
            "name" : "Kukhni Sokol Salon Mebeli",
            "name" : "The Moscow Times",
            "name" : "Khoroshyovsky District",
        запрос с keyword: curl "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=<API_KEY>&location=55.797208,37.5355793&radius=100&keyword=starbucks" | grep -E "name|next_page_token"
            "name" : "Starbucks",

    ожидаемое поведение:
        1. место с "name" : "Starbucks" ищется по запросу БЕЗ keyword
        2. место с "name" : "Starbucks" НЕ ищется по запросу С keyword

    иначе неопределенность в использовании API
```
## На данный момент ##
```
написаны тесты только для обязательных параметров
```