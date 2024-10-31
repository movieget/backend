from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `book` ALTER COLUMN `status` SET DEFAULT '진행 중';
        ALTER TABLE `book` MODIFY COLUMN `status` VARCHAR(20) NOT NULL  COMMENT 'PENDING: 진행 중\nCOMPLETED: 완료\nCANCELLED: 취소' DEFAULT '진행 중';
        ALTER TABLE `movie` MODIFY COLUMN `genre` VARCHAR(5) NOT NULL  COMMENT 'ACTION: 액션\nDRAMA: 드라마\nCOMEDY: 코미디\nHORROR: 공포\nSCIFI: SF\nROMANCE: 로맨스\nADVENTURE: 모험\nANIMATION: 애니메이션\nFANTASY: 판타지\nCRIME: 범죄\nDOCUMENTARY: 다큐멘터리\nMYSTERY: 미스터리\nWAR: 전쟁\nTHRILLER: 스릴러' DEFAULT '액션';
        ALTER TABLE `movie` MODIFY COLUMN `status` VARCHAR(5) NOT NULL  COMMENT 'NOW_SHOWING: 상영 중\nCOMING_SOON: 개봉 예정\nENDED: 상영 종료' DEFAULT '상영 중';
        ALTER TABLE `movie` ALTER COLUMN `age_rating` SET DEFAULT 'ALL';
        ALTER TABLE `movie` MODIFY COLUMN `age_rating` VARCHAR(3) NOT NULL  COMMENT 'ALL: ALL\nTWELVE: 12\nFIFTEEN: 15\nEIGHTEEN: 18' DEFAULT 'ALL';
        ALTER TABLE `screen_info` MODIFY COLUMN `screen_id` INT NOT NULL;
        ALTER TABLE `screen_info` MODIFY COLUMN `end_time` TIME(6) NOT NULL;
        ALTER TABLE `screen_info` MODIFY COLUMN `movie_id` INT NOT NULL;
        ALTER TABLE `screen_info` MODIFY COLUMN `start_time` TIME(6) NOT NULL;
        ALTER TABLE `actor_image` ADD `actor_name` VARCHAR(255) NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `book` ALTER COLUMN `status` SET DEFAULT 'pending';
        ALTER TABLE `book` MODIFY COLUMN `status` VARCHAR(20) NOT NULL  COMMENT 'PENDING: pending\nCOMPLETED: completed\nCANCELED: canceled' DEFAULT 'pending';
        ALTER TABLE `movie` MODIFY COLUMN `genre` VARCHAR(5) NOT NULL  COMMENT 'ACTION: 액션\nWAR: 전쟁\nDRAMA: 드라마\nCOMEDY: 코미디\nHORROR: 공포\nSCIFI: SF\nROMANCE: 로맨스\nADVENTURE: 모험\nDOCUMENTARY: 다큐멘터리\nMYSTERY: 미스터리\nTHRILLER: 스릴러\nANIMATION: 애니메이션' DEFAULT '액션';
        ALTER TABLE `movie` MODIFY COLUMN `status` VARCHAR(5) NOT NULL  COMMENT 'NOW_SHOWING: 상영 중\nCOMING_SOON: 상영 예정\nENDED: 상영 종료' DEFAULT '상영 중';
        ALTER TABLE `movie` ALTER COLUMN `age_rating` SET DEFAULT 'All';
        ALTER TABLE `movie` MODIFY COLUMN `age_rating` VARCHAR(3) NOT NULL  COMMENT 'ALL: All\nAGE_12: 12\nAGE_15: 15\nAGE_18: 18' DEFAULT 'All';
        ALTER TABLE `actor_image` DROP COLUMN `actor_name`;
        ALTER TABLE `screen_info` MODIFY COLUMN `screen_id` INT;
        ALTER TABLE `screen_info` MODIFY COLUMN `end_time` DATETIME(6) NOT NULL;
        ALTER TABLE `screen_info` MODIFY COLUMN `movie_id` INT;
        ALTER TABLE `screen_info` MODIFY COLUMN `start_time` DATETIME(6) NOT NULL;"""
