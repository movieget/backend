from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        SET @index_exists = (SELECT COUNT(1) FROM information_schema.statistics 
                             WHERE table_schema = DATABASE() 
                             AND table_name = 'user' 
                             AND index_name = 'idx_user_usernam_9987ab');
        SET @sql = IF(@index_exists > 0, 
                      'ALTER TABLE `user` DROP INDEX `idx_user_usernam_9987ab`', 
                      'SELECT 1');
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ADD UNIQUE INDEX `uid_user_usernam_9987ab` (`username`);"""
