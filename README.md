![](logo.svg)

## Python клиент Хабр Карьера (https://career.habr.com/)

> **Примечание**: клиент не официальный

Функционал включает следующие разделы веб клиента:
- [x] вакансии (https://career.habr.com/vacancies)
- [x] специалисты (https://career.habr.com/resumes)
- [x] эксперты (https://career.habr.com/experts)
- [ ] компании (https://career.habr.com/companies)
- [x] рейтинг (https://career.habr.com/companies/ratings)
- [x] зарплаты (https://career.habr.com/salaries)
- [x] образование (https://career.habr.com/courses)
- [ ] журнал (https://career.habr.com/journal)
- [x] переписки (https://career.habr.com/conversations)
- [x] друзья (https://career.habr.com/x55aah/friends)

Утильные разделы, созданные для удобства:
- [x] tools - набор вспомогательных методов, используемых для работы веб клиента
- [x] users - набор методов для работы с пользователем

> Клиент пока не полон т. к. есть места, где API либо отсутствует, либо сломано.

## Как этим пользоваться?

Для начала экспортируем токен:
```shell
export HABR_CAREER_TOKEN=<Your token here>
```
После чего python код может выглядеть следующим образом:
```python
import os
from habr.career import HABRCareerClient, TokenAuthenticator

# Получаем сконфигурированный этапом ранее токен
token = os.getenv("HABR_CAREER_TOKEN")

# Создаем аутентификатор
auth = TokenAuthenticator(token=token)

# Создаем клиент
client = HABRCareerClient(auth=auth)

# Ваш код
cv_data: bytes = client.get_my_cv()
with open("my_cv_file.pdf", "wb") as f:
    f.write(cv_data)
```

## Где взять токен?

Поскольку процесс логина защищен google recaptcha, то сначала выполняем вход
на веб клиенте как обычно. После чего копируем `remember_user_token`, сохраненный в `cookies`.

Токены живут достаточно долго. Я пока не сталкивался с ситуацией, когда созданный ранее токен
переставал работать.

> Токен не умирает даже если выполнить logout. Поэтому нужно быть крайне осторожным,
> чтобы токен никуда случайно не утек. Как инвалидировать конкретно взятый токен
> пока не ясно.