from multimethod import multimethod

from grai_client.endpoints.utilities import expects_unique_query, paginated


@multimethod
def get():
    """ """
    raise NotImplementedError()


@multimethod
def post():
    """ """
    raise NotImplementedError()


@multimethod
def patch():
    """ """
    raise NotImplementedError()


@multimethod
def delete():
    """ """
    raise NotImplementedError()


@paginated
def paginated_get(*args, **kwargs):
    """ """
    return get(*args, **kwargs)


@paginated
def paginated_post(*args, **kwargs):
    """ """
    return post(*args, **kwargs)


@paginated
def paginated_patch(*args, **kwargs):
    """ """
    return patch(*args, **kwargs)


@paginated
def paginated_delete(*args, **kwargs):
    """ """
    return delete(*args, **kwargs)


@expects_unique_query
def get_is_unique(*args, **kwargs):
    """ """
    return get(*args, **kwargs)


@expects_unique_query
def paginated_get_is_unique(*args, **kwargs):
    """ """
    return paginated_get(*args, **kwargs)
