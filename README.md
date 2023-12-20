![](logos/logo.svg)

## Python клиент (https://career.habr.com/)

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

> Клиент не официальный и пока не полон т. к. есть места, где API либо отсутствует, либо сломано.

## Как этим пользоваться?

Для начала экспортируем токен:
```shell
export HABR_CAREER_TOKEN=<Your token here>
```
После чего python код может выглядеть следующим образом:
```python
import os
from habr.career.client import HABRCareerClient, TokenAuthenticator

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

Поскольку процесс логина защищен `google recaptcha`, то сначала выполняем вход
на веб клиенте как обычно. После чего копируем `remember_user_token`, сохраненный в `cookies`.

Токены выдаются на 29 дней.

В случае утечки токена его следует инвалидировать:
```python
import os
from habr.career.client import HABRCareerClient, TokenAuthenticator

token = os.getenv("HABR_CAREER_TOKEN")
client = HABRCareerClient(auth=TokenAuthenticator(token=token))

client.logout()
```
Или даже проще, так как есть для этого отдельная функция:
```python
from habr.career.client import logout

logout("<Your token here>")
```

## CLI

Также доступен CLI инструмент `career`.

Примеры использования:
```shell
career version
career --help
career conversations list
career conversations connect --username test_it
career conversations send --username test_it -m "Давайте завтра в 13.00."
career users cv -u test_it -p "test_it_cv.pdf"
career users complain -u test_it --reason spam
career friendships list
career friendships requests approve --username test_it
career friendships requests --help
career logout
```

Реализованы следующие разделы:
- [ ] вакансии (https://career.habr.com/vacancies)
- [ ] специалисты (https://career.habr.com/resumes)
- [ ] эксперты (https://career.habr.com/experts)
- [ ] компании (https://career.habr.com/companies)
- [ ] рейтинг (https://career.habr.com/companies/ratings)
- [ ] зарплаты (https://career.habr.com/salaries)
- [ ] образование (https://career.habr.com/courses)
- [ ] журнал (https://career.habr.com/journal)
- [x] переписки (https://career.habr.com/conversations)
- [x] друзья (https://career.habr.com/x55aah/friends)
