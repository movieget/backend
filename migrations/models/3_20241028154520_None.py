from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `user` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `password_hash` VARCHAR(128),
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `nickname` VARCHAR(50) NOT NULL,
    `phone_number` VARCHAR(16),
    `image_url` VARCHAR(255),
    `oauth_provider` VARCHAR(20) NOT NULL,
    `birthday` VARCHAR(10),
    `kakao_id` VARCHAR(50)  UNIQUE,
    `is_active` BOOL NOT NULL  DEFAULT 1,
    `is_deleted` BOOL NOT NULL  DEFAULT 0,
    `last_login` DATETIME(6)
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
    `location_id` INT NOT NULL,
    CONSTRAINT `fk_cinema_location_9252e6c1` FOREIGN KEY (`location_id`) REFERENCES `location` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `movie` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(30) NOT NULL,
    `genre` VARCHAR(7) NOT NULL  COMMENT 'ACTION: ACTION\nDRAMA: DRAMA\nCOMEDY: COMEDY\nHORROR: HORROR\nSCIFI: SCIFI\nROMANCE: ROMANCE' DEFAULT 'ACTION',
    `release_data` DATE NOT NULL,
    `duration` INT NOT NULL,
    `rating` INT NOT NULL,
    `status` VARCHAR(5) NOT NULL  COMMENT 'NOW_SHOWING: 상영 중\nCOMING_SOON: 상영 예정\nENDED: 상영 종료' DEFAULT '상영 중',
    `image_url` VARCHAR(100) NOT NULL,
    `poster_image_url` VARCHAR(255) NOT NULL,
    `overview` LONGTEXT NOT NULL,
    `trailer_url` VARCHAR(100) NOT NULL,
    `age_rating` VARCHAR(3) NOT NULL  COMMENT 'ALL: all\nAGE_12: 12\nAGE_15: 15\nAGE_18: 18' DEFAULT 'all'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `favorite` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `added_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `movie_id` INT,
    `user_id` INT,
    CONSTRAINT `fk_favorite_movie_e4ba1ebb` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_favorite_user_babde07c` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `review` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(255) NOT NULL,
    `username` VARCHAR(20) NOT NULL,
    `contents` LONGTEXT NOT NULL,
    `review_image_url` VARCHAR(50) NOT NULL,
    `rating` VARCHAR(20) NOT NULL  COMMENT 'no_star: 0\none_star: 1\ntwo_star: 2\nthree_star: 3\nfour_star: 4\nfive_star: 5' DEFAULT '0',
    `registration_date` DATE NOT NULL,
    `movie_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_review_movie_91a1e22d` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_review_user_c0877390` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `screen` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `screen_number` VARCHAR(30) NOT NULL,
    `total_seats` INT NOT NULL,
    `cinema_id` INT,
    CONSTRAINT `fk_screen_cinema_81cfe596` FOREIGN KEY (`cinema_id`) REFERENCES `cinema` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `screen_info` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `screening_date` DATE NOT NULL,
    `start_time` DATETIME(6) NOT NULL,
    `end_time` DATETIME(6) NOT NULL,
    `movie_id` INT,
    `screen_id` INT,
    CONSTRAINT `fk_screen_i_movie_d5bf129e` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_screen_i_screen_96df0003` FOREIGN KEY (`screen_id`) REFERENCES `screen` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `book` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `book_time` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `status` VARCHAR(20) NOT NULL  COMMENT 'PENDING: 진행 중\nCOMPLETED: 완료\nCANCELLED: 취소' DEFAULT '진행 중',
    `movie_price` SMALLINT NOT NULL  COMMENT 'adult: 14000\nchild: 12000',
    `adult_count` INT NOT NULL  DEFAULT 0,
    `child_count` INT NOT NULL  DEFAULT 0,
    `screen_info_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_book_screen_i_78612a29` FOREIGN KEY (`screen_info_id`) REFERENCES `screen_info` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_book_user_325b1912` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `payment` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `payment_amount` DECIMAL(10,2) NOT NULL,
    `payment_method` VARCHAR(20) NOT NULL  COMMENT 'CREDIT_CARD: credit_card\nDEBIT_CARD: debit_card\nBANK_TRANSFER: bank_transfer\nPAYPAL: paypal',
    `payment_time` DATETIME(6) NOT NULL,
    `book_id` INT NOT NULL,
    `user_id` INT,
    CONSTRAINT `fk_payment_book_3c671b0b` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_payment_user_3d4ede6e` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `alert` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `message` VARCHAR(50) NOT NULL,
    `notification_type` VARCHAR(20) NOT NULL,
    `book_id` INT NOT NULL,
    `payment_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_alert_book_8db5c475` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_alert_payment_f405eb4e` FOREIGN KEY (`payment_id`) REFERENCES `payment` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_alert_user_2bac072c` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
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
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `refund_amount` DECIMAL(10,2) NOT NULL,
    `refund_status` VARCHAR(20) NOT NULL  COMMENT 'PENDING: 보류중\nAPPROVED: 승인됨\nREJECTED: 거부됨\nCOMPLETED: 완료됨',
    `refund_time` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `payment_id` INT  UNIQUE,
    CONSTRAINT `fk_refund_payment_336c5ccc` FOREIGN KEY (`payment_id`) REFERENCES `payment` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `seat` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `seat_number` INT NOT NULL,
    `is_selected` BOOL NOT NULL  DEFAULT 0,
    `row` VARCHAR(10) NOT NULL,
    `column` INT NOT NULL,
    `screen_id` INT NOT NULL,
    CONSTRAINT `fk_seat_screen_24e3c4ac` FOREIGN KEY (`screen_id`) REFERENCES `screen` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `book_seat` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `book_id` INT NOT NULL,
    `seat_id` INT NOT NULL,
    CONSTRAINT `fk_book_sea_book_16d52531` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_book_sea_seat_f37ff7ea` FOREIGN KEY (`seat_id`) REFERENCES `seat` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `actor_image` (
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `image_url` VARCHAR(255) NOT NULL,
    `movie_id` INT,
    CONSTRAINT `fk_actor_im_movie_d17833d7` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`) ON DELETE CASCADE
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
