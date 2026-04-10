"""
Web服务器集群负载均衡模拟系统 - 后端
======================================
基于时间片轮转(Round Robin)算法的多线程服务器集群模拟
使用Flask-SocketIO提供实时数据给前端

启动命令: python server.py
然后在浏览器中打开 http://localhost:5000
"""

import threading
import time
import queue
import random
from datetime import datetime
from typing import Optional, Dict, List
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'web-server-simulation'
socketio = SocketIO(app, cors_allowed_origins="*")


class Request:
    """HTTP请求类"""
    _id_counter = 0
    _lock = threading.Lock()

    def __init__(self, client_ip: str, processing_time: float):
        with Request._lock:
            Request._id_counter += 1
            self.request_id = Request._id_counter
        self.client_ip = client_ip
        self.processing_time = processing_time
        self.create_time = datetime.now()
        self.start_time: Optional[datetime] = None
        self.finish_time: Optional[datetime] = None
        self.assigned_server: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            'id': self.request_id,
            'ip': self.client_ip,
            'processing_time': self.processing_time,
            'server': self.assigned_server
        }


class WebServer(threading.Thread):
    """模拟Web服务器 - 继承Thread实现并发"""

    def __init__(self, server_id: int, socketio_instance: SocketIO):
        super().__init__(name=f"Server-{server_id}")
        self.server_id = server_id
        self.socketio = socketio_instance
        self.request_queue: queue.Queue[Request] = queue.Queue()
        self.active = True
        self.busy = False
        self.processed_count = 0
        self.lock = threading.Lock()
        self.current_request: Optional[Request] = None
        self.progress = 0.0  # 处理进度 0-100%

    def run(self):
        """服务器主循环 - 持续处理请求"""
        while self.active:
            try:
                request = self.request_queue.get(timeout=0.05)
                self.current_request = request

                with self.lock:
                    self.busy = True
                    self.progress = 0.0

                # 通知前端 - 开始处理
                self.socketio.emit('server_status', {
                    'server_id': self.server_id,
                    'status': 'busy',
                    'request': request.to_dict(),
                    'queue_size': self.request_queue.qsize()
                })

                # 模拟请求处理过程（带进度更新）
                self.process_request_with_progress(request)

                with self.lock:
                    self.busy = False
                    self.progress = 0.0
                    self.processed_count += 1
                    self.current_request = None

                # 通知前端 - 处理完成
                self.socketio.emit('server_status', {
                    'server_id': self.server_id,
                    'status': 'idle',
                    'processed': self.processed_count,
                    'queue_size': self.request_queue.qsize()
                })

            except queue.Empty:
                continue

    def process_request_with_progress(self, request: Request):
        """处理请求并发送进度更新"""
        request.start_time = datetime.now()
        total_time = request.processing_time

        # 每100ms更新一次进度
        steps = int(total_time / 0.1)
        for i in range(steps):
            if not self.active:
                break
            time.sleep(0.1)
            self.progress = (i + 1) / steps * 100

            # 发送进度更新
            self.socketio.emit('request_progress', {
                'server_id': self.server_id,
                'request_id': request.request_id,
                'progress': self.progress
            })

        request.finish_time = datetime.now()
        response_time = (request.finish_time - request.create_time).total_seconds()

        # 发送完成消息
        self.socketio.emit('request_complete', {
            'server_id': self.server_id,
            'request': request.to_dict(),
            'response_time': response_time
        })

    def assign_request(self, request: Request) -> bool:
        """分配请求到服务器队列"""
        try:
            request.assigned_server = self.server_id
            self.request_queue.put(request, block=False)

            # 通知前端 - 请求入队
            self.socketio.emit('request_queued', {
                'server_id': self.server_id,
                'request': request.to_dict(),
                'queue_size': self.request_queue.qsize()
            })
            return True
        except queue.Full:
            return False

    def is_busy(self) -> bool:
        """检查服务器是否忙碌"""
        with self.lock:
            return self.busy

    def get_status(self) -> dict:
        """获取服务器状态"""
        with self.lock:
            return {
                'id': self.server_id,
                'busy': self.busy,
                'progress': self.progress,
                'processed': self.processed_count,
                'queue_size': self.request_queue.qsize(),
                'current_request': self.current_request.to_dict() if self.current_request else None
            }

    def shutdown(self):
        """关闭服务器"""
        self.active = False


class LoadBalancer:
    """负载均衡器 - 时间片轮转(Round Robin)算法"""

    def __init__(self, num_servers: int, socketio_instance: SocketIO):
        self.num_servers = num_servers
        self.socketio = socketio_instance
        self.servers: List[WebServer] = []
        self.current_index = 0
        self.lock = threading.Lock()
        self.total_requests = 0
        self.dropped_requests = 0
        self.request_history: List[dict] = []
        self.running = False

    def create_servers(self):
        """创建服务器集群"""
        for i in range(self.num_servers):
            server = WebServer(server_id=i, socketio_instance=self.socketio)
            self.servers.append(server)
            server.start()
            print(f"[+] Server-{i} 已启动")

    def dispatch_request(self, request: Request) -> bool:
        """
        分发请求 - 时间片轮转算法
        使用互斥锁保护临界区
        """
        with self.lock:
            # 优先寻找空闲服务器
            for _ in range(self.num_servers):
                server = self.servers[self.current_index]
                if not server.is_busy():
                    selected_server = server
                    self.current_index = (self.current_index + 1) % self.num_servers
                    break
                self.current_index = (self.current_index + 1) % self.num_servers
            else:
                # 没有空闲服务器，轮询分配
                selected_server = self.servers[self.current_index]
                self.current_index = (self.current_index + 1) % self.num_servers

        # 在锁外分配请求
        if selected_server.assign_request(request):
            self.total_requests += 1
            self.request_history.append(request.to_dict())

            # 通知前端 - 请求分配
            self.socketio.emit('request_assigned', {
                'request': request.to_dict(),
                'algorithm': 'Round Robin',
                'current_index': self.current_index
            })
            return True
        else:
            self.dropped_requests += 1
            return False

    def get_stats(self) -> dict:
        """获取系统统计信息"""
        return {
            'total_requests': self.total_requests,
            'dropped_requests': self.dropped_requests,
            'servers': [server.get_status() for server in self.servers]
        }

    def shutdown(self):
        """关闭所有服务器"""
        self.running = False
        for server in self.servers:
            server.shutdown()
            server.join()
            print(f"[-] Server-{server.server_id} 已关闭")


class SimulationController:
    """模拟控制器 - 管理整个模拟过程"""

    def __init__(self, socketio_instance: SocketIO):
        self.socketio = socketio_instance
        self.load_balancer: Optional[LoadBalancer] = None
        self.simulation_thread: Optional[threading.Thread] = None
        self.running = False

    def start_simulation(self, num_servers: int = 3, num_requests: int = 20,
                        request_interval: float = 0.5):
        """启动模拟"""
        if self.running:
            return False

        self.running = True
        self.load_balancer = LoadBalancer(num_servers, self.socketio)
        self.load_balancer.create_servers()

        # 在新线程中运行模拟
        self.simulation_thread = threading.Thread(
            target=self._run_simulation,
            args=(num_requests, request_interval)
        )
        self.simulation_thread.start()
        return True

    def _run_simulation(self, num_requests: int, request_interval: float):
        """运行模拟循环"""
        print(f"[*] 模拟开始: {num_requests} 个请求")

        for i in range(num_requests):
            if not self.running:
                break

            # 生成随机请求
            ip = self._generate_random_ip()
            processing_time = random.uniform(0.5, 3.0)
            request = Request(client_ip=ip, processing_time=processing_time)

            # 通知前端 - 新请求到达
            self.socketio.emit('new_request', request.to_dict())

            # 分发请求
            self.load_balancer.dispatch_request(request)

            # 请求到达间隔
            time.sleep(request_interval)

        # 等待所有请求处理完成
        print("[*] 等待所有请求处理完成...")
        time.sleep(5)

        # 发送最终统计
        stats = self.load_balancer.get_stats()
        self.socketio.emit('simulation_complete', stats)

        self.running = False

    def stop_simulation(self):
        """停止模拟"""
        self.running = False
        if self.load_balancer:
            self.load_balancer.shutdown()

    @staticmethod
    def _generate_random_ip() -> str:
        """生成随机IP地址"""
        return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"


# 全局模拟控制器
sim_controller = SimulationController(socketio)


# ============ Flask 路由 ============

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/stats')
def get_stats():
    """获取当前统计信息"""
    if sim_controller.load_balancer:
        return jsonify(sim_controller.load_balancer.get_stats())
    return jsonify({'error': 'Simulation not running'})


# ============ SocketIO 事件 ============

@socketio.on('connect')
def handle_connect():
    """客户端连接"""
    print('[*] 客户端已连接')
    emit('connected', {'message': 'Connected to Web Server Simulation'})


@socketio.on('disconnect')
def handle_disconnect():
    """客户端断开"""
    print('[*] 客户端已断开')


@socketio.on('start_simulation')
def handle_start_simulation(data):
    """开始模拟"""
    num_servers = data.get('num_servers', 3)
    num_requests = data.get('num_requests', 20)
    interval = data.get('interval', 0.5)

    success = sim_controller.start_simulation(num_servers, num_requests, interval)
    emit('simulation_started', {'success': success})


@socketio.on('stop_simulation')
def handle_stop_simulation():
    """停止模拟"""
    sim_controller.stop_simulation()
    emit('simulation_stopped', {'message': 'Simulation stopped'})


@socketio.on('get_status')
def handle_get_status():
    """获取当前状态"""
    if sim_controller.load_balancer:
        emit('system_status', sim_controller.load_balancer.get_stats())


if __name__ == '__main__':
    print("="*60)
    print("Web服务器集群负载均衡模拟系统 - 后端服务")
    print("访问 http://localhost:5000 查看前端动画")
    print("="*60)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
