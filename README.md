
![image](i.webp)

# yandex-searcher
<br/>Библиотека для удобного взаимодействия с поисковой системой Яндекс.
Позволяет получать ссылки на изображения и статьи по заданному поисковому запросу.
## Возможности

- Получение URL изображений с Яндекс.Картинок по поисковому запросу.
- Получение URL статей с Яндекс поиска.

---
# Как использовать
Установите библиотеку
```commandline
pip install yandex-searcher
```
Импортируйте и используйте в своём коде
```python
import yandexsearcher

# список url с изображениями из поисковой системы Яндекс
cat_picture_urls = yandexsearcher.get_picture_urls("cats")


# список url со статьями из поисковой системы Яндекс
cat_article_urls = yandexsearcher.get_articles_urls("cats")

```


