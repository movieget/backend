from pydantic import BaseModel


class KakaoOauthResponse(BaseModel):
    access_token: str
    id: int
    profile_image_url: str


class KakaoOauthErrorResponse(BaseModel):
    error: str
