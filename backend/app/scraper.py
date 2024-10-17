import requests
from bs4 import BeautifulSoup


def scrape_movies():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    url = "https://www.kinoafisha.info/rating/movies/?page=0"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    all_movies = soup.find_all('div', attrs={
                               'class': 'movieList_item movieItem movieItem-rating movieItem-position'})

    movies = []
    # Получаем нужные данные с страницы
    for item in all_movies:
        title = item.find("a", attrs={"class": "movieItem_title"}).text
        genre = item.find("span", attrs={"class": "movieItem_genres"}).text
        rating = float(item.find("span", attrs={
                       "class": "movieItem_itemRating miniRating miniRating-good"}).text)
        image_url = item.find("img", attrs={"class": "picture_image"})[
            "data-picture"]

        # Получаем дополнительные данные с старницы фильма
        film_url = item.find("a", attrs={"class": "movieItem_title"})["href"]
        page_film = requests.get(film_url, headers=headers)
        soup_page_film = BeautifulSoup(page_film.content, 'lxml')

        # У некоторых фильмов нет описания
        try:
            description = soup_page_film.find(
                "div", attrs={"class": "tabs_contentItem js-active", "data-tabs-content-item": "1"}).find("p").text
        except:
            description = "Настолько интересный фильм что лучше его посмотреть чем читать описание :)"

        rating_IMDb = float(soup_page_film.find(
            "span", attrs={"class": "ratingBlockCard_externalVal"}).text)

        # У некоторых фильмов не указан режисер
        try:
            director = soup_page_film.find(
                "div", attrs={"class": "badgeList_content"}).find("span").text
        except:
            director = "Режисер захотел остаться неизвестным :)"

        try:
            image_path = download_image(image_url, title)
            movies.append({
                "title": title,
                "description": description,
                "rating": rating,
                "rating_IMDb": rating_IMDb,
                "genre": genre,
                "director": director,
                "image_path": image_path
            })
        except Exception as e:
            print(f"Ошибка при обработке {title}: {e}")

    return movies


def download_image(url, title):
    # Удаляем запрещенные символы для сохранение обложек фильмов
    title = title.replace(":", "").replace("|", "").replace(
        " ", "_")
    response = requests.get(url)
    path = f"backend/images/{title}.jpg"
    with open(path, "wb") as f:
        f.write(response.content)
    return path
