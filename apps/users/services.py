from rest_framework.exceptions import ValidationError, NotFound, APIException
from .repositories import UserRepository

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def _format_user(self, user):
        if user:
            user['id'] = str(user.pop('_id'))
        return user

    def get_all_users(self):
        try:
            users = self.repo.get_all()
            return [self._format_user(u) for u in users]
        except Exception:
            raise APIException("Error conectando a MongoDB")

    def get_user_by_id(self, user_id: str):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise NotFound("No se ha encontrado el usuario")
        return self._format_user(user)

    def create_user(self, user_data: dict):
        if self.repo.get_by_email(user_data.get('email', '')):
            raise ValidationError("El usuario con este email ya existe.")
        
        user = self.repo.create(user_data)
        return self._format_user(user)

    def update_user(self, user_id: str, user_data: dict):
        user = self.repo.update(user_id, user_data)
        if not user:
            raise NotFound("No se ha actualizado el usuario")
        return self._format_user(user)

    def delete_user(self, user_id: str):
        success = self.repo.delete(user_id)
        if not success:
            raise NotFound("No se ha eliminado el usuario")