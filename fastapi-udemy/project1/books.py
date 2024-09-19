from fastapi import FastAPI, Body

app = FastAPI()

# 실행 : uvicorn books:app --reload
# --reload 옵션 줄시 코드 변화가 있을때 마다 자동 리로드
# 혹은 fastapi run books2.py
# fastapi run dev books2.py 로 실행시 개발모드

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Fi  ve', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


# 작거나 정적 api 를 앞에 둬야함
@app.get("/api-endpoint")
async def first_api():
    return "{'message': 'Hello fff'}"


@app.get("/books")
async def read_all_books():
    return BOOKS


# 위에서 부터 탐색하기 때문에 아래에 둘 경우 무시됨
# @app.get("/books/mybook")
# async def read_all_books():
#     return {'dynamic_param': 'My favorite book!'}


@app.get("/books/{book_title}")
async def read_all_books(book_title: str):
    return {'dynamic_param': book_title}


@app.get("/book/{book_title}")
async def read_specific_book(book_title: str):
    for book in BOOKS:
        # casefold() : 소문자 변환
        if book.get('title').casefold() == book_title.casefold():
            return book


# url 에 쿼리 파라미터를 정의하지 않아도 알아서 적용
@app.get("/books/")
async def read_category_by_query(category: str) -> list:
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

# 밑에 함수보다 밑에 있으면 오류남
# ‼️작은 api 는 가급적 앞에 있어야함 ‼️
@app.get("/books/author/")
async def read_books_written_by(author: str) -> list:
    books_to_return = []
    for i in range(len(BOOKS)):
        if BOOKS[i].get('author').casefold() == author.casefold():
            books_to_return.append(BOOKS[i])
    return books_to_return


@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str) -> list:
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
                book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


# swagger 에서 테스트할때는 쌍따음표를 써야함
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(update_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == update_book.get('title').casefold():
            BOOKS[i] = update_book


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
