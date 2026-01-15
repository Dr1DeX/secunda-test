import asyncio
import random

from geoalchemy2 import WKTElement
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils.types.ltree import Ltree

from core.db.accessor import AsyncSessionFactory
from core.db.models.activity import Activity
from core.db.models.building import Building
from core.db.models.organization import Organization, OrganizationPhone, OrganizationActivity


# Тестовые данные для зданий (Москва)
BUILDINGS_DATA = [
    {"address": "Красная площадь, 1", "lat": 55.7539, "lon": 37.6208},
    {"address": "Тверская улица, 10", "lat": 55.7558, "lon": 37.6173},
    {"address": "Арбат, 25", "lat": 55.7520, "lon": 37.5925},
    {"address": "Кутузовский проспект, 2/1", "lat": 55.7420, "lon": 37.5350},
    {"address": "Ленинградский проспект, 39", "lat": 55.7890, "lon": 37.5360},
    {"address": "Проспект Мира, 119", "lat": 55.8300, "lon": 37.6300},
    {"address": "Варшавское шоссе, 47", "lat": 55.6500, "lon": 37.6100},
    {"address": "Ленинский проспект, 32", "lat": 55.7000, "lon": 37.5700},
    {"address": "Новый Арбат, 15", "lat": 55.7520, "lon": 37.5920},
    {"address": "Садовая-Кудринская, 5", "lat": 55.7600, "lon": 37.6000},
]

# Древовидная структура активностей
ACTIVITIES_TREE = [
    # Уровень 1
    {"name": "Торговля", "path": "1", "parent_id": None},
    {"name": "Общественное питание", "path": "2", "parent_id": None},
    {"name": "Услуги", "path": "3", "parent_id": None},
    {"name": "Развлечения", "path": "4", "parent_id": None},
    # Уровень 2 - Торговля
    {"name": "Продукты питания", "path": "1.1", "parent_id": 1},
    {"name": "Одежда и обувь", "path": "1.2", "parent_id": 1},
    {"name": "Электроника", "path": "1.3", "parent_id": 1},
    {"name": "Мебель", "path": "1.4", "parent_id": 1},
    # Уровень 3 - Продукты питания
    {"name": "Супермаркеты", "path": "1.1.1", "parent_id": 5},
    {"name": "Гипермаркеты", "path": "1.1.2", "parent_id": 5},
    {"name": "Магазины у дома", "path": "1.1.3", "parent_id": 5},
    # Уровень 2 - Общественное питание
    {"name": "Рестораны", "path": "2.1", "parent_id": 2},
    {"name": "Кафе", "path": "2.2", "parent_id": 2},
    {"name": "Фастфуд", "path": "2.3", "parent_id": 2},
    # Уровень 2 - Услуги
    {"name": "Банки", "path": "3.1", "parent_id": 3},
    {"name": "Салоны красоты", "path": "3.2", "parent_id": 3},
    {"name": "Медицинские услуги", "path": "3.3", "parent_id": 3},
    # Уровень 2 - Развлечения
    {"name": "Кинотеатры", "path": "4.1", "parent_id": 4},
    {"name": "Боулинг", "path": "4.2", "parent_id": 4},
    {"name": "Караоке", "path": "4.3", "parent_id": 4},
]

# Названия организаций по категориям
ORGANIZATION_NAMES = {
    "Супермаркеты": [
        "Пятёрочка",
        "Магнит",
        "Дикси",
        "Перекрёсток",
        "Ашан",
    ],
    "Гипермаркеты": [
        "Ашан",
        "Лента",
        "Карусель",
        "Глобус",
    ],
    "Рестораны": [
        "Ресторан 'Москва'",
        "Трактир 'У Палыча'",
        "Итальянский ресторан 'Белла'",
        "Японский ресторан 'Сакура'",
        "Грузинский ресторан 'Тбилиси'",
    ],
    "Кафе": [
        "Кофейня 'Кофеин'",
        "Кафе 'Уютное'",
        "Пекарня 'Сдоба'",
        "Кафе 'Бригантина'",
    ],
    "Фастфуд": [
        "Макдональдс",
        "Бургер Кинг",
        "KFC",
        "Subway",
    ],
    "Банки": [
        "Сбербанк",
        "ВТБ",
        "Альфа-Банк",
        "Тинькофф Банк",
    ],
    "Салоны красоты": [
        "Салон красоты 'Элегант'",
        "Парикмахерская 'Стиль'",
        "Студия красоты 'Шарм'",
    ],
    "Медицинские услуги": [
        "Медицинский центр 'Здоровье'",
        "Стоматология 'Белый клык'",
        "Клиника 'Доктор'",
    ],
    "Кинотеатры": [
        "Кинотеатр 'Октябрь'",
        "Кинотеатр 'Каро'",
        "Кинотеатр 'Формула кино'",
    ],
    "Боулинг": [
        "Боулинг 'Страйк'",
        "Боулинг-клуб 'Глория'",
    ],
    "Караоке": [
        "Караоке-бар 'Микрофон'",
        "Караоке-клуб 'Звёзды'",
    ],
    "Одежда и обувь": [
        "Магазин 'Модный стиль'",
        "Бутик 'Элегант'",
        "Обувной магазин 'Туфли'",
    ],
    "Электроника": [
        "Магазин электроники 'Техно'",
        "Салон связи 'МТС'",
        "Магазин 'Эльдорадо'",
    ],
    "Мебель": [
        "Магазин мебели 'Дом'",
        "Мебельный салон 'Комфорт'",
    ],
}


def generate_phone() -> str:
    """Генерирует случайный номер телефона."""
    return (
        f"+7 ({random.randint(900, 999)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
    )


async def create_buildings(session: AsyncSession) -> list[Building]:
    """Создаёт здания с координатами."""
    buildings = []
    for building_data in BUILDINGS_DATA:
        # Создаём WKT строку для Point (lon, lat для PostGIS)
        # Для Geography используем extended=True
        wkt = f"POINT({building_data['lon']} {building_data['lat']})"
        location = WKTElement(wkt, srid=4326, extended=True)

        building = Building(
            address=building_data["address"],
            location=location,
        )
        session.add(building)
        buildings.append(building)

    await session.commit()
    for building in buildings:
        await session.refresh(building)

    print(f"Создано {len(buildings)} зданий")
    return buildings


async def create_activities(session: AsyncSession) -> dict[int, Activity]:
    """Создаёт древовидную структуру активностей."""
    activities = []
    activity_id_map = {}  # Карта для связи индекса в списке с ID из БД

    for idx, activity_data in enumerate(ACTIVITIES_TREE):
        # Используем Ltree класс для правильной работы с LtreeType
        ltree_path = Ltree(activity_data["path"])
        activity = Activity(
            name=activity_data["name"],
            path=ltree_path,
            parent_id=None,
        )
        session.add(activity)
        activities.append(activity)

    await session.commit()

    for idx, activity in enumerate(activities):
        await session.refresh(activity)
        activity_id_map[idx + 1] = activity.id  # idx+1 потому что parent_id в данных начинается с 1

    for idx, activity_data in enumerate(ACTIVITIES_TREE):
        activity = activities[idx]
        if activity_data["parent_id"]:
            parent_idx = activity_data["parent_id"]
            activity.parent_id = activity_id_map[parent_idx]
            session.add(activity)

    await session.commit()

    for activity in activities:
        await session.refresh(activity)

    print(f"Создано {len(activities)} активностей")
    return {activity.id: activity for activity in activities}


async def create_organizations(
    session: AsyncSession,
    buildings: list[Building],
    activities: dict[int, Activity],
) -> list[Organization]:
    """Создаёт организации с телефонами и связями."""
    organizations = []

    activities_by_name = {activity.name: activity for activity in activities.values()}

    for category_name, org_names in ORGANIZATION_NAMES.items():
        if category_name not in activities_by_name:
            continue

        for org_name in org_names:
            building = random.choice(buildings)

            organization = Organization(
                name=org_name,
                building_id=building.id,
            )
            session.add(organization)
            organizations.append(organization)

    await session.commit()

    for org in organizations:
        await session.refresh(org)

    # Создаём карту организаций по категориям для правильной связи с активностями
    org_category_map = {}  # organization -> category_name
    for category_name, org_names in ORGANIZATION_NAMES.items():
        for org_name in org_names:
            for org in organizations:
                if org.name == org_name:
                    org_category_map[org] = category_name
                    break

    for org in organizations:
        num_phones = random.randint(1, 2)
        for _ in range(num_phones):
            phone = OrganizationPhone(
                organization_id=org.id,
                phone=generate_phone(),
            )
            session.add(phone)

        category_name = org_category_map.get(org)
        if category_name and category_name in activities_by_name:
            matched_activity = activities_by_name[category_name]
        else:
            matched_activity = random.choice(list(activities.values()))

        org_activity = OrganizationActivity(
            organization_id=org.id,
            activity_id=matched_activity.id,
        )
        session.add(org_activity)

        # С вероятностью 30% добавляем ещё одну активность (родительскую)
        if matched_activity.parent_id and random.random() < 0.3:
            parent_activity = activities[matched_activity.parent_id]
            parent_org_activity = OrganizationActivity(
                organization_id=org.id,
                activity_id=parent_activity.id,
            )
            session.add(parent_org_activity)

    await session.commit()

    print(f"Создано {len(organizations)} организаций")
    return organizations


async def clear_data(session: AsyncSession):
    """Очищает все данные из таблиц."""
    print("Очистка существующих данных...")

    # Удаляем в правильном порядке из-за внешних ключей
    await session.execute(text("TRUNCATE TABLE organization_phone CASCADE"))
    await session.execute(text("TRUNCATE TABLE organization_activity CASCADE"))
    await session.execute(text("TRUNCATE TABLE organization CASCADE"))
    await session.execute(text("TRUNCATE TABLE building CASCADE"))
    await session.execute(text("TRUNCATE TABLE activity CASCADE"))

    await session.commit()
    print("✓ Данные очищены")


async def main():
    print("=" * 60)
    print("Генерация тестовых данных")
    print("=" * 60)

    async with AsyncSessionFactory() as session:
        try:
            await clear_data(session)

            buildings = await create_buildings(session)

            activities = await create_activities(session)

            organizations = await create_organizations(session, buildings, activities)

            print("=" * 60)
            print("Генерация данных завершена успешно!")
            print("=" * 60)
            print("\nСоздано:")
            print(f"  - Зданий: {len(buildings)}")
            print(f"  - Деятельностей: {len(activities)}")
            print(f"  - Организаций: {len(organizations)}")

        except Exception as e:
            await session.rollback()
            print(f"Ошибка при генерации данных: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(main())
