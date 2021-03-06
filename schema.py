import graphene
import json
import uuid
from datetime import datetime

# Model


class Post(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()


class User(graphene.ObjectType):
    # id = graphene.ID()
    # created_at = graphene.DateTime()
    id = graphene.ID(default_value=str(uuid.uuid4()))
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())
 # this makes getting created at and id dynamic so we dont have to pass them in the mutate function
    avatar_url = graphene.String()

    def resolve_avatar_url(self, info):
        return 'https://cloudinary.com/{}/{}'.format(self.username, self.id)
#  Query


class Query(graphene.ObjectType):
    # using limits.
    users = graphene.List(User, limit=graphene.Int())
    # users = graphene.List(User)
    hello = graphene.String()
    is_admin = graphene.Boolean()

# Resolvers

    def resolve_hello(self, info):
        return "world"

    def resolve_users(self, info, limit=None):
        # when using limit and also making it optional def resolve_users(self, info):
        return [
            User(id=1, username="fred", created_at=datetime.now()),
            User(id=2, username="ken", created_at=datetime.now()),
        ][:limit]
        # [:limit] is needed when using limit

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


class CreatePost(graphene.Mutation):
    post = graphene.Field(Post)

    class Arguments:
        title = graphene.String()
        content = graphene.String()

    def mutate(self, info, title, content):
        info.context.get('is_anonymous')
        post = Post(title=title, content=content)
        return CreatePost(post=post)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()  # class that handles creating user
    create_post = CreatePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

# schema.execute queries must be a string and does not work with camel case. you need to change to snake case.

# a work around is graphene.Schema(query=Query, auto_camelcase=False)
result = schema.execute(
    '''
      mutation {
        createPost(title: "Hello", content: "World") {
          post {
            title
            content
          }
        }
      }
      
    ''',
    context={'is_anonymous': True},
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
    # mutation {
    #     createUser(username: "Joe") {
    #       user {
    #         id
    #         username
    #         createdAt
    #       }
    #     }
    #   }

    # query getUsersQuery ($limit: Int) {
    #     users (limit: $limit) {
    #       id
    #       username
    #       createdAt
    #     }
    #   }
    # variable_values={'username': 'Dave'}
    variable_values={'limit': 1}
)

dictResult = dict(result.data.items())

print(json.dumps(dictResult, indent=2))
