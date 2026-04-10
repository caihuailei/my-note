#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行多线程任务调度系统
按优先级调度：VIP > 普通 > 对公
同优先级内：非抢占式短作业优先 (SJF)
"""

import threading
import queue
import time
import random
from dataclasses import dataclass, field
from typing import List, Optional
import heapq


@dataclass
class Task:
    """任务类"""
    task_id: int
    priority: int          # 优先级 (0=VIP, 1=普通, 2=对公)
    estimated_time: float  # 预估处理时间（秒）
    arrival_time: float    # 到达时间
    business_type: str     # 业务类型描述

    def __lt__(self, other):
        """用于堆排序：优先级低的先出，同优先级时间短的先出"""
        if self.priority != other.priority:
            return self.priority < other.priority
        return self.estimated_time < other.estimated_time


class PrioritySJFQueue:
    """
    优先级SJF队列
    - 3个优先级队列（VIP、普通、对公）
    - 同优先级内按短作业优先排序
    """
    def __init__(self):
        self.lock = threading.Lock()
        self.vip_queue = []       # 优先级0
        self.normal_queue = []    # 优先级1
        self.corporate_queue = [] # 优先级2

    def put(self, task: Task):
        """添加任务到对应优先级队列"""
        with self.lock:
            if task.priority == 0:
                heapq.heappush(self.vip_queue, task)
            elif task.priority == 1:
                heapq.heappush(self.normal_queue, task)
            else:
                heapq.heappush(self.corporate_queue, task)

    def get(self, timeout: float = None) -> Optional[Task]:
        """从最高优先级非空队列中取出任务"""
        with self.lock:
            for q in [self.vip_queue, self.normal_queue, self.corporate_queue]:
                if q:
                    return heapq.heappop(q)
            return None

    def is_empty(self) -> bool:
        """队列是否为空"""
        with self.lock:
            return not (self.vip_queue or self.normal_queue or self.corporate_queue)


class BankTaskScheduler:
    """银行任务调度器"""

    def __init__(self, num_workers: int = 3):
        self.task_queue = PrioritySJFQueue()
        self.num_workers = num_workers
        self.workers = []
        self.task_counter = 0
        self.start_time = time.time()
        self.results = []
        self.results_lock = threading.Lock()
        self.shutdown = False

    def process_task(self, worker_id: int, task: Task):
        """处理单个任务（模拟业务处理）"""
        priority_names = {0: "VIP", 1: "普通", 2: "对公"}
        print(f"[{time.strftime('%H:%M:%S')}] "
              f"(worker-{worker_id}) 开始处理 "
              f"{task.business_type} (ID:{task.task_id}, "
              f"优先级:{priority_names.get(task.priority, '未知')}, "
              f"预计时间:{task.estimated_time:.2f}s)")

        # 模拟任务处理时间
        actual_time = task.estimated_time * random.uniform(0.8, 1.2)
        time.sleep(actual_time)

        completion_time = time.time() - self.start_time
        turnaround_time = completion_time - task.arrival_time

        print(f"[{time.strftime('%H:%M:%S')}] "
              f"(worker-{worker_id}) 完成处理 "
              f"{task.business_type} (ID:{task.task_id}) "
              f"实际耗时:{actual_time:.2f}s")

        with self.results_lock:
            self.results.append({
                'task_id': task.task_id,
                'priority': task.priority,
                'business_type': task.business_type,
                'arrival_time': task.arrival_time,
                'completion_time': completion_time,
                'actual_time': actual_time,
                'turnaround_time': turnaround_time,
                'worker_id': worker_id
            })

    def worker(self, worker_id: int):
        """工作线程函数"""
        while not self.shutdown:
            try:
                task = self.task_queue.get(timeout=0.5)
                if task:
                    self.process_task(worker_id, task)
            except queue.Empty:
                continue

    def submit_task(self, priority: int, estimated_time: float, business_type: str):
        """提交新任务"""
        self.task_counter += 1
        task = Task(
            task_id=self.task_counter,
            priority=priority,
            estimated_time=estimated_time,
            arrival_time=time.time() - self.start_time,
            business_type=business_type
        )
        self.task_queue.put(task)
        priority_names = {0: "VIP", 1: "普通", 2: "对公"}
        print(f"[{time.strftime('%H:%M:%S')}] 任务到达: "
              f"{business_type} (ID:{task.task_id}, "
              f"优先级:{priority_names.get(priority, '未知')}, "
              f"预计时间:{estimated_time:.2f}s)")
        return task

    def start(self):
        """启动调度器"""
        print("=" * 60)
        print("银行任务调度系统启动")
        print(f"工作线程数: {self.num_workers}")
        print("调度策略: 优先级调度 (VIP > 普通 > 对公)")
        print("          同优先级内采用非抢占式SJF")
        print("=" * 60)

        for i in range(self.num_workers):
            t = threading.Thread(target=self.worker, args=(i,), daemon=True)
            self.workers.append(t)
            t.start()

    def stop(self):
        """停止调度器"""
        self.shutdown = True
        for t in self.workers:
            t.join(timeout=2)

    def print_statistics(self):
        """打印统计信息"""
        print("\n" + "=" * 60)
        print("调度统计结果")
        print("=" * 60)

        if not self.results:
            print("暂无完成的任务")
            return

        sorted_results = sorted(self.results, key=lambda x: x['completion_time'])

        print(f"{'任务ID':<6} {'优先级':<8} {'业务类型':<12} {'到达':<6} {'完成':<6} "
              f"{'处理':<6} {'周转':<8} {'Worker':<6}")
        print("-" * 60)

        total_turnaround = 0
        priority_stats = {0: [], 1: [], 2: []}

        for r in sorted_results:
            print(f"{r['task_id']:<6} {r['priority']:<8} {r['business_type']:<12} "
                  f"{r['arrival_time']:<6.2f} {r['completion_time']:<6.2f} "
                  f"{r['actual_time']:<6.2f} {r['turnaround_time']:<8.2f} {r['worker_id']:<6}")
            total_turnaround += r['turnaround_time']
            priority_stats[r['priority']].append(r['turnaround_time'])

        print("-" * 60)
        print(f"平均周转时间: {total_turnaround / len(self.results):.2f}秒")
        print(f"总任务数: {len(self.results)}")

        priority_names = {0: "VIP", 1: "普通", 2: "对公"}
        print("\n按优先级统计:")
        for p in range(3):
            if priority_stats[p]:
                avg_t = sum(priority_stats[p]) / len(priority_stats[p])
                print(f"  {priority_names[p]:<6}: {len(priority_stats[p])}个任务, "
                      f"平均周转时间: {avg_t:.2f}秒")


def generate_test_tasks(scheduler: BankTaskScheduler, num_tasks: int = 15):
    """生成测试任务"""
    time.sleep(0.5)

    # 任务列表: (优先级, 处理时间, 业务类型)
    tasks = [
        (1, 0.8, "普通存款"),
        (0, 1.2, "VIP转账"),
        (2, 1.5, "对公开户"),
        (1, 0.5, "普通取款"),
        (0, 0.3, "VIP理财赎回"),
        (2, 2.0, "对公贷款审批"),
        (1, 1.0, "普通转账"),
        (0, 0.6, "VIP咨询"),
        (2, 0.4, "对公查询"),
        (1, 2.5, "普通贷款申请"),
        (0, 0.9, "VIP信用审批"),
        (2, 1.2, "对公 payroll"),
        (1, 0.7, "普通换卡"),
        (0, 1.0, "VIP冻结"),
        (2, 0.8, "对公结汇"),
    ]

    for priority, est_time, biz_type in tasks[:num_tasks]:
        time.sleep(random.uniform(0.3, 0.8))
        scheduler.submit_task(priority, est_time, biz_type)


def main():
    """主函数：模拟银行任务调度"""
    print("=" * 60)
    print("学号尾数为单号的同学做第1题")
    print("题目：银行多线程任务调度系统")
    print("调度策略：VIP > 普通 > 对公，同优先级内采用非抢占式SJF")
    print("=" * 60)
    print()

    # 创建调度器，启动3个工作线程
    scheduler = BankTaskScheduler(num_workers=3)
    scheduler.start()

    # 生成测试任务
    generate_test_tasks(scheduler, num_tasks=15)

    # 等待所有任务处理完成
    time.sleep(12)

    # 停止调度器并输出统计
    scheduler.stop()
    scheduler.print_statistics()


if __name__ == "__main__":
    main()
