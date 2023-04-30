from pydantic import BaseModel


class FakeUser(BaseModel):
    id: str = "8c7f211d-85a2-442c-bc69-4cf4d719bf71"
    login: str = "test_login"
    email: str = "test_login@test.ru"
    password: str = "1235qwer"
    first_name: str = "Ivan"
    last_name: str = "Ivanov"
    age_group: str = "18-24"
    roles: list = ["basicRole"]


fake_user = FakeUser()
