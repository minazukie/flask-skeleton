import time

import mongoengine as me


class Cat(me.Document):
    name = me.StringField(required=True)
    age = me.IntField(required=True, min_value=0)
    gender = me.IntField(required=True, min_value=0, max_value=2)
    birthday = me.IntField(required=True)
    tags = me.ListField(default=list)
    state = me.StringField(required=True)
    created_at = me.IntField(required=True)
    updated_at = me.IntField(required=True)


if __name__ == "__main__":
    me.connect(host="mongodb://localhost/cat_house")
    Cat(
        name="kitty",
        age=1,
        gender=1,
        birthday=int(time.time()),
        state="active",
        created_at=int(time.time()),
        updated_at=int(time.time()),
    ).save()
    print(Cat.objects().to_json())
