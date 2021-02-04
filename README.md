Написать API на Flask для парсинга сайтов с двумя методами. POST запрос получает адрес сайта и в ответ возвращает ID задачи. GET запрос по ID задачи возвращает текущее состояние задачи. Когда задача выполнена, возвращает URL, по которому можно скачать архив.
 В задание входит парсер, который пробегается по сайту с лимитированной вложенностью, например, до 3 уровней и сохраняет html/css/js и медиа файлы.

Зависимости

```
pip install flask 
pip install flask-restful 
pip install flask-sqlalchemy 
pip install flask-marshmallow 
pip install marshmallow-sqlalchemy 
pip install environs
pip install requests
pip install beautifulsoup4
pip install lxml