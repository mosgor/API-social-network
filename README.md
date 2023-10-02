# Техническое задание проекта №2

Вы - бэкенд-разработчик API для платформы социальной сети для текстовых постов. Вам требуется создать полноценный сервис, который выполняет следующие функции:

+ Создает пользователя (проверяет почту на правильность), который может писать посты, ставить реакции (heart, like, dislike, boom, ...) на посты других пользователей
+ Выдает данные по конкретному пользователю
+ Создает пост
+ Выдает данные по конкретному посту
+ Пользователь ставит реакцию на пост
+ Выдает все посты пользователя, отсортированные по количеству реакций
+ Генерирует список пользователей, отсортированный по количеству реакций
+ Генерирует график пользователей по количеству реакций

Допущения:

- Объекты допустимо хранить в runtime
- Валидацию правильности почты можно сделать через регулярные выражения, сторонние библиотеки

Необходимо:

- Код должен быть отформатирован (например, при помощи black)
- Обработать все частные случаи (пользователя не существует, пользователь с такой почтой уже зарегистрирован и т. д.)

# Запросы и ответы

- Создание пользователя `POST /users/create`

Request example:
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string",
}
```

Response example:
```json
{
  "id": "number",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "total_reactions": "number"
  "posts": []
}
```

- Получение данных по определенному пользователю `GET /users/<user_id>`

Response example:
```json
{
  "id": "number",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "total_reactions": "number",
  "posts": [
    "number",
    ...
  ]
}
```

- Создание поста `POST /posts/create`

Request example:
```json
{
  "author_id": "number",
  "text": "string",
}
```

Response example:
```json
{
  "id": "number",
  "author_id": "number",
  "text": "string",
  "reactions": [
  	"string",
    ...
  ] 
}
```

- Получение данных по определенному посту `GET /posts/<post_id>`

Response example:
```json
{
  "id": "number",
  "author_id": "number",
  "text": "string",
  "reactions": [
  	"string",
    ...
  ] 
}
```

- Поставить реакцию посту `POST /posts/<post_id>/reaction`

Request example:
```json
{
  "user_id": "number",
  "reaction": "string"
}
```

Response example: (пусто, только код ответа)

- Получение всех постов пользователя, отсортированных по количеству реакций `GET /users/<user_id>/posts`

Значение `asc` обозначет `ascending` (по возрастанию), параметр `desc` обозначет `descending` (по убыванию)

Request example:
```json
{
  "sort": "asc/desc"
}
```

Response example:
```json
{
	"posts": [
    	{
  			"id": "number",
  			"author_id": "string",
  			"text": "string",
  			"reactions": [
  				"string",
    			...
  			] 
  		},
        {
        	...
        }
    ]
}
```

- Получение всех пользователей, отсортированных по количеству реакций `GET /users/leaderboard`

Значение `asc` обозначет `ascending` (по возрастанию), параметр `desc` обозначет `descending` (по убыванию)

Request example:
```json
{
  "type": "list",
  "sort": "asc/desc"
}
```

Response example:
```json
{
	"users": [
    	{
          "id": "number",
          "first_name": "string",
          "last_name": "string",
          "email": "string",
          "total_reactions": "number"
		},
        {
        	...
        }
    ]
}
```

- Получение графика пользователей по количеству реакций `GET /users/leaderboard`

Request example:
```json
{
  "type": "graph",
}
```

Response example:
```html
<img src="path_to_graph">
```