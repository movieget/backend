from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from TMDB_API.movie_api.etl.etl_job import run_etl  # ETL 파일 경로에 맞게 수정

app = FastAPI()

@app.on_event("startup")
@repeat_every(seconds=86400)  # 매 시간마다 ETL 작업 실행 24시간 기준
async def etl_scheduler():
    await run_etl()

