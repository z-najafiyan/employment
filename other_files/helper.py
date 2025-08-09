from rest_framework import exceptions
class FactoryGetObject:
    """
    a class is factory pattern for
    get a object
    """

    @classmethod
    def find_object(cls, object_type, *args, **kwargs) -> object:
        try:
            return object_type.objects.get(*args, **kwargs)
        except:
            name = str(object_type).split('.')[-1][0:-2]
            raise exceptions.NotFound(detail=f'{name} was not found')

    @classmethod
    def filter_object(cls, object_type, *args, **kwargs):
        if hasattr(object_type, 'is_active'):
            kwargs.update({'is_active': True})
        return object_type.objects.filter(*args, **kwargs)

    @classmethod
    def find_object_or_none(cls, object_type, *args, **kwargs):
        instance = object_type.objects.filter(is_active=True, *args, **kwargs).first()
        return instance if instance else None
