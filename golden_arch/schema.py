from graphene import ObjectType, Schema
import conference.schema 

class Query(conference.schema.Query, ObjectType):
    pass


class Mutation(conference.schema.Mutation, ObjectType):
    pass

schema = Schema(query=Query, mutation=Mutation)
