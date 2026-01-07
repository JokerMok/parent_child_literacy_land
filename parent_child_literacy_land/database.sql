-- 亲子识字乐园数据库建表SQL
-- Version: 1.0.0 Commercial
-- Database: MySQL 8.0

-- 创建数据库
CREATE DATABASE IF NOT EXISTS parent_child_literacy DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE parent_child_literacy;

-- -----------------------------
-- 表结构 t_users (用户表)
-- -----------------------------
CREATE TABLE IF NOT EXISTS t_users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    openid VARCHAR(100) NOT NULL UNIQUE COMMENT '微信OpenID',
    nickname VARCHAR(50) NOT NULL DEFAULT '' COMMENT '用户昵称',
    avatar VARCHAR(255) NOT NULL DEFAULT '' COMMENT '用户头像URL',
    is_vip TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否VIP: 0-普通用户, 1-VIP用户',
    vip_expire_time DATETIME NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT 'VIP到期时间',
    voice_id VARCHAR(100) NOT NULL DEFAULT '' COMMENT '克隆音色ID',
    daily_upload_count INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '今日上传图片数量',
    last_upload_date DATE NOT NULL DEFAULT '1970-01-01' COMMENT '最后上传日期',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_openid (openid),
    INDEX idx_is_vip (is_vip),
    INDEX idx_vip_expire_time (vip_expire_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- -----------------------------
-- 表结构 t_voice_samples (声音样本表)
-- -----------------------------
CREATE TABLE IF NOT EXISTS t_voice_samples (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '样本ID',
    user_id BIGINT UNSIGNED NOT NULL COMMENT '所属用户ID',
    audio_url VARCHAR(255) NOT NULL COMMENT '原始录音URL',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_user_id (user_id),
    FOREIGN KEY (user_id) REFERENCES t_users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='声音样本表';

-- -----------------------------
-- 表结构 t_orders (订单表)
-- -----------------------------
CREATE TABLE IF NOT EXISTS t_orders (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '订单ID',
    order_no VARCHAR(50) NOT NULL UNIQUE COMMENT '订单号',
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    amount DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '订单金额',
    status TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '订单状态: 0-待支付, 1-已支付, 2-已取消',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    pay_time DATETIME NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '支付时间',
    INDEX idx_user_id (user_id),
    INDEX idx_order_no (order_no),
    INDEX idx_status (status),
    FOREIGN KEY (user_id) REFERENCES t_users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='订单表';

-- -----------------------------
-- 表结构 t_scenes (场景表)
-- -----------------------------
CREATE TABLE IF NOT EXISTS t_scenes (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '场景ID',
    title VARCHAR(100) NOT NULL DEFAULT '' COMMENT '场景标题',
    cover VARCHAR(255) NOT NULL DEFAULT '' COMMENT '场景封面URL',
    user_id BIGINT UNSIGNED NOT NULL COMMENT '创建者ID',
    is_public TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否公开: 0-私有, 1-公开',
    status TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '状态: 0-待审核, 1-已通过, 2-已拒绝',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_user_id (user_id),
    INDEX idx_is_public (is_public),
    INDEX idx_status (status),
    FOREIGN KEY (user_id) REFERENCES t_users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='场景表';

-- -----------------------------
-- 表结构 t_cards (卡片表)
-- -----------------------------
CREATE TABLE IF NOT EXISTS t_cards (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '卡片ID',
    scene_id BIGINT UNSIGNED NOT NULL COMMENT '所属场景ID',
    image_url VARCHAR(255) NOT NULL COMMENT '卡片图片URL',
    name VARCHAR(50) NOT NULL DEFAULT '' COMMENT '卡片名称',
    status TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '状态: 0-待审核, 1-已通过, 2-已拒绝',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_scene_id (scene_id),
    INDEX idx_status (status),
    FOREIGN KEY (scene_id) REFERENCES t_scenes(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='卡片表';

-- -----------------------------
-- 表结构 t_hotspots (热点表)
-- -----------------------------
CREATE TABLE IF NOT EXISTS t_hotspots (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '热点ID',
    card_id BIGINT UNSIGNED NOT NULL COMMENT '所属卡片ID',
    text VARCHAR(100) NOT NULL DEFAULT '' COMMENT '热点文字',
    pinyin VARCHAR(100) NOT NULL DEFAULT '' COMMENT '拼音',
    audio_url VARCHAR(255) NOT NULL DEFAULT '' COMMENT '音频URL',
    rect_json TEXT NOT NULL COMMENT '热点矩形坐标JSON',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_card_id (card_id),
    FOREIGN KEY (card_id) REFERENCES t_cards(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='热点表';
