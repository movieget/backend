from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `review` ALTER COLUMN `rating` SET DEFAULT 0;
        ALTER TABLE `review` MODIFY COLUMN `rating` SMALLINT NOT NULL  COMMENT 'no_star: 0\none_star: 1\ntwo_star: 2\nthree_star: 3\nfour_star: 4\nfive_star: 5' DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `review` MODIFY COLUMN `rating` VARCHAR(20) NOT NULL  COMMENT 'no_star: 0\none_star: 1\ntwo_star: 2\nthree_star: 3\nfour_star: 4\nfive_star: 5' DEFAULT '0';
        ALTER TABLE `review` ALTER COLUMN `rating` SET DEFAULT '0';"""
