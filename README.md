![](logos/logo.svg)

---

Функционал включает следующие разделы веб клиента:
- [x] [вакансии](https://career.habr.com/vacancies)
- [x] [специалисты](https://career.habr.com/resumes)
- [x] [эксперты](https://career.habr.com/experts)
- [ ] [компании](https://career.habr.com/companies)
- [x] [рейтинг](https://career.habr.com/companies/ratings)
- [x] [зарплаты](https://career.habr.com/salaries)
- [x] [образование](https://career.habr.com/courses)
- [ ] [журнал](https://career.habr.com/journal)
- [x] [переписки](https://career.habr.com/conversations)
- [x] [друзья](https://career.habr.com/x55aah/friends)

> Клиент не официальный и пока не полон т. к. есть места, где API 
> либо отсутствует, либо сломано.

> Кроме того JSON, получаемый от сервиса, валидируется при помощи 
> `pydantic` и потому это еще одна точка возможного сбоя, поскольку
> нет открытой документации по форматам данных, получаемых при
> помощи не официального API.

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
на веб клиенте как обычно через форму. После чего копируем `remember_user_token`, 
сохраненный в `cookies`.

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

Есть правда еще один токен, который сессионный.
Сохраняется он также в `cookies` под именем `_career_session`.
И он также может быть использован для выполнения операций требующих авторизации:

```python
import os
from habr.career.client import HABRCareerClient

session_id = os.getenv("HABR_CAREER_SESSION_ID")
client = HABRCareerClient(session_id=session_id)

# Ваш код
```

В отличие от основного токена, сессионный токен генерируется после каждого запроса.
При этом остается возможность использовать и сгенерированный ранее. Как долго - пока не ясно.
Но совершенно точно дольше обычного. Поэтому с точки зрения удобства лучше использовать
именно его.

## CLI

Также доступен CLI инструмент `career`.

Примеры использования:
```shell
export HABR_CAREER_TOKEN="Your token here"
# export HABR_CAREER_SESSION_ID="Your session ID here"
# export HABR_CAREER_DEBUG=1

# Включаем autocomplete (в данном случае для оболочки zsh)
# Подробнее об этом можно посмотреть здесь
# https://click.palletsprojects.com/en/8.1.x/shell-completion/#enabling-completion
eval "$(_CAREER_COMPLETE=zsh_source career)"

career --version
career --help
career conversations list
career conversations connect --username testuser
career conversations send --username testuser -m "Давайте завтра в 13.00."
career users cv -u testuser -o "testuser_cv.pdf"
career users complain -u testuser --reason spam
career friendships list
career friendships requests approve --username testuser
career friendships requests --help
career logout
```

Реализованы следующие разделы:
- [x] [вакансии](https://career.habr.com/vacancies)
- [x] [специалисты](https://career.habr.com/resumes)
- [x] [эксперты](https://career.habr.com/experts)
- [ ] [компании](https://career.habr.com/companies)
- [x] [рейтинг](https://career.habr.com/companies/ratings)
- [x] [зарплаты](https://career.habr.com/salaries)
- [ ] [образование](https://career.habr.com/courses)
- [ ] [журнал](https://career.habr.com/journal)
- [x] [переписки](https://career.habr.com/conversations)
- [x] [друзья](https://career.habr.com/x55aah/friends)

## Кому это может быть нужно?

- Во-первых, это любители командной строки.
Теперь есть возможность искать работу/сотрудников как настоящий IT профессионал =).
Также есть возможность вести переписку, просматривать статистику заработных плат
в виде красивых диаграмм и многое другое, что предлагает сервис хабр карьера,
при этом не покидая любимого терминала. Где-то это даже удобнее, так как
вы получаете ровно ту информацию, которую запрашиваете, без рекламы и рекомендаций.
А где-то и менее, в особенности там где есть сложные и многочисленные фильтры.


- И тут стоит упомянуть о второй категории людей, кому это может пригодиться - 
любители все автоматизировать =). Скрипты, отображающие данные в табличной
форме, также умеют выводить данные в `JSON` формате, который легко прочитать
сторонним инструментом, таким как `jq` и построить pipeline, который в дальнейшем 
будет запускаться посредством `CRON` или другим планировщиком, или вручную.
Вот пример того, как можно отобрать среди кандидатов на вакансию 5 человек
и сохранить их CV на локальном жестком диске:

      career resumes list \
      --sort salary_asc \
      --with-salary \
      --qualification 6 \
      --skills 446 \
      --salary 500000 \
      --currency rur \
      --locations c_707 \
      --per-page 5 \
      --relocation \
      --work-state search \
      --json \
      | jq ".resumes.objects.[] | .id" \
      | xargs -L1 -I {} \
      career users cv -u {} -o "{}_cv.pdf"

- Тем же хардкорным автоматизаторам, которым и этого окажется мало, есть возможность,
к примеру, поднять сервис, используя API python клиента, который будет проверять на наличие таких
событий, как новое сообщение, входящий запрос на добавления в друзья или другие,
и обрабатывать их в автоматическом режиме, избавляя вас от необходимости мониторить это вручную.
Например, можно сразу ответить HRу, сообщив где лучше всего с вами связаться, или, выявив среди
его контактов телегу, ответить туда, приложив файл с вашим CV.