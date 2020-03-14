# -*- encoding: utf-8 -*-

from datetime import datetime
from django_filters import FilterSet, OrderingFilter
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


class ConferenceTopicFilter(FilterSet):
    class Meta:
        model = ConferenceTopic
        fields = {
            "name": {"exact", "icontains", "istartswith"},
            "description": {"exact", "icontains"},
        }

    order_by = OrderingFilter(
        fields=(
            ('create_time', 'create_time'),
        )
    )

class ConferenceTopicNode(DjangoObjectType):
    class Meta:
        model = ConferenceTopic
        filterset_class = ConferenceTopicFilter
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


class ConferenceTopicMutation(FixedDjangoModelFormMutation):
    """增加或修改主题。当不带 ID 时, 为新增主题。"""
    conference_topic = graphene.Field(ConferenceTopicNode)

    @classmethod
    def perform_mutate(cls, form, info):
        obj = form.save(commit=False)
        obj.creator = info.context.user
        obj.save()
        form.save_m2m()
        kwargs = {cls._meta.return_field_name: obj}
        return cls(errors=[], **kwargs)

    class Meta:
        form_class = ConferenceTopicForm


class ClaimConferenceTopicMutation(relay.ClientIDMutation):
    """某个用户认领主题"""
    class Input:
        id = graphene.ID(required=True)

    conference_topic = graphene.Field(ConferenceTopicNode)
    errors = graphene.List(ErrorType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, **kwargs):
        # print("ID is", id)
        conference_topic: ConferenceTopic = ConferenceTopic.objects.get(pk=from_global_id(id)[1])
        if conference_topic.claim_user:
            return ClaimConferenceTopicMutation(conference_topic=conference_topic, errors=[{'error': ["任务已经被认领"]}])
        conference_topic.claim_user = info.context.user
        conference_topic.claim_time = datetime.now()
        conference_topic.save()
        return ClaimConferenceTopicMutation(conference_topic=conference_topic, errors=[])


class Mutation(graphene.ObjectType):
    conference = ConferenceMutation.Field()
    conference_topic = ConferenceTopicMutation.Field()
    claim_conference_topic = ClaimConferenceTopicMutation.Field()
