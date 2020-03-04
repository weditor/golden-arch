
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_relay import from_global_id


class FixedDjangoModelFormMutation(DjangoModelFormMutation):

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        """覆盖原有的函数。原来的函数有个bug。没法反序列化 graphene.ID"""
        kwargs = {"data": input}

        pk = input.pop("id", None)
        if pk:
            _, _pk = from_global_id(pk)
            instance = cls._meta.model._default_manager.get(pk=_pk)
            kwargs["instance"] = instance

        return kwargs
        
    class Meta:
        abstract = True
