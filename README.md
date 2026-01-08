# 亲子识字乐园 (Parent-Child Literacy Land)

## 项目简介
一款商业级亲子识字小程序。核心壁垒是'AI声音克隆'（只需父母录制一次声音，即可用父母音色朗读所有单词）。商业模式为会员订阅制。

## 技术栈
- **前端**: 微信小程序原生开发 (WXML, WXSS, JS)
- **后端**: Python 3.10+, FastAPI, Uvicorn, SQLAlchemy/PyMySQL
- **数据库**: MySQL 8.0
- **AI 视觉**: 阿里云 Qwen-VL (视觉识别)
- **AI 语音**: 火山引擎 CosyVoice / GPT-SoVITS API (声音克隆与合成)
- **部署**: Windows Server + Nginx
- **安全**: 微信官方内容安全接口 (msgSecCheck, imgSecCheck)

## 功能模块

### 微信小程序客户端
- **登录授权**: 微信登录并同步OpenID, JWT Token 鉴权, 用户资料完善
- **声音克隆中心**: 录音引导, 录音功能, 模型训练, 试听功能
- **UGC创作流程**: 上传图片, AI智能识别, 可视化编辑, 提交保存
- **会员收银台**: 会员权益展示, 支付接口对接, 订单状态轮询

### 后端服务
- **API接口**: 声音克隆, 语音合成, 内容安全检测, 订单管理
- **业务逻辑**: 上传限制, 语音路由, VIP权限管理

## 安装和运行

### 1. 数据库配置
- 创建MySQL数据库
- 执行 `database.sql` 文件中的SQL语句创建表结构

### 2. 环境配置
- 复制 `.env.example` 为 `.env` 并修改配置

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 运行后端服务
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 访问API文档
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## 核心功能说明

### 声音克隆
1. 用户上传5-10秒录音
2. 后端调用火山引擎API克隆声音
3. 返回voice_id并绑定到用户
4. 用户可以使用克隆的声音生成任意文本的语音

### TTS语音合成
- **VIP用户**: 如果有克隆音色，使用克隆音；否则使用Edge-TTS
- **普通用户**: 只能使用Edge-TTS

### 上传限制
- **普通用户**: 每日限上传1张图片
- **VIP用户**: 无限上传图片

## 开发说明

### AI服务集成
- 视觉识别: 阿里云Qwen-VL API
- 声音克隆与合成: 火山引擎CosyVoice/GPT-SoVITS API（预留接口）

### 内容安全
- 所有用户输入的文字、上传的图片，入库前必须经过微信安全接口检测
- 违规内容直接拒绝保存

## 许可证
Commercial (High-End)
