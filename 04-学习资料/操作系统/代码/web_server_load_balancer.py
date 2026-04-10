"""
Web服务器集群负载均衡模拟系统
================================
基于时间片轮转(Round Robin)算法的多线程服务器集群模拟

作者: [你的名字]
学号: [你的学号]
日期: 2026-04-06
"""

import threading
import time
import queue
import random
from datetime import datetime
from typing import Optional


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

    def __repr__(self):
        return f"Request(id={self.request_id}, ip={self.client_ip}, time={self.processing_time:.2f}s)"


class WebServer(threading.Thread):
    """
    模拟Web服务器
    继承自Thread类，每个服务器实例作为一个独立线程运行
    """
    def __init__(self, server_id: int, load_balancer: 'LoadBalancer'):
        super().__init__(name=f"Server-{server_id}")
        self.server_id = server_id
        self.load_balancer = load_balancer
        self.request_queue = queue.Queue()
        self.active = True
        self.busy = False
        self.processed_count = 0
        self.lock = threading.Lock()

    def run(self):
        """服务器主循环 - 持续处理请求"""
        while self.active:
            try:
                # 非阻塞方式获取请求，超时100ms后继续检查active状态
                request = self.request_queue.get(timeout=0.1)

                with self.lock:
                    self.busy = True

                # 处理请求
                self.process_request(request)

                with self.lock:
                    self.busy = False
                    self.processed_count += 1

            except queue.Empty:
                continue

    def process_request(self, request: Request):
        """处理HTTP请求 - 用sleep模拟I/O等待和计算耗时"""
        request.start_time = datetime.now()

        # 模拟请求处理时间
        time.sleep(request.processing_time)

        request.finish_time = datetime.now()

        # 计算响应时间
        response_time = (request.finish_time - request.create_time).total_seconds()

        print(f"[OK] Server-{self.server_id} 完成请求 {request.request_id} "
              f"(客户端: {request.client_ip}, 响应时间: {response_time:.3f}s)")

    def assign_request(self, request: Request) -> bool:
        """分配请求到服务器队列"""
        try:
            self.request_queue.put(request, block=False)
            print(f"[TO] 请求 {request.request_id} 分配给 Server-{self.server_id}")
            return True
        except queue.Full:
            return False

    def is_busy(self) -> bool:
        """检查服务器是否忙碌"""
        with self.lock:
            return self.busy

    def shutdown(self):
        """关闭服务器"""
        self.active = False


class LoadBalancer:
    """
    负载均衡器
    使用时间片轮转(Round Robin)算法分配请求
    """
    def __init__(self, num_servers: int):
        self.num_servers = num_servers
        self.servers: list[WebServer] = []
        self.current_index = 0
        self.lock = threading.Lock()  # 互斥锁保护临界区
        self.total_requests = 0
        self.dropped_requests = 0

        # 创建服务器集群
        self._create_servers()

    def _create_servers(self):
        """初始化服务器集群"""
        for i in range(self.num_servers):
            server = WebServer(server_id=i, load_balancer=self)
            self.servers.append(server)
            server.start()
            print(f"[+] Server-{i} 已启动")

    def dispatch_request(self, request: Request) -> bool:
        """
        分发请求到服务器 - 时间片轮转算法
        使用互斥锁保护current_index的更新（临界区）
        """
        # 查找可用服务器（非忙碌状态优先）
        with self.lock:
            # 记录查找起始位置，避免无限循环
            start_index = self.current_index
            selected_server = None

            # 遍历所有服务器，寻找空闲服务器
            for _ in range(self.num_servers):
                server = self.servers[self.current_index]

                # 检查服务器是否空闲
                if not server.is_busy():
                    selected_server = server
                    # 更新索引，指向下一个服务器（RR算法核心）
                    self.current_index = (self.current_index + 1) % self.num_servers
                    break

                # 移动到下一个服务器
                self.current_index = (self.current_index + 1) % self.num_servers

            # 如果没有空闲服务器，使用轮询分配（负载均衡保证）
            if selected_server is None:
                selected_server = self.servers[self.current_index]
                self.current_index = (self.current_index + 1) % self.num_servers

        # 在锁外分配请求，减少临界区
        if selected_server.assign_request(request):
            self.total_requests += 1
            return True
        else:
            self.dropped_requests += 1
            print(f"[FAIL] 请求 {request.request_id} 分配失败（服务器队列已满）")
            return False

    def get_stats(self) -> dict:
        """获取统计信息"""
        stats = {
            'total_requests': self.total_requests,
            'dropped_requests': self.dropped_requests,
            'servers': []
        }

        for server in self.servers:
            stats['servers'].append({
                'id': server.server_id,
                'processed': server.processed_count,
                'busy': server.is_busy(),
                'queue_size': server.request_queue.qsize()
            })

        return stats

    def print_stats(self):
        """打印统计信息"""
        print("\n" + "="*50)
        print("服务器集群状态统计")
        print("="*50)

        stats = self.get_stats()
        for server_info in stats['servers']:
            status = "忙碌" if server_info['busy'] else "空闲"
            print(f"Server-{server_info['id']}: 已处理 {server_info['processed']} 个请求, "
                  f"当前状态: {status}, 队列长度: {server_info['queue_size']}")

        print("-"*50)
        print(f"总请求数: {stats['total_requests']}")
        print(f"丢弃请求: {stats['dropped_requests']}")
        print("="*50 + "\n")

    def shutdown(self):
        """关闭所有服务器"""
        print("\n[*] 正在关闭服务器集群...")
        for server in self.servers:
            server.shutdown()
            server.join()
            print(f"[-] Server-{server.server_id} 已关闭")


class ClientSimulator:
    """客户端模拟器 - 生成随机HTTP请求"""

    @staticmethod
    def generate_random_ip() -> str:
        """生成随机IP地址"""
        return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

    @staticmethod
    def generate_request() -> Request:
        """生成随机请求 - 模拟不同复杂度的HTTP请求"""
        ip = ClientSimulator.generate_random_ip()
        # 随机处理时间：0.1秒到2秒（模拟不同复杂度的请求）
        processing_time = random.uniform(0.1, 2.0)
        return Request(client_ip=ip, processing_time=processing_time)


def simulate_web_server_cluster():
    """
    主模拟程序
    模拟高并发场景下的Web服务器集群处理
    """
    print("="*60)
    print("Web服务器集群负载均衡模拟系统")
    print("调度算法: 时间片轮转 (Round Robin)")
    print("="*60 + "\n")

    # 配置参数
    NUM_SERVERS = 3           # 服务器数量
    NUM_REQUESTS = 20         # 总请求数
    REQUEST_INTERVAL = 0.3    # 请求到达间隔（秒）

    # 创建负载均衡器和服务器集群
    load_balancer = LoadBalancer(num_servers=NUM_SERVERS)

    # 等待服务器启动
    time.sleep(0.5)

    print(f"\n[*] 开始模拟: 共 {NUM_REQUESTS} 个请求\n")

    # 生成并分发请求
    for i in range(NUM_REQUESTS):
        request = ClientSimulator.generate_request()
        print(f"[+] 收到新请求 {request}")

        # 分发请求
        load_balancer.dispatch_request(request)

        # 模拟请求到达间隔
        time.sleep(REQUEST_INTERVAL)

    # 等待所有请求处理完成
    print("\n[*] 等待所有请求处理完成...\n")
    time.sleep(3)

    # 打印最终统计
    load_balancer.print_stats()

    # 关闭服务器
    load_balancer.shutdown()

    print("\n[*] 模拟结束")


if __name__ == "__main__":
    simulate_web_server_cluster()
