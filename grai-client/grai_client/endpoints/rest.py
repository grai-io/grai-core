from multimethod import multimethod


@multimethod
def get():
    raise NotImplementedError()


@multimethod
def post():
    raise NotImplementedError()


@multimethod
def patch():
    raise NotImplementedError()


@multimethod
def delete():
    raise NotImplementedError()
