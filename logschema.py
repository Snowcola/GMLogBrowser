import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from parse import (Session, Log as LogModel, Instrument as InstrumentModel,
                    HourlyRecord as HourlyRecordModel, DailyRecord as DailyRecordModel )


class Instrument(SQLAlchemyObjectType):
    class Meta:
        model = InstrumentModel
        filter_field = ['instrument']
        interfaces = (relay.Node, )

class InstrumentConnection(relay.Connection):
    class Meta:
        node = Instrument

class Log(SQLAlchemyObjectType):
    class Meta:
        model = LogModel
        interfaces = (relay.Node, )

class LogConnections(relay.Connection):
    class Meta:
        node = Log

class HourlyRecord(SQLAlchemyObjectType):
    class Meta:
        model = HourlyRecordModel
        interfaces = (relay.Node, )

class HourlyRecordConnections(relay.Connection):
    class Meta:
        node = HourlyRecord

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    instrument = graphene.List(Instrument, name=graphene.String(required=True))
    all_logs = SQLAlchemyConnectionField(LogConnections, sort=None)
    all_instruments = SQLAlchemyConnectionField(InstrumentConnection, sort=None)

    def resolve_instrument(self, info, name):
        return Instrument.get_query(info).filter_by(instrument=name)




schema = graphene.Schema(query=Query, types=[Log, Instrument, HourlyRecord])