# База данных:

Таблица `Card`:

| Name            | Type    | description                                |
|-----------------|---------|--------------------------------------------|
| id              | INTEGER |                                            |
| name            | TEXT    | Название карточки                          |
| deadline_date   | TEXT    | Крайняя дата сдачи. В формате `ДД.ММ.ГГГГ` |
| deadline_date   | TEXT    | Крайняя дата сдачи. В формате `ЧЧ:ММ`      |
| ts_deadline     | INTEGER | Крайняя дата сдачи. В формате `timestamp`  |
| sequence_number | INTEGER | Порядковый номер задания                   |

Описание:
Информация о карточке для парсинга. Например, карточка модуля
---
Таблица `Comment`:

| id              | Type    | description                            |
|-----------------|---------|----------------------------------------|
| id              | INTEGER |                                        |
| task_id         | INTEGER | `id` задания                           |
| person_id       | INTEGER | `id` задания студента                  |
| content         | TEXT    | Текст комментария                      |
| overdue         | INTEGER | 0 - не просрочено, 1 - просрочено      |
| ts_create       | INTEGER | Дата комментария в формате `timestamp` |
| sequence_number | INTEGER | Порядковый номер комментария           |

Описание:
Информация о комментарии задания
---
Таблица `Person`:

| Name             | Type    | description               |
|------------------|---------|---------------------------|
| id               | INTEGER |                           |
| name             | TEXT    | Имя Фамилия студента      |
| rate             | TEXT    | Тариф студента            |
| tg_url           | TEXT    | Ссылка на телеграмм канал |
| tg_name          | TEXT    | Название телеграмм канала |
| subscriber_count | INTEGER | Количество подписчиков    |

Описание:
Информация о студенте
---
Таблица `PersonCard`:

| Name       | Type    | description                                                                |
|------------|---------|----------------------------------------------------------------------------|
| id         | INTEGER |                                                                            |
| person_id  | INTEGER | `id` задания студента                                                      |
| card_id    | INTEGER | `id` задания карточки                                                      |
| is_done    | INTEGER | 0 - задания не сделаны или сделаны но не все,<br/> 1 - сделаны все задания |
| total_done | TEXT    | Количество выполненных заданий                                             |

Описание:
Информация о результатах карточки студента
---
Таблица `Task`:

| Name            | Type    | description           |
|-----------------|---------|-----------------------|
| id              | INTEGER |                       |
| name            | TEXT    | Название задания      |
| card_id         | INTEGER | `id` задания карточки |
| sequence_number | INTEGER | Порядковый номер      |

Описание:
Информация о задании

# Требование к состояниям карточек:

- Сделано
- Задано
- Просрочено
    - назначить в столбец
