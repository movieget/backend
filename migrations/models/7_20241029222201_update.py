from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `book` DROP COLUMN `movie_price`;
        ALTER TABLE `book` MODIFY COLUMN `status` VARCHAR(20) NOT NULL  COMMENT 'PENDING: pending\nCOMPLETED: completed\nCANCELED: canceled' DEFAULT 'pending';
        ALTER TABLE `movie` MODIFY COLUMN `age_rating` VARCHAR(3) NOT NULL  COMMENT 'ALL: All\nAGE_12: 12\nAGE_15: 15\nAGE_18: 18' DEFAULT 'All';
        ALTER TABLE `payment` ADD `orderId` VARCHAR(50) NOT NULL;
        ALTER TABLE `payment` ADD `paymentKey` VARCHAR(50) NOT NULL;
        ALTER TABLE `payment` ADD `amount` INT NOT NULL;
        ALTER TABLE `payment` DROP COLUMN `payment_time`;
        ALTER TABLE `payment` DROP COLUMN `payment_method`;
        ALTER TABLE `payment` DROP COLUMN `payment_amount`;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `book` ADD `movie_price` SMALLINT NOT NULL  COMMENT 'adult: 14000\nchild: 12000' DEFAULT 14000;
        ALTER TABLE `book` MODIFY COLUMN `status` VARCHAR(20) NOT NULL  COMMENT 'PENDING: pending\nCOMPLETED: completed\nCANCELLED: cancelled' DEFAULT 'pending';
        ALTER TABLE `movie` MODIFY COLUMN `age_rating` VARCHAR(3) NOT NULL  COMMENT 'ALL: All\nAGE_12: 12\nAGE_15: 15\nAGE_18: 18\nAGE_19: 19' DEFAULT 'All';
        ALTER TABLE `payment` ADD `payment_time` DATETIME(6) NOT NULL;
        ALTER TABLE `payment` ADD `payment_method` VARCHAR(20) NOT NULL  COMMENT 'CREDIT_CARD: credit_card\nDEBIT_CARD: debit_card\nBANK_TRANSFER: bank_transfer\nPAYPAL: paypal';
        ALTER TABLE `payment` ADD `payment_amount` DECIMAL(10,2) NOT NULL;
        ALTER TABLE `payment` DROP COLUMN `orderId`;
        ALTER TABLE `payment` DROP COLUMN `paymentKey`;
        ALTER TABLE `payment` DROP COLUMN `amount`;"""
