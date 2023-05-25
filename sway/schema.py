import graphene
import meditations.schema


class Query(meditations.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
