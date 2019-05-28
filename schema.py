import graphene
import json
import uuid
from datetime import datetime

# Model


class User(graphene.ObjectType):
    # id = graphene.ID()
    # created_at = graphene.DateTime()
    id = graphene.ID(default_value=str(uuid.uuid4()))
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())
 # this makes getting created at and id dynamic so we dont have to pass them in the mutate function

#  Query


class Query(graphene.ObjectType):
    users = graphene.List(User)
    # users = graphene.List(User, limit=graphene.Int()) using limits.
    hello = graphene.String()
    is_admin = graphene.Boolean()

# Resolvers

    def resolve_hello(self, info):
        return "world"

    def resolve_users(self, info):
        # def resolve_users(self, info, limit=None): when using limit and also making it optional
        return [
            User(id=1, username="fred", created_at=datetime.now()),
            User(id=2, username="ken", created_at=datetime.now()),
        ]

    def resolve_is_admin(self, info):
        return True
# query resolver must be written in camel case and must start with  the word resolve


class CreateUser(graphene.Mutation):
    user = graphene.Field(User)  # this like basically extending the User class

    class Arguments:
        username = graphene.String()

    def mutate(self, info, username):  # will always be mutate
        user = User(username=username)
        return CreateUser(user=user)

# Mutation


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()  # class that handles creating user


schema = graphene.Schema(query=Query, mutation=Mutation)

# schema.execute queries must be a string and does not work with camel case. you need to change to snake case.

# a work around is graphene.Schema(query=Query, auto_camelcase=False)
result = schema.execute(
    '''
      mutation {
        createUser(username: "Joe") {
          user {
            id
            username
            createdAt
          }
        }
      }
    ''',
    # mutation ($username: String) {
    # using variables to make mutations dynamic
    #       createUser(username: $username) {
    #         user {
    #           id
    #           username
    #           createdAt
    #         }
    #       }
    #     }

    # {  calling query with limit
    #   users(limit: 1) {
    #     id
    #     username
    #     createdAt
    #   }
    # }
    variable_values={'username': 'Dave'}
)

dictResult = dict(result.data.items())

print(json.dumps(dictResult, indent=2))
