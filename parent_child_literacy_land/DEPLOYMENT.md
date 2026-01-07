# 亲子识字乐园项目部署指南

## 部署环境
- **服务器**: 腾讯云CVM (Windows Server 2022 Datacenter)
- **Web服务器**: Nginx for Windows
- **应用服务器**: Uvicorn (作为Windows服务运行)
- **数据库**: MySQL 8.0
- **Python**: 3.10+

## 部署流程

### 1. 服务器准备

#### 1.1 登录服务器
使用远程桌面连接登录Windows Server：
- 打开「远程桌面连接」
- 输入服务器的公网IP地址
- 使用管理员账号和密码登录

#### 1.2 安装必要软件

##### 1.2.1 安装Git
1. 下载Git for Windows：https://git-scm.com/download/win
2. 运行安装程序，选择默认安装选项即可

##### 1.2.2 安装Python 3.10
1. 下载Python 3.10：https://www.python.org/ftp/python/3.10.12/python-3.10.12-amd64.exe
2. 运行安装程序，勾选「Add Python 3.10 to PATH」
3. 选择「Customize installation」，然后点击「Next」
4. 勾选所有可选功能，点击「Next」
5. 选择安装路径（建议使用默认路径），点击「Install」
6. 安装完成后，验证Python安装：
   - 打开命令提示符
   - 输入 `python --version`，应该显示 Python 3.10.12
   - 输入 `pip --version`，应该显示 pip 版本

##### 1.2.3 安装MySQL 8.0
1. 下载MySQL 8.0：https://dev.mysql.com/downloads/installer/
2. 运行安装程序，选择「Developer Default」安装类型
3. 点击「Next」，然后点击「Execute」安装依赖
4. 依赖安装完成后，点击「Next」
5. 点击「Execute」开始安装MySQL
6. 安装完成后，点击「Next」
7. 进入配置向导，选择「Standalone MySQL Server / Classic MySQL Replication」
8. 点击「Next」，保持默认配置
9. 设置root密码（记好这个密码）
10. 点击「Next」，保持默认配置
11. 点击「Execute」完成配置
12. 验证MySQL安装：
    - 打开命令提示符
    - 输入 `mysql -u root -p`
    - 输入设置的root密码，应该能成功登录

##### 1.2.4 安装Nginx for Windows
1. 下载Nginx for Windows：https://nginx.org/en/download.html（选择稳定版本）
2. 解压下载的zip文件到合适的目录（例如 `D:\nginx`）
3. 验证Nginx安装：
   - 打开命令提示符，切换到Nginx目录
   - 输入 `nginx -v`，应该显示Nginx版本
   - 输入 `nginx` 启动Nginx
   - 在浏览器中输入 `http://localhost`，应该显示Nginx欢迎页面
   - 输入 `nginx -s stop` 停止Nginx

### 2. 部署项目

#### 2.1 克隆项目代码
1. 选择一个合适的目录（例如 `D:\wwwroot`）
2. 打开命令提示符，切换到该目录
3. 克隆项目代码：
   ```cmd
   git clone https://your-git-repo-url/literacy-land.git
   cd literacy-land
   ```

#### 2.2 创建虚拟环境
```cmd
python -m venv venv
venv\Scripts\activate
```

#### 2.3 安装依赖
```cmd
pip install -r requirements.txt
```

#### 2.4 配置环境变量
1. 复制 `.env.example` 为 `.env`：
   ```cmd
   copy .env.example .env
   ```
2. 使用文本编辑器打开 `.env`，根据实际情况修改配置：
   - 数据库连接信息
   - API密钥
   - 其他配置项

#### 2.5 初始化数据库
```cmd
python main.py  # 这将创建所有表结构
```

### 3. 配置Nginx反向代理

#### 3.1 创建Nginx配置文件
1. 打开Nginx配置目录（例如 `D:\nginx\conf`）
2. 备份默认的 `nginx.conf` 文件
3. 使用文本编辑器打开 `nginx.conf`，替换为以下内容：
   ```nginx
   worker_processes  1;

   events {
       worker_connections  1024;
   }

   http {
       include       mime.types;
       default_type  application/octet-stream;

       sendfile        on;
       keepalive_timeout  65;

       server {
           listen       80;
           server_name  localhost;  # 替换为你的域名或IP

           location / {
               proxy_pass http://127.0.0.1:8000;
               proxy_set_header Host $host;
               proxy_set_header X-Real-IP $remote_addr;
               proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
               proxy_set_header X-Forwarded-Proto $scheme;
           }

           location /uploads {
               alias D:/wwwroot/literacy-land/uploads;  # 替换为项目的uploads目录绝对路径
               expires 30d;
               access_log off;
           }

           error_page   500 502 503 504  /50x.html;
           location = /50x.html {
               root   html;
           }
       }
   }
   ```

#### 3.2 验证Nginx配置
```cmd
cd D:\nginx
nginx -t
```

如果显示 "nginx: configuration file D:\nginx/conf/nginx.conf test is successful"，则配置正确。

### 4. 配置Uvicorn作为Windows服务

#### 4.1 安装NSSM
1. 下载NSSM：https://nssm.cc/download
2. 解压下载的文件，将 `nssm.exe` 复制到 `C:\Windows\System32` 目录

#### 4.2 创建Uvicorn服务
1. 打开命令提示符（管理员权限）
2. 输入以下命令创建服务：
   ```cmd
   nssm install LiteracyLandUvicorn
   ```
3. 在NSSM配置界面中：
   - 应用程序标签页：
     - 路径：选择项目虚拟环境中的python.exe（例如 `D:\wwwroot\literacy-land\venv\Scripts\python.exe`）
     - 启动目录：选择项目目录（例如 `D:\wwwroot\literacy-land`）
     - 参数：`-m uvicorn main:app --host 127.0.0.1 --port 8000 --workers 4`
   - 登录标签页：
     - 选择「本地系统账户」
   - 退出操作标签页：
     - 重启服务：勾选「重启服务」，延迟设为3000毫秒
   - 点击「Install service」
4. 启动服务：
   ```cmd
   nssm start LiteracyLandUvicorn
   ```
5. 验证服务状态：
   ```cmd
   nssm status LiteracyLandUvicorn
   ```

#### 4.3 创建Nginx服务
1. 打开命令提示符（管理员权限）
2. 输入以下命令创建服务：
   ```cmd
   nssm install LiteracyLandNginx
   ```
3. 在NSSM配置界面中：
   - 应用程序标签页：
     - 路径：选择Nginx可执行文件（例如 `D:\nginx\nginx.exe`）
     - 启动目录：选择Nginx目录（例如 `D:\nginx`）
   - 登录标签页：
     - 选择「本地系统账户」
   - 退出操作标签页：
     - 重启服务：勾选「重启服务」，延迟设为3000毫秒
   - 点击「Install service」
4. 启动服务：
   ```cmd
   nssm start LiteracyLandNginx
   ```
5. 验证服务状态：
   ```cmd
   nssm status LiteracyLandNginx
   ```

### 5. 配置防火墙

1. 打开「Windows Defender 防火墙」
2. 点击「高级设置」
3. 点击「入站规则」
4. 点击右侧「新建规则」
5. 选择「端口」，点击「下一步」
6. 选择「TCP」，输入「80」作为特定本地端口，点击「下一步」
7. 选择「允许连接」，点击「下一步」
8. 保持默认配置，点击「下一步」
9. 输入名称「允许HTTP端口80」，点击「完成」

### 6. 验证部署

1. 在本地浏览器中输入 `http://localhost`，应该能访问项目API
2. 访问 `http://localhost/api/v1/docs`，应该能看到Swagger API文档
3. 访问 `http://localhost/health`，应该返回健康检查结果

### 7. 后续维护

#### 7.1 查看服务状态
```cmd
nssm status LiteracyLandUvicorn
nssm status LiteracyLandNginx
```

#### 7.2 重启服务
```cmd
nssm restart LiteracyLandUvicorn
nssm restart LiteracyLandNginx
```

#### 7.3 停止服务
```cmd
nssm stop LiteracyLandUvicorn
nssm stop LiteracyLandNginx
```

#### 7.4 更新代码
```cmd
cd D:\wwwroot\literacy-land
git pull
venv\Scripts\activate
pip install -r requirements.txt
nssm restart LiteracyLandUvicorn
```

#### 7.5 重新加载Nginx配置
```cmd
nssm restart LiteracyLandNginx
```

#### 7.6 数据库备份
```cmd
mysqldump -u root -p parent_child_literacy > backup_$(date +%Y%m%d_%H%M%S).sql
```

## 常见问题

1. **服务启动失败**
   - 检查服务状态：`nssm status LiteracyLandUvicorn` 或 `nssm status LiteracyLandNginx`
   - 查看日志：服务日志默认保存在系统事件日志中
   - 检查环境变量配置是否正确
   - 确保数据库连接正常

2. **502 Bad Gateway**
   - 检查Uvicorn服务是否运行
   - 检查Nginx配置是否正确
   - 检查端口8000是否被占用

3. **数据库连接失败**
   - 检查MySQL服务是否运行
   - 检查数据库用户名和密码是否正确
   - 检查数据库权限配置

4. **API调用失败**
   - 检查API密钥是否正确配置
   - 检查网络连接是否正常
   - 查看Uvicorn日志

## 安全建议

1. 定期更新系统和依赖包
2. 使用强密码并定期更换
3. 关闭不必要的端口
4. 配置HTTPS证书（推荐使用Let's Encrypt）
5. 定期备份数据库
6. 配置防火墙规则
7. 使用监控工具（如Prometheus + Grafana）监控服务状态
