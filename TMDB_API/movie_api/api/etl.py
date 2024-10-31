from fastapi import APIRouter, HTTPException
from TMDB_API.movie_api.etl.etl_job import run_etl

router = APIRouter()


@router.post("/run/")
async def run_etl_endpoint():
    try:
        await run_etl()
        return {"message": "ETL 작업이 성공적으로 실행되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ETL 작업 실행 중 오류: {str(e)}")
