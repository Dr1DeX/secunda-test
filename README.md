# secunda-test
Тестовое задание Secunda
___
## Цель задания: реализовать REST API приложения для справочника Организаций, Зданий, Деятельности
___

## Стек: 
### PostGis(расширение для PostgreSQL)
### FastAPI
### Python 3.12
### SQLAlchemy + LTree(для работы с деревьями) + geoalchemy2(для работы с координатами)
### Pydantic
### Alembic

___

## Локальный запуск(только инфра)
### Я использую пакетный менеджер `uv`, однако можно воспользоваться стандартным `pip`

#### Установка зависимостей через uv
`uv sync --no cache`

#### Установка зависимостей через pip
`pip install -r requirements.txt`

### Запуск приложения
`python main.py app`

#### Или через IDE конфигурацию(нужно передать обязательно параметр app)
___

## Локальный запуск через Docker
### `make run-staging`

___

## Документация Swager UI доступна по адресу http://localhost:8889/api/public/docs
`GET /api/public/directory/buildings` - список зданий

`lat` - широта
`lon` - долгота

```json
{
  "result": [
    {
      "id": 1,
      "address": "Красная площадь, 1",
      "lat": 55.7539,
      "lon": 37.6208
    },
    {
      "id": 2,
      "address": "Тверская улица, 10",
      "lat": 55.7558,
      "lon": 37.6173
    }
  ],
  "status": 200,
  "error_message": ""
}
```

`GET /api/public/directory/buildings/{building_id}/organizations` - организации в здании
```json
{
  "result": [
    {
      "id": 14,
      "name": "Грузинский ресторан 'Тбилиси'"
    },
    {
      "id": 18,
      "name": "Кафе 'Бригантина'"
    }
  ],
  "status": 200,
  "error_message": ""
}

```
`GET /api/public/directory/organizations/{organization_id}` - информация об организации
```json
{
  "result": {
    "id": 1,
    "name": "Пятёрочка",
    "phones": [
      "+7 (928) 519-60-10",
      "+7 (937) 235-78-64"
    ],
    "building": {
      "id": 7,
      "address": "Варшавское шоссе, 47",
      "lat": 55.65,
      "lon": 37.61
    },
    "activities": [
      {
        "id": 9,
        "name": "Супермаркеты",
        "path": "1.1.1",
        "level": null
      }
    ]
  },
  "status": 200,
  "error_message": ""
}
```
`GET /api/public/directory/organizations/search?name=...` - поиск по названию
```json
{
  "result": [
    {
      "id": 21,
      "name": "KFC"
    }
  ],
  "status": 200,
  "error_message": ""
}
```
`GET /api/public/directory/organizations/radius?lat=...&lon=...&radius_m=...` - организации в радиусе
```json
{
  "result": [
    {
      "id": 6,
      "name": "Ашан",
      "building_id": 9,
      "address": "Новый Арбат, 15",
      "distance_m": 0
    },
    {
      "id": 14,
      "name": "Грузинский ресторан 'Тбилиси'",
      "building_id": 9,
      "address": "Новый Арбат, 15",
      "distance_m": 0
    }
  ],
  "status": 200,
  "error_message": ""
}
```
- `GET /api/public/directory/organizations/bbox?min_lat=...&min_lon=...&max_lat=...&max_lon=...` - организации в области
```json
{
  "result": [
    {
      "id": 1,
      "name": "Пятёрочка"
    },
    {
      "id": 2,
      "name": "Магнит"
    }
  ],
  "status": 200,
  "error_message": ""
}
```
- `GET /api/public/directory/activities` - список видов деятельности
```json
{
  "result": [
    {
      "id": 1,
      "name": "Торговля",
      "path": "1",
      "parent_id": null
    },
    {
      "id": 2,
      "name": "Общественное питание",
      "path": "2",
      "parent_id": null
    }
  ],
  "status": 200,
  "error_message": ""
}
```
- `GET /api/public/directory/activities/{activity_id}/organizations/exact` - организации по точному виду деятельности
```json
{
  "result": [
    {
      "id": 41,
      "name": "Бутик 'Элегант'"
    },
    {
      "id": 42,
      "name": "Обувной магазин 'Туфли'"
    }
  ],
  "status": 200,
  "error_message": ""
}
```
- `GET /api/public/directory/activities/{activity_id}/organizations/subtree` - организации по поддереву деятельности
```json
{
  "result": [
    {
      "id": 1,
      "name": "Пятёрочка"
    },
    {
      "id": 2,
      "name": "Магнит"
    }
  ],
  "status": 200,
  "error_message": ""
}
```