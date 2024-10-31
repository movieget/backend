from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` DROP COLUMN `point`;
        ALTER TABLE `favorite` ADD `is_liked` BOOL NOT NULL  DEFAULT 0;
        ALTER TABLE `actor_image` ADD `actor_name` VARCHAR(255) NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ADD `point` INT NOT NULL;
        ALTER TABLE `favorite` DROP COLUMN `is_liked`;
        ALTER TABLE `actor_image` DROP COLUMN `actor_name`;"""
