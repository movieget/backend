from tortoise import fields
from tortoise.models import Model


class ActorImage(Model):
    """
    영화 출연 배우의 이미지 정보를 저장하는 데이터베이스 모델

    Attributes:
        id (int): 이미지의 고유 식별자
        image_url (str): 배우 이미지의 URL
        movie_id (int): 관련 영화의 ID (외래 키)
        created_at (datetime): 레코드 생성 시간
        updated_at (datetime): 레코드 최종 수정 시간
    """

    id = fields.IntField(pk=True, description="이미지의 고유 식별자")
    image_url = fields.CharField(max_length=255, description="배우 이미지의 URL")
    movie_id = fields.IntField(null=True, description="관련 영화의 ID (외래 키)")

    created_at = fields.DatetimeField(auto_now_add=True, description="레코드 생성 시간")
    updated_at = fields.DatetimeField(auto_now=True, description="레코드 최종 수정 시간")

    class Meta:
        table = "actor_image"
        description = "영화 출연 배우의 이미지 정보"

    def __str__(self):
        return f"ActorImage {self.id} for Movie {self.movie_id}"
