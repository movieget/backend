from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `book` ALTER COLUMN `status` SET DEFAULT '진행중';
        ALTER TABLE `book` MODIFY COLUMN `status` VARCHAR(20) NOT NULL  COMMENT 'PENDING: 진행중\nCOMPLETED: 완료\nCANCELLED: 취소' DEFAULT '진행중';
        CREATE TABLE IF NOT EXISTS `point_history` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `change_type` VARCHAR(10) NOT NULL,
    `points` INT NOT NULL,
    `description` VARCHAR(30) NOT NULL,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `payment_id` INT,
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_point_hi_payment_dbe6dd6e` FOREIGN KEY (`payment_id`) REFERENCES `payment` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_point_hi_user_44dfc355` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `book` ALTER COLUMN `status` SET DEFAULT '진행 중';
        ALTER TABLE `book` MODIFY COLUMN `status` VARCHAR(20) NOT NULL  COMMENT 'PENDING: 진행 중\nCOMPLETED: 완료\nCANCELLED: 취소' DEFAULT '진행 중';
        DROP TABLE IF EXISTS `point_history`;"""
