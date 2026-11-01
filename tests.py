import pytest

from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_genre()) == 2 #Я ИСПРАВИЛ ТУТ МЕТОД, ИНАЧЕ ПРОВЕРКА ПАДАЕТ

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()


    @pytest.mark.parametrize('book_name', [
        '',                                             
        'Яндекс Практикум, прими сё с первого раза'    
    ])
    def test_add_new_book_invalid_length_not_added(self, book_name):
        # 1. Параметризация на некорректную длину названия книги
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert book_name not in collector.get_books_genre()

    def test_add_new_book_add_duplicate_book_not_added_twice(self):
        # 2. Одну и ту же книгу пытаемся добавить дважды
        collector = BooksCollector()
        collector.add_new_book('Дракула')
        collector.add_new_book('Дракула')
        assert len(collector.get_books_genre()) == 1

    @pytest.mark.parametrize('genre', ['Фантастика', 'Ужасы', 'Комедии'])
    def test_set_book_genre_existing_book_valid_genres_are_set(self, genre):
        # 3. Параметризация на установку разных валидных жанров из списка разрешенных
        collector = BooksCollector()
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', genre)
        assert collector.get_book_genre('Оно') == genre

    def test_set_book_genre_invalid_genre_not_set(self):
        # 4. Несуществующий в списке жанр не устанавливается
        collector = BooksCollector()
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Аниме')  # Такого жанра нет в self.genre
        assert collector.get_book_genre('Оно') == ''

    def test_get_book_genre_for_new_book_is_empty_string(self):
        # 5. У только что добавленной книги жанр изначально пустой
        collector = BooksCollector()
        collector.add_new_book('Шерлок Холмс')
        assert collector.get_book_genre('Шерлок Холмс') == ''

    def test_get_books_with_specific_genre_returns_only_matching_books(self):
        # 6. Проверяем фильтрацию книг по конкретному жанру
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.add_new_book('Основание')
        collector.set_book_genre('Дюна', 'Фантастика')
        collector.set_book_genre('Основание', 'Фантастика')
        
        books = collector.get_books_with_specific_genre('Фантастика')
        assert 'Дюна' in books and 'Основание' in books and len(books) == 2

    @pytest.mark.parametrize('genre', ['Мультфильмы', 'Комедии'])
    def test_get_books_for_children_allowed_genres_are_added(self, genre):
        # 7а. Проверяем, что жанры без возрастного рейтинга успешно добавляются в список для детей
        collector = BooksCollector()
        book_name = f'Детская книга {genre}'
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        
        children_books = collector.get_books_for_children()
        assert book_name in children_books

    @pytest.mark.parametrize('genre', ['Ужасы', 'Детективы'])
    def test_get_books_for_children_restricted_genres_are_excluded(self, genre):
        # 7б. Проверяем, что жанры с возрастным рейтингом строго исключаются из списка для детей
        collector = BooksCollector()
        book_name = f'Взрослая книга {genre}'
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        
        children_books = collector.get_books_for_children()
        assert book_name not in children_books

    def test_add_book_in_favorites_existing_book_is_added(self):
        # 8. Успешное добавление существующей книги в избранное
        collector = BooksCollector()
        collector.add_new_book('Властелин Колец')
        collector.add_book_in_favorites('Властелин Колец')
        assert 'Властелин Колец' in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_not_in_collector_not_added(self):
        # 9. Добавление в избранное книгу, которой нет в общем списке
        collector = BooksCollector()
        collector.add_book_in_favorites('Несуществующая книга')
        assert 'Несуществующая книга' not in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_removes_correctly(self):
        # 10. Удаление книги из избранного
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.add_book_in_favorites('Гарри Поттер')
        collector.delete_book_from_favorites('Гарри Поттер')
        assert 'Гарри Поттер' not in collector.get_list_of_favorites_books()

    def test_get_books_genre_returns_full_dictionary(self):
        # 11. Тестируем непосредственно метод get_books_genre
        collector = BooksCollector()
        collector.add_new_book('Русалочка')
        collector.set_book_genre('Русалочка', 'Мультфильмы')
        
        current_genres = collector.get_books_genre()
        assert current_genres == {'Русалочка': 'Мультфильмы'}

    def test_get_list_of_favorites_books_returns_full_list(self):
        # 12. Тестируем непосредственно метод get_list_of_favorites_books
        collector = BooksCollector()
        collector.add_new_book('Дракула')
        collector.add_book_in_favorites('Дракула')
        
        favorites_list = collector.get_list_of_favorites_books()
        assert favorites_list == ['Дракула'] 

        # перенести создание экземпляра в фикстуры в отдельный файл conftest - это не стал делать
        # в 26 строчке прописано: 
        # # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()
        # но с реальным проектом лучше использовать фикстуры, чтобы код был чище, согласен полностью

