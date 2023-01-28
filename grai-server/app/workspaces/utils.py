try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local


_thread_locals = local()


def get_current_user():
    """
    Utils to get the user that has been set in the current thread using `set_current_user`.
    Can be used by doing:
    ```
        my_class_object = get_current_user()
    ```
    Will return None if the user is not set
    """
    return getattr(_thread_locals, "user", None)


def set_current_user(user):
    """
    Utils to set a user in the current thread.
    Often used in a middleware once a user is logged in to make sure all db
    calls are sharded to the current user.
    Can be used by doing:
    ```
        get_current_user(my_class_object)
    ```
    """

    setattr(_thread_locals, "user", user)
