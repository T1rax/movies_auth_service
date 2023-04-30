from pydantic import BaseSettings, Field


class MainConfig(BaseSettings):
    """Project settings"""

    log_level: str = Field("INFO")
    existing_roles: list = Field(["basicRole", "premiumUser", "admin", "superUser"])
    pending_anonymous_id: str = Field(None)
    testing: bool = Field(False)


class MemoryDataStorageConfig(BaseSettings):
    """Cache settings"""

    address: str = Field("http://redis:6379")
    host: str = Field("redis")
    port: int = Field(6379)
    exp: int = Field(60 * 5)  # 5 minutes


class DataBaseConfig(BaseSettings):
    """Elastic settings"""

    url: str = Field("postgresql://<username>:<password>@<host>/<database_name>")
    name: str = Field("database_name")
    user: str = Field("app")
    password: str = Field("123qwe")
    host: str = Field("127.0.0.1")
    port: str = Field("5432")


class TracingConfig(BaseSettings):
    """Tracing settings"""

    host: str = Field("jaeger")
    port: int = Field(6831)
    need_to_launch: bool = Field(True)


class RpmConfig(BaseSettings):
    """Requests limiter settings"""

    limit: int = Field(20)
    need_to_launch: bool = Field(True)


class GoogleOauth(BaseSettings):
    """Google Oauth settings"""

    client_id: str = Field("some_value_from_provider")
    secret: str = Field("some_value_from_provider")


class YandexOauth(BaseSettings):
    """Google Oauth settings"""

    client_id: str = Field("some_value_from_provider")
    secret: str = Field("some_value_from_provider")


class VkOauth(BaseSettings):
    """Google Oauth settings"""

    client_id: str = Field("some_value_from_provider")
    secret: str = Field("some_value_from_provider")


class OauthApps(BaseSettings):
    """Project settings"""

    google: GoogleOauth = GoogleOauth()
    yandex: YandexOauth = YandexOauth()
    vk: VkOauth = VkOauth()
    secret_key: str = Field("some_key")
    apps: set = Field({"google", "yandex", "vk"})


class BaseConfig(BaseSettings):
    mds: MemoryDataStorageConfig = MemoryDataStorageConfig()
    db: DataBaseConfig = DataBaseConfig()
    main: MainConfig = MainConfig()
    tracing: TracingConfig = TracingConfig()
    rpm: RpmConfig = RpmConfig()
    oauth: OauthApps = OauthApps()

    class Config:
        env_prefix = "AUTH_"
        env_nested_delimiter = "__"
        env_file = "./../.env"
        env_file_encoding = "utf-8"


configs = BaseConfig()
