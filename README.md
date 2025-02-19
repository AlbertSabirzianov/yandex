# yandex
Модуль, который позволяет получить картинку из поисковика Яндекс

# Как использовать
установите зависимости
```commandline
pip install -r requirements.txt
```
импортируйте и используйте в своём коде
```python
from yandex.pictures import get_picture

with open("my_picture.jpeg", "wb") as file:
    file.write(get_picture("кошечка"))
```


