from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE `book_seat` (
    `book_id` INT NOT NULL REFERENCES `book` (`id`) ON DELETE CASCADE,
    `seat_id` INT NOT NULL REFERENCES `seat` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `book_seat`;"""
