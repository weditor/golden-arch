
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
from golden_arch.patch import FixedDjangoModelFormMutation
from graphene import relay, ObjectType
import graphene
from graphene_django.types import ErrorType

from .models import HxUser
# from .forms import ConferenceForm, ConferenceTopicForm
# from graphql_relay import from_global_id


class HxUserNode(DjangoObjectType):
    class Meta:
        model = HxUser
        fields = ("email", "username", "name")
        # filter_fields = {
        #     "name": {"exact", "icontains", "istartswith"},
        #     "description": {"exact", "icontains"},
        # }
        interfaces = (relay.Node, )


class Query(ObjectType):
    user = relay.Node.Field(HxUserNode)
    # conferences = DjangoFilterConnectionField(ConferenceNode)
    # single_conference_topic = relay.Node.Field(ConferenceTopicNode)
    # conferences_topic = DjangoFilterConnectionField(ConferenceTopicNode)
