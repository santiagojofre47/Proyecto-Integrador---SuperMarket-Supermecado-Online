from flask_login import UserMixin

class Admin(UserMixin):
    def __init__(self, id, correo, codigo):
        self.id = id
        self.correo = correo
        self.codigo = codigo