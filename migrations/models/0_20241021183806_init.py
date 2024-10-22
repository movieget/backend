from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `users` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `username` VARCHAR(20) NOT NULL UNIQUE,
    `password_hash` VARCHAR(128) NOT NULL,
    `email` VARCHAR(50) NOT NULL UNIQUE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `location` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `spot` VARCHAR(20) NOT NULL,
    `longitude` DOUBLE,
    `latitude` DOUBLE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `cinema` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `cinema_name` VARCHAR(30) NOT NULL UNIQUE,
    `location_id_id` INT NOT NULL UNIQUE,
    CONSTRAINT `fk_cinema_location_4b7c27e1` FOREIGN KEY (`location_id_id`) REFERENCES `location` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `movie` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(30) NOT NULL,
    `genre` VARCHAR(7) NOT NULL  COMMENT 'ACTION: Action\nDRAMA: Drama\nCOMEDY: Comedy\nHORROR: Horror\nSCIFI: Sci-Fi\nROMANCE: Romance' DEFAULT 'Action',
    `release_data` DATE NOT NULL,
    `duration` INT NOT NULL,
    `rating` INT NOT NULL,
    `status` VARCHAR(5) NOT NULL  COMMENT 'NOW_SHOWING: 상영 중\nCOMING_SOON: 상영 예정\nENDED: 상영 종료' DEFAULT '상영 중',
    `image_url` VARCHAR(100) NOT NULL,
    `poster_image_url` VARCHAR(100) NOT NULL,
    `actor_Image_url` VARCHAR(100) NOT NULL,
    `overview` LONGTEXT NOT NULL,
    `trailer_url` VARCHAR(100) NOT NULL,
    `age_rating` SMALLINT NOT NULL  COMMENT 'basic: 12\nmiddle: 15\nhigh: 18' DEFAULT 12
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `favorite` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `added_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `movie_id_id` INT,
    `user_id_id` INT,
    CONSTRAINT `fk_favorite_movie_da5aabec` FOREIGN KEY (`movie_id_id`) REFERENCES `movie` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_favorite_users_c90a8c86` FOREIGN KEY (`user_id_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `review` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(255) NOT NULL,
    `username` VARCHAR(20) NOT NULL,
    `contents` LONGTEXT NOT NULL,
    `review_image_url` VARCHAR(50) NOT NULL,
    `rating` VARCHAR(20) NOT NULL  COMMENT 'no_star: ☆☆☆☆☆\none_star: ★☆☆☆☆\ntwo_star: ★★☆☆☆\nthree_star: ★★★☆☆\nfour_star: ★★★★☆\nfive_star: ★★★★★' DEFAULT '☆☆☆☆☆',
    `registration_date` DATE NOT NULL,
    `movie_id_id` INT NOT NULL,
    `user_id_id` INT NOT NULL,
    CONSTRAINT `fk_review_movie_07da6114` FOREIGN KEY (`movie_id_id`) REFERENCES `movie` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_review_users_ff0d24ab` FOREIGN KEY (`user_id_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `screen` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `screen_number` VARCHAR(30) NOT NULL,
    `total_seats` INT NOT NULL,
    `cinema_id_id` INT,
    CONSTRAINT `fk_screen_cinema_bebd1cd2` FOREIGN KEY (`cinema_id_id`) REFERENCES `cinema` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `screen_info` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `start_time` DATETIME(6) NOT NULL,
    `end_time` DATETIME(6) NOT NULL,
    `movie_id_id` INT,
    `screen_id_id` INT,
    CONSTRAINT `fk_screen_i_movie_67c18024` FOREIGN KEY (`movie_id_id`) REFERENCES `movie` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_screen_i_screen_4ca416eb` FOREIGN KEY (`screen_id_id`) REFERENCES `screen` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `book` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `book_time` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `status` VARCHAR(20) NOT NULL  COMMENT 'PENDING: 진행 중\nCOMPLETED: 완료\nCANCELLED: 취소' DEFAULT '진행 중',
    `movie_price` VARCHAR(10) NOT NULL  COMMENT 'adult: 14000\nchild: 12000',
    `adult_count` INT NOT NULL  DEFAULT 0,
    `child_count` INT NOT NULL  DEFAULT 0,
    `screen_info_id_id` INT NOT NULL,
    `user_id_id` INT NOT NULL,
    CONSTRAINT `fk_book_screen_i_95fc6242` FOREIGN KEY (`screen_info_id_id`) REFERENCES `screen_info` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_book_users_c03eb91a` FOREIGN KEY (`user_id_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `payment` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `payment_amount` DECIMAL(10,2) NOT NULL,
    `payment_method` VARCHAR(20) NOT NULL  COMMENT 'CREDIT_CARD: credit_card\nDEBIT_CARD: debit_card\nBANK_TRANSFER: bank_transfer\nPAYPAL: paypal',
    `payment_time` DATETIME(6) NOT NULL,
    `book_id_id` INT NOT NULL,
    `user_id_id` INT,
    CONSTRAINT `fk_payment_book_40d45257` FOREIGN KEY (`book_id_id`) REFERENCES `book` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_payment_users_857c695e` FOREIGN KEY (`user_id_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `alert` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `message` VARCHAR(50) NOT NULL,
    `notification_type` VARCHAR(20) NOT NULL,
    `book_id_id` INT NOT NULL,
    `payment_id_id` INT NOT NULL,
    `user_id_id` INT NOT NULL,
    CONSTRAINT `fk_alert_book_443d6939` FOREIGN KEY (`book_id_id`) REFERENCES `book` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_alert_payment_57c877f8` FOREIGN KEY (`payment_id_id`) REFERENCES `payment` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_alert_users_fe3f756d` FOREIGN KEY (`user_id_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `payment_history` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `contents` VARCHAR(20) NOT NULL,
    `payment_id` INT,
    CONSTRAINT `fk_payment__payment_e71bc751` FOREIGN KEY (`payment_id`) REFERENCES `payment` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `refund` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `refund_amount` DECIMAL(10,2) NOT NULL,
    `refund_status` VARCHAR(20) NOT NULL  COMMENT 'PENDING: 보류중\nAPPROVED: 승인됨\nREJECTED: 거부됨\nCOMPLETED: 완료됨',
    `refund_time` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `payment_id` INT  UNIQUE,
    CONSTRAINT `fk_refund_payment_336c5ccc` FOREIGN KEY (`payment_id`) REFERENCES `payment` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
