import aiomysql
import logging
import asyncio
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 환경 변수에서 데이터베이스 연결 정보 가져오기
TMDB_HOST = os.getenv('TMDB_HOST')
TMDB_PORT = int(os.getenv('TMDB_PORT'))
TMDB_USER = os.getenv('TMDB_USER')
TMDB_PASSWORD = os.getenv('TMDB_PASSWORD')
TMDB_DB = os.getenv('TMDB_DB')

MOVIE_HOST = os.getenv('MOVIE_HOST')
MOVIE_PORT = int(os.getenv('MOVIE_PORT'))
MOVIE_USER = os.getenv('MOVIE_USER')
MOVIE_PASSWORD = os.getenv('MOVIE_PASSWORD')
MOVIE_DB = os.getenv('MOVIE_DB')

async def connect_to_database(host, port, user, password, db):
    """
    데이터베이스 연결 함수
    지정된 호스트, 포트, 사용자, 비밀번호, 데이터베이스 이름으로 데이터베이스에 연결합니다.
    """
    try:
        pool = await aiomysql.create_pool(host=host, port=port, user=user, password=password, db=db, autocommit=False)
        logger.info(f"Successfully connected to database: {db}")
        return pool
    except Exception as e:
        logger.error(f"Failed to connect to database {db}: {e}")
        raise

async def fetch_data(cursor, table):
    """
    데이터 조회 함수
    지정된 테이블에서 모든 데이터를 조회합니다.
    """
    try:
        await cursor.execute(f"SELECT * FROM {table}")
        data = await cursor.fetchall()
        logger.info(f"Fetched {len(data)} records from {table}")
        return data
    except Exception as e:
        logger.error(f"Error fetching data from {table}: {e}")
        raise

async def insert_movies(cursor, data):
    """
    영화 데이터 삽입 함수
    영화 데이터를 movie 테이블에 삽입하거나 업데이트합니다.
    """
    try:
        sql = """
        INSERT INTO movie (id, created_at, updated_at, title, genre, release_data, 
        duration, rating, status, image_url, poster_image_url, overview, trailer_url, age_rating, actor_Image_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        updated_at = VALUES(updated_at), title = VALUES(title), genre = VALUES(genre),
        release_data = VALUES(release_data), duration = VALUES(duration), rating = VALUES(rating),
        status = VALUES(status), image_url = VALUES(image_url), poster_image_url = VALUES(poster_image_url),
        overview = VALUES(overview), trailer_url = VALUES(trailer_url), age_rating = VALUES(age_rating),
        actor_Image_url = VALUES(actor_Image_url)
        """
        processed_data = []
        for movie in data:
            processed_movie = (
                movie[0],  # id
                movie[1],  # created_at
                movie[2],  # updated_at
                movie[3][:30],  # 제목 (30자로 제한)
                movie[4][:7],  # 장르 (7자로 제한)
                movie[5],  # 개봉일
                movie[6],  # 상영 시간
                int(float(movie[7])),  # 평점 (소수점을 정수로 변환)
                movie[8][:5],  # 상영 상태 (5자로 제한)
                movie[9][:100],  # 이미지 URL (100자로 제한)
                movie[10][:100],  # 포스터 이미지 URL (100자로 제한)
                movie[11],  # 줄거리
                (movie[12] or '')[:100],  # 예고편 URL (100자로 제한, 없으면 빈 문자열)
                movie[13][:3],  # 연령 등급 (3자로 제한)
                ''  # 배우 이미지 URL (기본값으로 빈 문자열 사용)
            )
            processed_data.append(processed_movie)

        await cursor.executemany(sql, processed_data)
        logger.info(f"Inserted/Updated {len(processed_data)} movies")
    except Exception as e:
        logger.error(f"Error inserting movies: {e}")
        raise

async def insert_actor_images(cursor, data):
    """
    배우 이미지 데이터 삽입 함수
    배우 이미지 데이터를 actor_image 테이블에 삽입하거나 업데이트합니다.
    """
    try:
        sql = """
        INSERT INTO actor_image (id, image_url, movie_id, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        image_url = VALUES(image_url), movie_id = VALUES(movie_id), 
        updated_at = VALUES(updated_at)
        """
        await cursor.executemany(sql, data)
        logger.info(f"Inserted/Updated {len(data)} actor images")
    except Exception as e:
        logger.error(f"Error inserting actor images: {e}")
        raise

async def migrate_data():
    """
    데이터 마이그레이션 함수
    TMDB_API 데이터베이스에서 movie 데이터베이스로 데이터를 마이그레이션합니다.
    """
    tmdb_pool = None
    movie_pool = None
    try:
        tmdb_pool = await connect_to_database(TMDB_HOST, TMDB_PORT, TMDB_USER, TMDB_PASSWORD, TMDB_DB)
        movie_pool = await connect_to_database(MOVIE_HOST, MOVIE_PORT, MOVIE_USER, MOVIE_PASSWORD, MOVIE_DB)

        async with tmdb_pool.acquire() as tmdb_conn, movie_pool.acquire() as movie_conn:
            async with tmdb_conn.cursor() as tmdb_cursor, movie_conn.cursor() as movie_cursor:
                # 영화 데이터 마이그레이션
                movies = await fetch_data(tmdb_cursor, "movies")
                await insert_movies(movie_cursor, movies)

                # 배우 이미지 데이터 마이그레이션
                actor_images = await fetch_data(tmdb_cursor, "actor_image")
                await insert_actor_images(movie_cursor, actor_images)

                # 변경사항 커밋
                await movie_conn.commit()
                logger.info("All changes committed successfully")

        logger.info("Data migration completed successfully.")

    except Exception as e:
        logger.error(f"An error occurred during migration: {e}")
        if 'movie_conn' in locals():
            await movie_conn.rollback()
            logger.info("Changes rolled back due to error")
    finally:
        if tmdb_pool:
            tmdb_pool.close()
            await tmdb_pool.wait_closed()
        if movie_pool:
            movie_pool.close()
            await movie_pool.wait_closed()

async def run_etl():
    """
    ETL 프로세스 실행 함수
    전체 ETL(추출, 변환, 적재) 프로세스를 실행합니다.
    """
    try:
        logger.info("Starting ETL process")
        await migrate_data()
        logger.info("ETL process completed successfully.")
    except Exception as e:
        logger.error(f"ETL process failed: {str(e)}")
        raise

if __name__ == "__main__":
    """
    메인 실행 부분
    스크립트가 직접 실행될 때 ETL 프로세스를 시작합니다.
    """
    asyncio.run(run_etl())