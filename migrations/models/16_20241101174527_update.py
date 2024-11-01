from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `review` MODIFY COLUMN `review_image_url` VARCHAR(255);
        DROP TABLE IF EXISTS `point_history`;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `review` MODIFY COLUMN `review_image_url` VARCHAR(50) NOT NULL;"""
