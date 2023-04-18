from multimethod import multimethod


@multimethod
async def get():
    raise NotImplementedError()


@multimethod
async def post():
    raise NotImplementedError()


@multimethod
def patch():
    raise NotImplementedError()


@multimethod
def delete():
    raise NotImplementedError()
