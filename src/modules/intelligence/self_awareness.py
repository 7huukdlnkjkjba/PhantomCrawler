# PhantomCrawler - 自我感知模块
import time
import psutil
import threading
from typing import Dict, List, Any, Optional
from src.config import global_config
import statistics

class SelfAwarenessMonitor:
    """
    自我感知监控器 - 负责监控爬虫的内部状态和环境条件
    提供实时的性能指标、资源使用情况和行为模式分析
    """
    
    def __init__(self):
        # 性能指标记录
        self.request_times = []
        self.response_sizes = []
        self.success_rates = []
        self.error_counts = {
            'timeout': 0,
            'connection_error': 0,
            'blocked': 0,
            'other': 0
        }
        
        # 资源使用监控
        self.cpu_usage_history = []
        self.memory_usage_history = []
        self.network_io_history = []
        
        # 环境状态
        self.environment = {
            'is_headless': global_config.get('playwright.headless', True),
            'proxy_availability': True,
            'system_load': 0.0
        }
        
        # 行为模式分析
        self.action_sequence = []
        self.pattern_recognition = {
            'current_pattern': 'normal',
            'pattern_history': []
        }
        
        # 启动资源监控线程
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_resources, daemon=True)
        self.monitor_thread.start()
    
    def _monitor_resources(self):
        """资源监控线程函数"""
        process = psutil.Process()
        last_net_io = psutil.net_io_counters()
        
        while self.monitoring_active:
            # 记录CPU使用率
            cpu_percent = process.cpu_percent(interval=0.1)
            self.cpu_usage_history.append(cpu_percent)
            if len(self.cpu_usage_history) > 60:
                self.cpu_usage_history.pop(0)
            
            # 记录内存使用率
            memory_info = process.memory_info()
            memory_percent = process.memory_percent()
            self.memory_usage_history.append(memory_percent)
            if len(self.memory_usage_history) > 60:
                self.memory_usage_history.pop(0)
            
            # 记录网络I/O
            current_net_io = psutil.net_io_counters()
            net_io_diff = {
                'bytes_sent': current_net_io.bytes_sent - last_net_io.bytes_sent,
                'bytes_recv': current_net_io.bytes_recv - last_net_io.bytes_recv
            }
            self.network_io_history.append(net_io_diff)
            if len(self.network_io_history) > 60:
                self.network_io_history.pop(0)
            last_net_io = current_net_io
            
            # 更新系统负载
            if hasattr(psutil, 'getloadavg'):
                load_avg = psutil.getloadavg()[0]
            else:
                # Windows系统
                load_avg = cpu_percent / 100
            self.environment['system_load'] = load_avg
            
            # 检查是否需要调整行为
            self._check_resource_thresholds()
            
            # 每秒检查一次
            time.sleep(1)
    
    def _check_resource_thresholds(self):
        """检查资源使用阈值并调整行为"""
        # 获取最近的资源使用情况
        if len(self.cpu_usage_history) > 0:
            avg_cpu = statistics.mean(self.cpu_usage_history)
        else:
            avg_cpu = 0
        
        if len(self.memory_usage_history) > 0:
            avg_memory = statistics.mean(self.memory_usage_history)
        else:
            avg_memory = 0
        
        # 如果资源使用过高，调整全局配置
        if avg_cpu > 80:
            print(f"[SelfAwareness] 检测到CPU使用率过高 ({avg_cpu:.1f}%)，降低并发")
            global_config.set('behavior_simulation.max_concurrent', max(1, global_config.get('behavior_simulation.max_concurrent', 5) - 1))
        
        if avg_memory > 80:
            print(f"[SelfAwareness] 检测到内存使用率过高 ({avg_memory:.1f}%)，增加垃圾回收频率")
            # 这里可以触发垃圾回收
            import gc
            gc.collect()
    
    def record_request_metrics(self, url: str, response_time: float, response_size: int, success: bool):
        """
        记录请求指标
        
        Args:
            url: 请求的URL
            response_time: 响应时间（秒）
            response_size: 响应大小（字节）
            success: 是否成功
        """
        # 记录响应时间
        self.request_times.append({
            'url': url,
            'time': response_time,
            'timestamp': time.time()
        })
        if len(self.request_times) > 100:
            self.request_times.pop(0)
        
        # 记录响应大小
        self.response_sizes.append(response_size)
        if len(self.response_sizes) > 100:
            self.response_sizes.pop(0)
        
        # 更新成功率
        recent_successes = sum(1 for r in self.request_times[-20:] if r.get('success', True)) / max(1, len(self.request_times[-20:]))
        self.success_rates.append(recent_successes)
        if len(self.success_rates) > 30:
            self.success_rates.pop(0)
        
        # 记录行为序列
        self.action_sequence.append({
            'action': 'request',
            'url': url,
            'success': success,
            'timestamp': time.time()
        })
        if len(self.action_sequence) > 50:
            self.action_sequence.pop(0)
    
    def record_error(self, error_type: str, details: str = None):
        """
        记录错误类型
        
        Args:
            error_type: 错误类型
            details: 错误详情
        """
        if error_type in self.error_counts:
            self.error_counts[error_type] += 1
        else:
            self.error_counts['other'] += 1
        
        # 记录错误事件
        self.action_sequence.append({
            'action': 'error',
            'error_type': error_type,
            'details': details,
            'timestamp': time.time()
        })
    
    def analyze_behavior_pattern(self) -> str:
        """
        分析当前的行为模式
        
        Returns:
            检测到的模式类型
        """
        # 分析最近的行为序列
        if len(self.action_sequence) < 10:
            return 'normal'
        
        # 计算最近的错误率
        recent_errors = sum(1 for a in self.action_sequence[-10:] if a.get('action') == 'error')
        error_rate = recent_errors / 10
        
        # 计算响应时间趋势
        if len(self.request_times) >= 5:
            recent_times = [r['time'] for r in self.request_times[-5:]]
            prev_times = [r['time'] for r in self.request_times[-10:-5]]
            time_increase = statistics.mean(recent_times) > statistics.mean(prev_times) * 1.5
        else:
            time_increase = False
        
        # 基于指标判断模式
        if error_rate > 0.5 or (recent_errors >= 3 and 'blocked' in [a.get('error_type') for a in self.action_sequence[-5:]]):
            pattern = 'blocked'
        elif error_rate > 0.3 or time_increase:
            pattern = 'suspicious'
        elif statistics.mean(self.success_rates[-5:]) > 0.95:
            pattern = 'optimal'
        else:
            pattern = 'normal'
        
        # 更新模式识别
        self.pattern_recognition['current_pattern'] = pattern
        self.pattern_recognition['pattern_history'].append({
            'pattern': pattern,
            'timestamp': time.time()
        })
        if len(self.pattern_recognition['pattern_history']) > 100:
            self.pattern_recognition['pattern_history'].pop(0)
        
        return pattern
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        获取当前性能指标
        
        Returns:
            性能指标字典
        """
        # 计算平均响应时间
        if self.request_times:
            avg_response_time = statistics.mean([r['time'] for r in self.request_times[-20:]])
            p95_response_time = sorted([r['time'] for r in self.request_times])[-int(len(self.request_times) * 0.05)] if self.request_times else 0
        else:
            avg_response_time = 0
            p95_response_time = 0
        
        # 计算平均响应大小
        if self.response_sizes:
            avg_response_size = statistics.mean(self.response_sizes[-20:])
        else:
            avg_response_size = 0
        
        # 计算最近成功率
        if self.success_rates:
            recent_success_rate = self.success_rates[-1]
        else:
            recent_success_rate = 1.0
        
        return {
            'avg_response_time': avg_response_time,
            'p95_response_time': p95_response_time,
            'avg_response_size': avg_response_size,
            'success_rate': recent_success_rate,
            'error_counts': self.error_counts.copy(),
            'current_pattern': self.pattern_recognition['current_pattern']
        }
    
    def get_resource_metrics(self) -> Dict[str, Any]:
        """
        获取资源使用指标
        
        Returns:
            资源使用指标字典
        """
        # 计算平均CPU使用率
        if self.cpu_usage_history:
            avg_cpu = statistics.mean(self.cpu_usage_history)
            max_cpu = max(self.cpu_usage_history)
        else:
            avg_cpu = 0
            max_cpu = 0
        
        # 计算平均内存使用率
        if self.memory_usage_history:
            avg_memory = statistics.mean(self.memory_usage_history)
            max_memory = max(self.memory_usage_history)
        else:
            avg_memory = 0
            max_memory = 0
        
        # 计算平均网络I/O
        if self.network_io_history:
            avg_bytes_sent = statistics.mean([io['bytes_sent'] for io in self.network_io_history[-10:]])
            avg_bytes_recv = statistics.mean([io['bytes_recv'] for io in self.network_io_history[-10:]])
        else:
            avg_bytes_sent = 0
            avg_bytes_recv = 0
        
        return {
            'cpu_usage': {
                'average': avg_cpu,
                'max': max_cpu
            },
            'memory_usage': {
                'average': avg_memory,
                'max': max_memory
            },
            'network_io': {
                'bytes_sent_per_second': avg_bytes_sent,
                'bytes_recv_per_second': avg_bytes_recv
            },
            'system_load': self.environment['system_load']
        }
    
    def detect_anomalies(self) -> List[Dict[str, Any]]:
        """
        检测异常情况
        
        Returns:
            检测到的异常列表
        """
        anomalies = []
        
        # 检查响应时间异常
        if len(self.request_times) >= 10:
            recent_times = [r['time'] for r in self.request_times[-10:]]
            if recent_times:
                mean_time = statistics.mean(recent_times)
                stdev_time = statistics.stdev(recent_times) if len(recent_times) > 1 else 0
                
                # 检查是否有响应时间异常高的请求
                for request in self.request_times[-5:]:
                    if stdev_time > 0 and (request['time'] > mean_time + 3 * stdev_time):
                        anomalies.append({
                            'type': 'slow_response',
                            'url': request['url'],
                            'response_time': request['time'],
                            'threshold': mean_time + 3 * stdev_time,
                            'timestamp': time.time()
                        })
        
        # 检查错误率异常
        recent_requests = len(self.action_sequence)
        recent_errors = sum(1 for a in self.action_sequence if a.get('action') == 'error')
        
        if recent_requests > 0:
            error_rate = recent_errors / recent_requests
            if error_rate > 0.4:
                anomalies.append({
                    'type': 'high_error_rate',
                    'error_rate': error_rate,
                    'threshold': 0.4,
                    'timestamp': time.time()
                })
        
        # 检查资源使用异常
        if self.cpu_usage_history and max(self.cpu_usage_history) > 95:
            anomalies.append({
                'type': 'high_cpu_usage',
                'cpu_usage': max(self.cpu_usage_history),
                'threshold': 95,
                'timestamp': time.time()
            })
        
        if self.memory_usage_history and max(self.memory_usage_history) > 95:
            anomalies.append({
                'type': 'high_memory_usage',
                'memory_usage': max(self.memory_usage_history),
                'threshold': 95,
                'timestamp': time.time()
            })
        
        return anomalies
    
    def get_environment_assessment(self) -> Dict[str, Any]:
        """
        获取环境评估
        
        Returns:
            环境评估字典
        """
        # 评估当前环境的适宜性
        resource_metrics = self.get_resource_metrics()
        performance_metrics = self.get_performance_metrics()
        
        # 计算环境评分（0-100）
        cpu_score = max(0, 100 - resource_metrics['cpu_usage']['average'])
        memory_score = max(0, 100 - resource_metrics['memory_usage']['average'])
        performance_score = performance_metrics['success_rate'] * 100
        
        overall_score = (cpu_score * 0.2 + memory_score * 0.2 + performance_score * 0.6)
        
        # 判断环境状态
        if overall_score >= 80:
            status = 'optimal'
        elif overall_score >= 60:
            status = 'good'
        elif overall_score >= 40:
            status = 'degraded'
        else:
            status = 'critical'
        
        return {
            'status': status,
            'overall_score': overall_score,
            'component_scores': {
                'cpu': cpu_score,
                'memory': memory_score,
                'performance': performance_score
            },
            'is_headless': self.environment['is_headless'],
            'proxy_available': self.environment['proxy_availability'],
            'anomalies': self.detect_anomalies()
        }
    
    def shutdown(self):
        """关闭监控器"""
        self.monitoring_active = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=2.0)