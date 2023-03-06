from tortoise import fields
from tortoise.models import Model


class User(Model):

    id = fields.IntField(pk=True)

    name = fields.CharField(max_length=64, blank=True, null=True)
    surname = fields.CharField(max_length=64, blank=True, null=True)
    
    email = fields.CharField(max_length=64, blank=False, unique=True)
    username = fields.CharField(max_length=64, blank=False, unique=True)
    password = fields.CharField(max_length=64, blank=False, unique=True)

    added_at = fields.DatetimeField(auto_now_add=True)

    async def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "added_at": str( self.added_at )
        }

    class Meta:

        ordering = ["-id"]


class Token(Model):

    id = fields.IntField(pk=True)
    
    token = fields.CharField(max_length=64, blank=False)
    expiration_date = fields.DateField()

    owner = fields.ForeignKeyField("models.User")
    added_at = fields.DatetimeField(auto_now_add=True)


    async def serialize(self) -> dict:
        owner = await self.owner 
        return {
            "id": self.id,
            "token": self.token,
            "expiration_date": str( self.expiration_date ),
            "owner": owner.id,
            "added_at": str( self.added_at )
        }


    class Meta:

        ordering = ["-id"]