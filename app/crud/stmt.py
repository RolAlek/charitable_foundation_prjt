from sqlalchemy import case, cast, extract, select, String

from app.models import CharityProject


SEC_MIN = 60
SEC_HOUR = SEC_MIN ** 2
SEC_DAY = SEC_HOUR * 24
TWO_DIG = 10
DAY = 1

stmt = select(
    [
        CharityProject.name,
        (
            cast((
                (extract('epoch', CharityProject.close_date) -
                 extract('epoch', CharityProject.create_date)) / SEC_DAY
            ), String) +
            case((
                (extract('epoch', CharityProject.close_date) -
                 extract('epoch', CharityProject.create_date)) / SEC_DAY > DAY,
                ' days '
            ), else_=' day ') +
            case((
                ((extract('epoch', CharityProject.close_date) -
                 extract('epoch', CharityProject.create_date)) %
                 SEC_DAY) / SEC_HOUR < TWO_DIG,
                '0' + cast(
                    ((extract('epoch', CharityProject.close_date) -
                     extract('epoch', CharityProject.create_date)) %
                     SEC_DAY) / SEC_HOUR, String)
            ), else_=cast(
                ((extract('epoch', CharityProject.close_date) -
                  extract('epoch', CharityProject.create_date)) %
                    SEC_DAY) / SEC_HOUR, String)
            ) +
            ':' +
            case((
                (((extract('epoch', CharityProject.close_date) -
                   extract('epoch', CharityProject.create_date)) %
                    SEC_DAY) % SEC_HOUR) / SEC_MIN < TWO_DIG,
                ('0' + cast((((extract('epoch', CharityProject.close_date) -
                               extract('epoch', CharityProject.create_date)) %
                            SEC_DAY) % SEC_HOUR) / SEC_MIN, String)
                 )
            ),
                else_=cast((((extract('epoch', CharityProject.close_date) -
                              extract('epoch', CharityProject.create_date)) %
                            SEC_DAY) % SEC_HOUR) / SEC_MIN, String)
            ) +
            ':' +
            case((
                (((extract('epoch', CharityProject.close_date) -
                   extract('epoch', CharityProject.create_date)) %
                    SEC_DAY) % SEC_HOUR) % SEC_MIN < TWO_DIG,
                ('0' + cast((((extract('epoch', CharityProject.close_date) -
                               extract('epoch', CharityProject.create_date)) %
                            SEC_DAY) % SEC_HOUR) % SEC_MIN, String)
                 )
            ),
                else_=cast((((extract('epoch', CharityProject.close_date) -
                              extract('epoch', CharityProject.create_date)) %
                            SEC_DAY) % SEC_HOUR) % SEC_MIN, String)
            )).label('duration'),
        CharityProject.description
    ]).where(CharityProject.fully_invested.is_(True)).order_by(
        extract('epoch', CharityProject.close_date) -
        extract('epoch', CharityProject.create_date))
