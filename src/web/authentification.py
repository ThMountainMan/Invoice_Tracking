from .helper import Container
from database import DbConnection, User, NotExists


class Container(Container):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user = get_current_user()

    def check_permission(self):
        pass


def get_current_user():

    id_user = 1
    # TODO: We need to implement a way to check the user session
    # id_user = session.get(KEY_LOGIN_USER)
    # if id_user is None:
    #     return User()
    with DbConnection() as db:
        try:
            user = db.get("user", id_user)
        except NotExists:
            user = User()

    # HACK: This needs to be removed !!!
    user.id = None
    return user


# def ensure_login():
#     if not session.get(KEY_LOGIN_USER):
#         raise redirect("/login?referer={}".format(urlquote(request.url)))
#     return True
