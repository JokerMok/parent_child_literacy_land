-- 1. 创建新数据库 (保留旧的 animal_card 不动，作为备份)
CREATE DATABASE IF NOT EXISTS parent_child_literacy DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE parent_child_literacy;

-- 2. 用户表 (完全采纳商业版设计)
CREATE TABLE t_users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    openid VARCHAR(100) NOT NULL UNIQUE,
    nickname VARCHAR(50) NOT NULL DEFAULT '',
    avatar VARCHAR(255) NOT NULL DEFAULT '',
    -- 会员体系
    is_vip TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '0-普通, 1-VIP',
    vip_expire_time DATETIME DEFAULT NULL COMMENT 'VIP到期时间',
    -- 声音克隆
    voice_id VARCHAR(100) DEFAULT '' COMMENT '火山引擎音色ID',
    -- 限制体系
    daily_upload_count INT UNSIGNED NOT NULL DEFAULT 0,
    last_upload_date DATE DEFAULT NULL,
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. 场景表 (融合版：补回了 description 和 sort_order)
CREATE TABLE t_scenes (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL DEFAULT '',
    description VARCHAR(255) DEFAULT '' COMMENT '保留了你的描述字段',
    cover VARCHAR(255) NOT NULL DEFAULT '',
    sort_order INT DEFAULT 0 COMMENT '保留了你的排序字段',
    
    user_id BIGINT UNSIGNED COMMENT 'NULL为官方',
    is_public TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '0-私有, 1-公开',
    status TINYINT UNSIGNED NOT NULL DEFAULT 1 COMMENT '0-审核中, 1-正常, 2-拒绝',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES t_users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. 卡片表 (融合版：弃用 card_key，改用标准外键)
CREATE TABLE t_cards (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    scene_id BIGINT UNSIGNED NOT NULL,
    name VARCHAR(50) NOT NULL DEFAULT '',
    image_url VARCHAR(255) NOT NULL,
    
    status TINYINT UNSIGNED NOT NULL DEFAULT 1 COMMENT '内容安全审核状态',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scene_id) REFERENCES t_scenes(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. 热区表 (融合版：改用 JSON 存坐标，加上拼音)
CREATE TABLE t_hotspots (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    card_id BIGINT UNSIGNED NOT NULL, -- 关联 t_cards.id
    text VARCHAR(100) NOT NULL,
    pinyin VARCHAR(100) DEFAULT '',
    audio_url VARCHAR(255) NOT NULL,
    
    -- 核心变化：用 JSON 存坐标 [left, top, width, height]
    rect_json JSON NOT NULL, 
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (card_id) REFERENCES t_cards(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. 订单表 (新增)
CREATE TABLE t_orders (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    order_no VARCHAR(50) NOT NULL UNIQUE,
    user_id BIGINT UNSIGNED NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '0-待付, 1-已付',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    pay_time DATETIME DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES t_users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. 声音样本表 (新增)
CREATE TABLE t_voice_samples (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    audio_url VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES t_users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;