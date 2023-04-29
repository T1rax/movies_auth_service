from pydantic import BaseModel


class FakeUser(BaseModel):
    id: str = '1235'

fake_user = FakeUser()


print(fake_user.id)