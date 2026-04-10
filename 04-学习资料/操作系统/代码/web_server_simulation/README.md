# Web服务器集群负载均衡模拟系统

基于时间片轮转(Round Robin)算法的多线程服务器集群模拟，前后端分离架构，前端使用Canvas展示实时动画效果。

## 项目结构

```
web_server_simulation/
├── server.py              # 后端服务 (Flask + SocketIO)
├── templates/
│   └── index.html         # 前端页面 (Canvas动画)
└── README.md              # 本文件
```

## 技术栈

### 后端
- **Python 3.7+**
- **Flask** - Web框架
- **Flask-SocketIO** - WebSocket实时通信
- **threading** - 多线程模拟服务器

### 前端
- **HTML5 Canvas** - 动画渲染
- **Socket.IO Client** - 实时数据通信
- **CSS3** - 现代化UI样式

## 安装依赖

```bash
cd web_server_simulation

# 安装Python依赖
pip install flask flask-socketio
```

## 运行方法

### 1. 启动后端服务

```bash
python server.py
```

成功启动后显示：
```
============================================================
Web服务器集群负载均衡模拟系统 - 后端服务
访问 http://localhost:5000 查看前端动画
============================================================
```

### 2. 打开浏览器访问

```
http://localhost:5000
```

## 功能说明

### 控制面板
- **服务器数量**: 设置模拟的服务器数量 (1-8)
- **请求总数**: 设置要模拟的HTTP请求数量 (5-100)
- **请求间隔**: 设置请求到达的时间间隔 (0.1-2.0秒)

### 动画展示
1. **左侧**: 客户端请求源
2. **中间**: 负载均衡器 (Load Balancer)
3. **右侧**: 服务器集群
   - 绿色 = 空闲
   - 黄色 = 忙碌
   - 进度条显示处理进度

### 实时数据
- 紫色粒子: 请求从负载均衡器流向服务器的动画
- 状态指示灯: 显示服务器当前状态
- 统计面板: 实时显示请求处理情况
- 日志面板: 显示详细的处理日志

## 核心算法

### 时间片轮转 (Round Robin)
```python
def dispatch_request(self, request):
    with self.lock:  # 互斥锁保护临界区
        # 优先寻找空闲服务器
        for _ in range(self.num_servers):
            server = self.servers[self.current_index]
            if not server.is_busy():
                selected_server = server
                break
            # 轮询下一个
            self.current_index = (self.current_index + 1) % self.num_servers
```

### 同步机制
- **互斥锁 (Lock)**: 保护`current_index`的更新
- **条件变量**: 服务器线程安全地处理请求队列
- **WebSocket**: 前后端实时通信

## 操作系统概念体现

| 概念 | 实现方式 |
|------|----------|
| 多线程 | 每个服务器是一个Thread子类 |
| 临界区 | 用Lock保护current_index更新 |
| 调度算法 | 时间片轮转(Round Robin) |
| 进程同步 | 队列+锁实现请求安全传递 |
| 忙则等待 | 服务器busy时轮询下一个 |

## 截图示例

运行后会看到：
1. 服务器状态实时变化
2. 请求粒子流动动画
3. 进度条显示处理进度
4. 统计数据实时更新

## 注意事项

1. 需要先安装Python依赖才能运行
2. 前端需要浏览器支持Canvas和WebSocket
3. 推荐使用Chrome/Edge/Firefox浏览器
4. 如果端口5000被占用，可修改server.py最后一行的端口号

## 停止服务

按 `Ctrl+C` 停止后端服务
