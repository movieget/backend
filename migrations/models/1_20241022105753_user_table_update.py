from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ADD `image_url` VARCHAR(255);
        ALTER TABLE `user` ADD `oauth_provider` VARCHAR(20) NOT NULL;
        ALTER TABLE `user` ADD `kakao_id` VARCHAR(50)  UNIQUE;
        ALTER TABLE `user` ADD `birthday` VARCHAR(10);
        ALTER TABLE `user` ADD `phone_number` VARCHAR(16);
        ALTER TABLE `user` ADD `last_login` DATETIME(6);
        ALTER TABLE `user` ADD `is_active` BOOL NOT NULL  DEFAULT 1;
        ALTER TABLE `user` ADD `is_deleted` BOOL NOT NULL  DEFAULT 0;
        ALTER TABLE `user` MODIFY COLUMN `password_hash` VARCHAR(128);
        ALTER TABLE `user` MODIFY COLUMN `username` VARCHAR(50) NOT NULL;
        ALTER TABLE `user` MODIFY COLUMN `email` VARCHAR(100) NOT NULL;
        DROP TABLE IF EXISTS `basemodel`;
        ALTER TABLE `user` ADD UNIQUE INDEX `uid_user_kakao_i_49b9f2` (`kakao_id`);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` DROP INDEX `idx_user_kakao_i_49b9f2`;
        ALTER TABLE `user` DROP COLUMN `image_url`;
        ALTER TABLE `user` DROP COLUMN `oauth_provider`;
        ALTER TABLE `user` DROP COLUMN `kakao_id`;
        ALTER TABLE `user` DROP COLUMN `birthday`;
        ALTER TABLE `user` DROP COLUMN `phone_number`;
        ALTER TABLE `user` DROP COLUMN `last_login`;
        ALTER TABLE `user` DROP COLUMN `is_active`;
        ALTER TABLE `user` DROP COLUMN `is_deleted`;
        ALTER TABLE `user` MODIFY COLUMN `password_hash` VARCHAR(128) NOT NULL;
        ALTER TABLE `user` MODIFY COLUMN `username` VARCHAR(20) NOT NULL;
        ALTER TABLE `user` MODIFY COLUMN `email` VARCHAR(50) NOT NULL;
        ALTER TABLE `user` ADD UNIQUE INDEX `uid_user_nicknam_579938` (`nickname`);"""
