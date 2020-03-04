
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
from golden_arch.patch import FixedDjangoModelFormMutation
from graphene import relay, ObjectType
import graphene
from graphene_django.types import ErrorType

from .models import Conference, ConferenceTopic
from .forms import ConferenceForm, ConferenceTopicForm
from graphql_relay import from_global_id


class ConferenceNode(DjangoObjectType):
    class Meta:
        model = Conference
        filter_fields = {
            "name": {"exact", "icontains", "istartswith"},
            "description": {"exact", "icontains"},
        }
        interfaces = (relay.Node, )


class ConferenceTopicNode(DjangoObjectType):
    class Meta:
        model = ConferenceTopic
        filter_fields = {
            "name": {"exact", "icontains", "istartswith"},
            "description": {"exact", "icontains"},
        }
        interfaces = (relay.Node, )


class Query(ObjectType):
    single_conference = relay.Node.Field(ConferenceNode)
    conferences = DjangoFilterConnectionField(ConferenceNode)
    single_conference_topic = relay.Node.Field(ConferenceTopicNode)
    conferences_topic = DjangoFilterConnectionField(ConferenceTopicNode)


class ConferenceMutation(FixedDjangoModelFormMutation):
    conference = graphene.Field(ConferenceNode)

    class Meta:
        form_class = ConferenceForm


# class DeleteConferenceMutation(relay.ClientIDMutation):
#     class Input:
#         id = graphene.ID()

#     errors = graphene.List(ErrorType)
#     conference = graphene.Field(ConferenceNode)

#     @classmethod
#     def mutate_and_get_payload(cls, root, info, **kwargs):
#         conference = Conference.objects.get(pk=from_global_id(id)[1])
#         conference.delete()
#         return DeleteConferenceMutation(conference=conference)


class ConferenceTopicMutation(FixedDjangoModelFormMutation):
    conference_topic = graphene.Field(ConferenceTopicNode)

    class Meta:
        form_class = ConferenceTopicForm


class Mutation(graphene.ObjectType):
    conference = ConferenceMutation.Field()
    # delete_conference = DeleteConferenceMutation.Field()
    conference_topic = ConferenceTopicMutation.Field()
