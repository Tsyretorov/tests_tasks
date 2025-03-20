from tortoise import fields, models

class User(models.Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.IntField(null=True)
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255)
    username = fields.CharField(max_length=255)
    birth_date = fields.DateField(null=True)