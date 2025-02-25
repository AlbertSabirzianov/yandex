# yandex
Модуль, который позволяет получить картинку из поисковика Яндекс

# Как использовать
установите зависимости
```commandline
pip install -r requirements.txt
```
импортируйте и используйте в своём коде
```python
from yandex.pictures import get_picture, get_random_picture

with open("first_picture_from_yandex.jpeg", "wb") as file:
    file.write(get_picture("кошечка"))

with open("random_picture_from_yandex.jpeg", "wb") as file:
    file.write(get_random_picture("кошечка"))
```


