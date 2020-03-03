
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphene import relay, ObjectType
import graphene
from graphene_django.types import ErrorType

from .models import Conference, ConferenceTopic
from .forms import ConferenceForm
from graphql_relay import from_global_id


class ConferenceNode(DjangoObjectType):
    class Meta:
        model = Conference
        filter_fields = {
            "name": {"exact", "icontains", "istartswith"},
            "description": {"exact", "icontains"},
        }
        interfaces = (relay.Node, )


class Query(ObjectType):
    single_conference = relay.Node.Field(ConferenceNode)
    conferences = DjangoFilterConnectionField(ConferenceNode)


class ConferenceMutation(DjangoModelFormMutation):
    conference = graphene.Field(ConferenceNode)

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        kwargs = {"data": input}

        pk = input.pop("id", None)
        if pk:
            _, _pk = from_global_id(pk)
            instance = cls._meta.model._default_manager.get(pk=_pk)
            kwargs["instance"] = instance

        return kwargs

    class Meta:
        form_class = ConferenceForm


class CreateConferenceMutation(relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        holding_time = graphene.DateTime(required=True)
        description = graphene.String(required=False)

    errors = graphene.List(ErrorType)
    conference = graphene.Field(ConferenceNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        form = ConferenceForm(data=kwargs)
        if not form.is_valid():
            return UpdateConferenceMutation(errors=form.errors, conference=conference)
        conference = form.save()
        return UpdateConferenceMutation(errors=[], conference=conference)


class UpdateConferenceMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID()
        name = graphene.String(required=True)
        holding_time = graphene.DateTime(required=True)
        description = graphene.String(required=False)

    errors = graphene.List(ErrorType)
    conference = graphene.Field(ConferenceNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, **kwargs):
        conference = Conference.objects.get(pk=from_global_id(id)[1])
        form = ConferenceForm(instance=conference, data=kwargs)
        if not form.is_valid():
            return UpdateConferenceMutation(errors=form.errors, conference=conference)
        form.save()
        return UpdateConferenceMutation(errors=[], conference=conference)


class DeleteConferenceMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID()

    errors = graphene.List(ErrorType)
    conference = graphene.Field(ConferenceNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        conference = Conference.objects.get(pk=from_global_id(id)[1])
        conference.delete()
        return UpdateConferenceMutation(errors=[], conference=conference)


class Mutation(graphene.ObjectType):
    conference = ConferenceMutation.Field()
    create_conference = CreateConferenceMutation.Field()
    update_conference = UpdateConferenceMutation.Field()
    delete_conference = DeleteConferenceMutation.Field()
