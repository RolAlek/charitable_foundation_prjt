from datetime import datetime
from string import ascii_uppercase

from aiogoogle import Aiogoogle

from app.core.config import settings

COL = ascii_uppercase
FORMAT = "%Y/%m/%d %H:%M:%S"
SHEET_BODY = {
    'properties': {
        'sheetType': 'GRID',
        'sheetId': 0,
        'title': settings.sheet_title,
        'gridProperties': {
            'rowCount': 100,
            'columnCount': 11
        }
    }
}
TABLE_HEADER = [
    ['Отчет от'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {
            'title': f'Отчет от {now_date_time}',
            'locale': 'ru_RU'
        },
        'sheets': [SHEET_BODY]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: list[tuple[str]],
    wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = TABLE_HEADER.copy()
    table_values[0].append(datetime.now().strftime(FORMAT))

    for project in projects:
        data_row = [*project]
        table_values.append(data_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    column = COL[len(max(table_values, key=len)) - 1]
    lines_number = len(table_values)
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'A1:{column}{lines_number}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
