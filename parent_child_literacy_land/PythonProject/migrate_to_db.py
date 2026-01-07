import pymysql
import json

# ---------------- 配置区 ----------------
DB_HOST = "175.178.2.155"  # 你的服务器IP
DB_USER = "jokermok"
DB_PASS = "jokermok00"  # <--- 改这里
DB_NAME = "animal_card"

# 你的文件路径
DB_JSON_PATH = "data/db.js"  # 注意：之前是js，可能需要手动把内容复制出来改成纯json格式，或者你手动录入场景
ALL_CONFIGS_PATH = "all_configs.json"


# ---------------------------------------

def get_conn():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME, autocommit=True)


def migrate_hotspots():
    print("🚀 开始迁移热区数据...")
    with open(ALL_CONFIGS_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    conn = get_conn()
    cursor = conn.cursor()

    # 清空旧数据
    cursor.execute("TRUNCATE TABLE t_hotspots")

    count = 0
    for card_key, items in data.items():
        for item in items:
            sql = "INSERT INTO t_hotspots (card_key, text, audio_url, rect_left, rect_top, rect_width, rect_height) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            rect = item['rect']
            cursor.execute(sql, (
                card_key,
                item['text'],
                item['audio'],
                rect[0], rect[1], rect[2], rect[3]
            ))
            count += 1

    print(f"✅ 成功插入 {count} 条热区数据！")
    conn.close()


# 这一步建议手动在 DBeaver 里录入场景数据(t_scenes)和卡片数据(t_cards)
# 因为 db.js 结构比较简单，只有10条，手动录入更稳妥。
# 这里只自动迁移最复杂的坐标数据。

if __name__ == "__main__":
    migrate_hotspots()