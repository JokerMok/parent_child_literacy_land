## 问题分析

通过分析小程序运行日志和代码，发现以下主要问题：

### 1. URL前缀不匹配
- 小程序请求的API路径：`http://175.178.2.155/api/...`
- FastAPI实际服务路径：`http://175.178.2.155/api/v1/...`
- 原因：FastAPI配置了`/api/v1`前缀，而小程序使用了`/api`前缀

### 2. 端点命名不匹配
- 小程序调用：`/api/scenes`（复数）
- FastAPI实现：`/api/v1/scene/`（单数）
- 其他类似问题：`/api/card/...` vs `/api/v1/card/...`

### 3. 缺失关键端点
小程序调用但FastAPI未实现的端点：
- `/api/config/{cardKey}` - 获取卡片配置
- `/api/upload` - 上传图片
- `/api/analyze` - 分析图片获取热区
- `/api/admin/save_hotspots` - 保存热区
- `/api/system/config` - 获取系统配置
- `/api/user/create_card` - 创建卡片
- `/api/card/update_name` - 更新卡片名称

### 4. 数据模型缺失
- Card模型缺少`card_key`字段，导致无法根据小程序传递的`cardKey`查询数据

### 5. 无效请求
- 当用户未登录时，小程序调用`/api/user/0`，导致404错误

## 修复计划

### 1. 统一API前缀
- **方案**：修改FastAPI配置，将前缀从`/api/v1`改为`/api`
- **文件**：`app/core/config.py`
- **修改**：将`API_V1_STR`从`/api/v1`改为`/api`

### 2. 修复端点命名
- **方案**：调整FastAPI端点路径，使其与小程序调用匹配
- **文件**：`app/api/api_v1/api.py`
- **修改**：调整路由前缀，如将`/scene`改为`/scenes`

### 3. 实现缺失端点
- **方案**：根据小程序需求实现所有缺失的API端点
- **文件**：
  - `app/api/api_v1/endpoints/config.py` - 实现`/api/config/{cardKey}`
  - `app/api/api_v1/endpoints/upload.py` - 实现`/api/upload`和`/api/analyze`
  - `app/api/api_v1/endpoints/admin.py` - 实现`/api/admin/save_hotspots`
  - `app/api/api_v1/endpoints/system.py` - 实现`/api/system/config`
  - 更新`card.py` - 实现`/api/user/create_card`和`/api/card/update_name`

### 4. 更新数据模型
- **方案**：为Card模型添加`card_key`字段
- **文件**：`app/models/card.py`
- **修改**：添加`card_key`列，支持根据卡片key查询

### 5. 优化错误处理
- **方案**：在小程序和后端添加适当的错误处理
- **修改**：
  - 小程序：添加空值检查，避免调用无效的API路径
  - 后端：添加适当的404和错误响应

## 预期效果

修复后，小程序将能够成功调用所有API端点，解决当前的404错误，使亲子识字乐园应用能够正常运行。