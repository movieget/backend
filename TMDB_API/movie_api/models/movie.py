from tortoise import fields
from tortoise.models import Model

class Movie(Model):
    """
    영화 정보를 저장하는 데이터베이스 모델

    Attributes:
        id (int): 영화의 고유 식별자
        title (str): 영화 제목
        genre (str): 영화 장르
        release_date (date): 개봉일
        duration (int): 영화 상영 시간 (분)
        rating (float): 영화 평점
        status (str): 영화 상영 상태 (예: 상영 중, 개봉 예정, 종영)
        image_url (str): 영화 배경 이미지 URL
        poster_image_url (str): 영화 포스터 이미지 URL
        overview (str): 영화 줄거리
        trailer_url (str): 영화 예고편 URL
        age_rating (str): 영화 연령 등급
        created_at (datetime): 레코드 생성 시간
        updated_at (datetime): 레코드 최종 수정 시간
    """
    id = fields.IntField(pk=True, description="영화의 고유 식별자")
    title = fields.CharField(max_length=255, description="영화 제목")
    genre = fields.CharField(max_length=50, default="Action", description="영화 장르")
    release_date = fields.DateField(description="개봉일")
    duration = fields.IntField(description="영화 상영 시간 (분)")
    rating = fields.FloatField(description="영화 평점")
    status = fields.CharField(max_length=20, default="상영 중", description="영화 상영 상태")
    image_url = fields.CharField(max_length=255, description="영화 배경 이미지 URL")
    poster_image_url = fields.CharField(max_length=255, description="영화 포스터 이미지 URL")
    overview = fields.TextField(description="영화 줄거리")
    trailer_url = fields.CharField(max_length=255, null=True, default="", description="영화 예고편 URL")
    age_rating = fields.CharField(max_length=10, default="all", description="영화 연령 등급")

    created_at = fields.DatetimeField(auto_now_add=True, description="레코드 생성 시간")
    updated_at = fields.DatetimeField(auto_now=True, description="레코드 최종 수정 시간")

    class Meta:
        table = "movies"
        description = "영화 정보 저장 테이블"

    def __str__(self):
        return f"{self.title} ({self.release_date.year})"