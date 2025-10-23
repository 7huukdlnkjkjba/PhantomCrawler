# PhantomCrawler - 元认知引擎
import json
import time
import random
import pickle
import os
import threading
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from src.config import global_config
# 简单的logger替代实现，用于调试
class Logger:
    def __init__(self, name="PhantomCrawler"):
        self.name = name
    
    def info(self, message):
        print(f"[{self.name} INFO] {message}")
    
    def warning(self, message):
        print(f"[{self.name} WARNING] {message}")
    
    def error(self, message):
        print(f"[{self.name} ERROR] {message}")
    
    def debug(self, message):
        print(f"[{self.name} DEBUG] {message}")

class MetacognitionEngine:
    """
    元认知引擎 - PhantomCrawler的核心智能系统
    负责自我感知、学习优化和策略调整
    """
    
    def __init__(self):
        # 初始化知识库和学习模型
        self.knowledge_base = {}
        self.success_history = []
        self.failure_history = []
        self.strategy_scores = {}
        self.site_profiles = {}
        
        # 学习参数
        self.learning_rate = global_config.get('metacognition.learning_rate', 0.1)
        self.exploration_rate = global_config.get('metacognition.exploration_rate', 0.2)
        self.memory_size = global_config.get('metacognition.memory_size', 1000)
        self.discount_factor = global_config.get('metacognition.discount_factor', 0.9)
        
        # 元认知增强：环境感知和状态跟踪
        self.environment_awareness = {
            'detection_risk': 0.0,  # 检测风险 (0-1)
            'resource_pressure': {'cpu': 0.0, 'memory': 0.0, 'network': 0.0},  # 资源压力
            'system_performance': {'avg_response_time': 0.0, 'success_rate': 0.0}
        }
        
        # 行为模式跟踪
        self.current_behavior_pattern = 'normal'  # normal, careful, hurried, stealth
        self.behavior_transition_history = []
        self.last_pattern_change = time.time()
        
        # 线程安全锁
        self.lock = threading.RLock()
        
        # 性能历史
        self.performance_history = []
        
        # 日志
        try:
            self.logger = Logger('MetacognitionEngine')
        except:
            # 备用日志函数
            self.logger = type('Logger', (), {
                'info': lambda msg: print(f"[INFO] {msg}"),
                'warning': lambda msg: print(f"[WARNING] {msg}"),
                'error': lambda msg: print(f"[ERROR] {msg}"),
                'debug': lambda msg: print(f"[DEBUG] {msg}")
            })()
        
        # 加载历史数据
        self._load_knowledge()
        
        # 注册默认策略权重
        self._initialize_strategies()
        
        # 元认知增强：注册行为模式
        self._initialize_behavior_patterns()
        
        # 启动性能监控线程
        self._start_performance_monitor()
    
    def _initialize_strategies(self):
        """初始化默认策略权重"""
        self.strategy_scores = {
            'fingerprint_standard': 0.7,
            'fingerprint_advanced': 0.8,
            'delay_short': 0.6,
            'delay_medium': 0.7,
            'delay_long': 0.9,
            'request_chain_short': 0.6,
            'request_chain_medium': 0.7,
            'request_chain_long': 0.8,
            'proxy_direct': 0.5,
            'proxy_single': 0.6,
            'proxy_chain': 0.8,
        }
    
    def _initialize_behavior_patterns(self):
        """初始化行为模式参数"""
        self.behavior_patterns = {
            'normal': {
                'delay_multiplier': 1.0,
                'exploration_rate': 0.2,
                'risk_tolerance': 0.5,
                'resource_usage': 0.7
            },
            'careful': {
                'delay_multiplier': 1.5,
                'exploration_rate': 0.1,
                'risk_tolerance': 0.3,
                'resource_usage': 0.5
            },
            'hurried': {
                'delay_multiplier': 0.6,
                'exploration_rate': 0.3,
                'risk_tolerance': 0.7,
                'resource_usage': 0.9
            },
            'stealth': {
                'delay_multiplier': 2.0,
                'exploration_rate': 0.05,
                'risk_tolerance': 0.1,
                'resource_usage': 0.3
            }
        }
    
    def _start_performance_monitor(self):
        """启动性能监控线程"""
        def monitor_performance():
            while True:
                try:
                    # 每60秒更新一次性能统计
                    self._update_system_performance()
                    time.sleep(60)
                except Exception as e:
                    self.logger.error(f"性能监控出错: {e}")
        
        # 启动守护线程
        monitor_thread = threading.Thread(target=monitor_performance, daemon=True)
        monitor_thread.start()
        self.logger.debug("性能监控线程已启动")
    
    def _update_system_performance(self):
        """更新系统性能统计"""
        with self.lock:
            # 计算最近的成功率
            recent_history = self.success_history[-50:] + self.failure_history[-50:]
            recent_history.sort(key=lambda x: x.get('timestamp', 0))
            recent_history = recent_history[-50:]
            
            if recent_history:
                success_count = sum(1 for h in recent_history if h['url'] in [s['url'] for s in self.success_history])
                self.environment_awareness['system_performance']['success_rate'] = success_count / len(recent_history)
                
                # 计算平均响应时间（如果有）
                response_times = [h.get('result', {}).get('response_time', 0) for h in recent_history if 'response_time' in h.get('result', {})]
                if response_times:
                    self.environment_awareness['system_performance']['avg_response_time'] = sum(response_times) / len(response_times)
    
    def _load_knowledge(self):
        """从持久化存储加载知识库"""
        knowledge_path = global_config.get('metacognition.knowledge_path', 'data/metacognition.pkl')
        if os.path.exists(knowledge_path):
            try:
                with open(knowledge_path, 'rb') as f:
                    data = pickle.load(f)
                    self.knowledge_base = data.get('knowledge_base', {})
                    self.success_history = data.get('success_history', [])
                    self.failure_history = data.get('failure_history', [])
                    self.strategy_scores = data.get('strategy_scores', {})
                    self.site_profiles = data.get('site_profiles', {})
                    # 加载元认知数据
                    self.environment_awareness = data.get('environment_awareness', self.environment_awareness)
                    self.behavior_transition_history = data.get('behavior_transition_history', [])
                self.logger.info(f"成功加载知识库，包含 {len(self.site_profiles)} 个站点配置文件")
            except Exception as e:
                self.logger.error(f"加载知识库失败: {e}")
    
    def _save_knowledge(self):
        """将知识库保存到持久化存储"""
        knowledge_path = global_config.get('metacognition.knowledge_path', 'data/metacognition.pkl')
        os.makedirs(os.path.dirname(knowledge_path), exist_ok=True)
        
        data = {
            'knowledge_base': self.knowledge_base,
            'success_history': self.success_history[-self.memory_size:],
            'failure_history': self.failure_history[-self.memory_size:],
            'strategy_scores': self.strategy_scores,
            'site_profiles': self.site_profiles,
            'environment_awareness': self.environment_awareness,
            'behavior_transition_history': self.behavior_transition_history[-100:]
        }
        
        try:
            with open(knowledge_path, 'wb') as f:
                pickle.dump(data, f)
            self.logger.debug("知识库保存成功")
        except Exception as e:
            self.logger.error(f"保存知识库失败: {e}")
    
    def _update_detection_risk(self, success: bool, result: Dict[str, Any]):
        """根据爬取结果更新检测风险评估"""
        risk_delta = 0.0
        
        if not success:
            # 失败时增加风险
            content = result.get('content', '').lower()
            risk_keywords = ['captcha', '验证码', 'robot', 'blocked', 'security check']
            
            if any(keyword in content for keyword in risk_keywords):
                risk_delta += 0.3  # 明显的检测信号
            elif result.get('status_code') in [403, 429]:
                risk_delta += 0.2  # 访问被拒绝或速率限制
            else:
                risk_delta += 0.1  # 其他失败
        else:
            # 成功时降低风险
            risk_delta -= 0.05
        
        # 更新风险值
        new_risk = max(0.0, min(1.0, self.environment_awareness['detection_risk'] + risk_delta))
        self.environment_awareness['detection_risk'] = new_risk
        
        # 风险过高时触发警报
        if new_risk > 0.8:
            self.logger.warning(f"检测风险极高 ({new_risk:.2f})，建议立即调整策略")
    
    def _record_performance(self, success: bool, response_time: float):
        """记录性能数据"""
        record = {
            'timestamp': time.time(),
            'success': success,
            'response_time': response_time,
            'risk_level': self.environment_awareness['detection_risk'],
            'behavior_pattern': self.current_behavior_pattern
        }
        
        self.performance_history.append(record)
        # 保持历史记录大小限制
        if len(self.performance_history) > 1000:
            self.performance_history = self.performance_history[-1000:]
    
    def _select_optimized_behavior_pattern(self):
        """基于元认知分析选择优化的行为模式"""
        risk = self.environment_awareness['detection_risk']
        success_rate = self.environment_awareness['system_performance']['success_rate']
        
        # 避免频繁切换
        if time.time() - self.last_pattern_change < 300:  # 5分钟内不频繁切换
            return
        
        # 基于环境状态选择行为模式
        if risk > 0.7:
            new_pattern = 'stealth'
        elif risk > 0.4 or success_rate < 0.6:
            new_pattern = 'careful'
        elif success_rate > 0.8 and risk < 0.2:
            new_pattern = 'normal'
        else:
            new_pattern = 'normal'
        
        # 切换行为模式
        if new_pattern != self.current_behavior_pattern:
            self._change_behavior_pattern(new_pattern)
    
    def _change_behavior_pattern(self, new_pattern: str):
        """切换行为模式"""
        if new_pattern not in self.behavior_patterns:
            self.logger.warning(f"未知的行为模式: {new_pattern}，使用默认模式")
            new_pattern = 'normal'
        
        # 记录转换
        transition_record = {
            'timestamp': time.time(),
            'from_pattern': self.current_behavior_pattern,
            'to_pattern': new_pattern,
            'reason': f"风险级别: {self.environment_awareness['detection_risk']:.2f}, 成功率: {self.environment_awareness['system_performance']['success_rate']:.2f}"
        }
        
        self.behavior_transition_history.append(transition_record)
        self.current_behavior_pattern = new_pattern
        self.last_pattern_change = time.time()
        
        self.logger.info(f"行为模式已切换至: {new_pattern}")
    
    def _trigger_adaptive_response(self, domain: str, result: Dict[str, Any]):
        """触发自适应响应策略"""
        # 分析失败原因
        content = result.get('content', '').lower()
        status_code = result.get('status_code')
        
        # 生成响应策略
        response = {}
        
        if 'captcha' in content or '验证码' in content:
            response['type'] = 'captcha_detected'
            response['action'] = 'immediate_behavior_shift'
            response['new_pattern'] = 'stealth'
            response['cooldown'] = 300  # 5分钟冷却
            
            # 立即切换行为模式
            self.shift_behavior_pattern()
        
        elif status_code == 429:
            response['type'] = 'rate_limited'
            response['action'] = 'increase_delay'
            response['delay_factor'] = 2.0
            response['cooldown'] = 600  # 10分钟冷却
        
        elif status_code == 403:
            response['type'] = 'access_denied'
            response['action'] = 'full_reset'
            response['new_pattern'] = 'stealth'
            response['cooldown'] = 900  # 15分钟冷却
        
        # 记录响应
        if response:
            self.logger.warning(f"对 {domain} 触发自适应响应: {response['type']} - {response['action']}")
            
            # 更新站点配置文件
            if domain in self.site_profiles:
                self.site_profiles[domain]['last_response'] = response
                self.site_profiles[domain]['response_timestamp'] = time.time()
    
    def _is_successful_crawl(self, result: Dict[str, Any]) -> bool:
        """判断爬取是否成功"""
        # 检查状态码
        if result.get('status_code') not in [200, 201, 202, 203, 204, 205, 206]:
            return False
        
        # 检查内容是否包含阻止关键词
        content = result.get('content', '').lower()
        blocked_keywords = ['captcha', '验证码', 'robot', 'automated', 'blocked', 
                           'suspicious', 'unusual activity', 'access denied',
                           'security check', '验证', '人机验证']
        
        for keyword in blocked_keywords:
            if keyword in content:
                return False
        
        return True
    
    def analyze_crawl_result(self, url: str, result: Dict[str, Any], strategies_used: Dict[str, Any]):
        """
        分析爬取结果并更新知识
        
        Args:
            url: 爬取的URL
            result: 爬取结果
            strategies_used: 使用的策略
        """
        # 提取域名作为站点标识
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        
        # 判断成功或失败
        is_success = self._is_successful_crawl(result)
        
        # 更新检测风险评估
        self._update_detection_risk(is_success, result)
        
        # 记录性能数据
        response_time = result.get('response_time', 0)
        self._record_performance(is_success, response_time)
        
        # 记录历史
        record = {
            'url': url,
            'domain': domain,
            'timestamp': time.time(),
            'result': result,
            'strategies': strategies_used
        }
        
        with self.lock:
            if is_success:
                self.success_history.append(record)
                # 增加使用策略的得分
                self._reinforce_strategies(strategies_used, positive=True)
                self.logger.info(f"记录成功爬取: {url}")
            else:
                self.failure_history.append(record)
                # 降低使用策略的得分
                self._reinforce_strategies(strategies_used, positive=False)
                self.logger.warning(f"记录失败爬取: {url}")
                
                # 触发自适应响应
                self._trigger_adaptive_response(domain, result)
            
            # 更新站点配置文件
            self._update_site_profile(domain, is_success, strategies_used)
            
            # 基于当前状态优化行为模式
            self._select_optimized_behavior_pattern()
        
        # 保存知识
        self._save_knowledge()
    
    def update_resource_usage(self, cpu: float, memory: float, network: float):
        """更新资源使用情况
        
        Args:
            cpu: CPU使用率 (0-1)
            memory: 内存使用率 (0-1)
            network: 网络使用率 (0-1)
        """
        with self.lock:
            self.environment_awareness['resource_pressure'] = {
                'cpu': cpu,
                'memory': memory,
                'network': network
            }
            
            # 基于资源压力调整行为模式
            avg_pressure = (cpu + memory + network) / 3
            pattern = self.current_behavior_pattern
            pattern_resource_limit = self.behavior_patterns[pattern]['resource_usage']
            
            # 如果资源压力超过模式限制，切换到更保守的模式
            if avg_pressure > pattern_resource_limit + 0.2:
                if pattern == 'hurried' and avg_pressure > 0.8:
                    self._change_behavior_pattern('normal')
                elif pattern == 'normal' and avg_pressure > 0.9:
                    self._change_behavior_pattern('careful')
    
    def _reinforce_strategies(self, strategies_used: Dict[str, Any], positive: bool):
        """强化或弱化使用的策略"""
        for strategy_type, strategy_value in strategies_used.items():
            # 转换策略为标准格式
            strategy_name = self._get_strategy_name(strategy_type, strategy_value)
            
            if strategy_name in self.strategy_scores:
                # 更新策略得分
                if positive:
                    self.strategy_scores[strategy_name] += self.learning_rate
                    # 确保不超过1.0
                    self.strategy_scores[strategy_name] = min(1.0, self.strategy_scores[strategy_name])
                else:
                    self.strategy_scores[strategy_name] -= self.learning_rate * 0.5
                    # 确保不低于0.1
                    self.strategy_scores[strategy_name] = max(0.1, self.strategy_scores[strategy_name])
    
    def _get_strategy_name(self, strategy_type: str, strategy_value: Any) -> str:
        """将策略类型和值转换为标准策略名称"""
        if strategy_type == 'fingerprint':
            if isinstance(strategy_value, dict) and strategy_value.get('advanced', False):
                return 'fingerprint_advanced'
            return 'fingerprint_standard'
        elif strategy_type == 'delay':
            if strategy_value <= 2:
                return 'delay_short'
            elif strategy_value <= 5:
                return 'delay_medium'
            return 'delay_long'
        elif strategy_type == 'request_chain':
            if len(strategy_value) <= 3:
                return 'request_chain_short'
            elif len(strategy_value) <= 7:
                return 'request_chain_medium'
            return 'request_chain_long'
        elif strategy_type == 'proxy':
            if not strategy_value:
                return 'proxy_direct'
            elif isinstance(strategy_value, str):
                return 'proxy_single'
            return 'proxy_chain'
        return f"{strategy_type}_{strategy_value}"
    
    def _update_site_profile(self, domain: str, is_success: bool, strategies_used: Dict[str, Any]):
        """更新站点配置文件"""
        if domain not in self.site_profiles:
            self.site_profiles[domain] = {
                'success_count': 0,
                'failure_count': 0,
                'last_visit': time.time(),
                'preferred_strategies': {},
                'difficulty_level': 0.5  # 默认中等难度
            }
        
        profile = self.site_profiles[domain]
        
        # 更新统计信息
        if is_success:
            profile['success_count'] += 1
        else:
            profile['failure_count'] += 1
        
        profile['last_visit'] = time.time()
        
        # 更新首选策略
        for strategy_type, strategy_value in strategies_used.items():
            strategy_name = self._get_strategy_name(strategy_type, strategy_value)
            if strategy_name not in profile['preferred_strategies']:
                profile['preferred_strategies'][strategy_name] = 0
            
            # 根据成功/失败更新策略权重
            if is_success:
                profile['preferred_strategies'][strategy_name] += 1
            else:
                profile['preferred_strategies'][strategy_name] -= 0.5
                if profile['preferred_strategies'][strategy_name] < 0:
                    profile['preferred_strategies'][strategy_name] = 0
        
        # 更新难度级别
        total_attempts = profile['success_count'] + profile['failure_count']
        if total_attempts > 0:
            failure_rate = profile['failure_count'] / total_attempts
            profile['difficulty_level'] = min(1.0, max(0.1, failure_rate))
    
    def get_optimized_strategies(self, url: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        根据历史数据和站点配置文件获取优化的策略
        
        Args:
            url: 目标URL
            context: 额外上下文信息
            
        Returns:
            优化后的策略配置
        """
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        
        # 获取站点配置文件（如果存在）
        profile = self.site_profiles.get(domain, {})
        difficulty = profile.get('difficulty_level', 0.5)
        preferred_strategies = profile.get('preferred_strategies', {})
        
        # 检查冷却期
        if 'last_response' in profile and 'cooldown' in profile['last_response']:
            elapsed = time.time() - profile.get('response_timestamp', 0)
            if elapsed < profile['last_response']['cooldown']:
                # 冷却期内使用保守策略
                self.logger.info(f"{domain} 仍在冷却期，使用保守策略")
                strategies = self._get_defensive_strategies()
                self.logger.debug(f"为 {url} 选择防御策略: {strategies}")
                return strategies
        
        # 获取当前行为模式参数
        pattern_params = self.behavior_patterns[self.current_behavior_pattern]
        
        # 基于难度、行为模式和历史数据选择策略
        strategies = {
            'fingerprint': self._select_fingerprint_strategy(difficulty, preferred_strategies),
            'delay': self._select_delay_strategy(difficulty, preferred_strategies) * pattern_params['delay_multiplier'],
            'request_chain': self._select_request_chain_strategy(difficulty, preferred_strategies),
            'proxy': self._select_proxy_strategy(difficulty, preferred_strategies),
            'behavior_pattern': self.current_behavior_pattern,
            'risk_level': self.environment_awareness['detection_risk']
        }
        
        # 根据上下文调整
        if context:
            strategies = self._adjust_strategies_for_context(strategies, context)
        
        self.logger.debug(f"为 {url} 选择优化策略: {strategies}")
        return strategies
    
    def _get_defensive_strategies(self) -> Dict[str, Any]:
        """获取防御性策略"""
        return {
            'fingerprint': {'advanced': True},
            'delay': 8.0,
            'request_chain': self._select_request_chain_strategy(0.9, {}),
            'proxy': self._select_proxy_strategy(0.9, {}),
            'behavior_pattern': 'stealth',
            'risk_level': 1.0
        }
    
    def _adjust_strategies_for_context(self, strategies: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """根据上下文调整策略"""
        # 检测特殊情况
        if context.get('captcha_detected', False):
            strategies['behavior_pattern'] = 'stealth'
            strategies['delay'] = max(strategies['delay'], 10.0)
        
        if context.get('rate_limited', False):
            strategies['delay'] *= 2.0
        
        # 根据网站类型调整
        site_type = context.get('site_type', '')
        if site_type == 'ecommerce':
            strategies['fingerprint']['advanced'] = True
        elif site_type == 'social_media':
            strategies['behavior_pattern'] = 'careful'
        
        return strategies
    
    def _select_fingerprint_strategy(self, difficulty: float, preferred_strategies: Dict[str, float]) -> Dict[str, Any]:
        """选择指纹策略"""
        # 获取当前行为模式的探索率
        pattern_exploration = self.behavior_patterns[self.current_behavior_pattern]['exploration_rate']
        
        # 有一定概率探索新策略
        if random.random() < pattern_exploration:
            return {'advanced': random.random() > 0.3}
        
        # 否则基于难度、风险和历史数据选择
        risk = self.environment_awareness['detection_risk']
        score_advanced = preferred_strategies.get('fingerprint_advanced', 0) + self.strategy_scores.get('fingerprint_advanced', 0.8) * 10
        score_standard = preferred_strategies.get('fingerprint_standard', 0) + self.strategy_scores.get('fingerprint_standard', 0.7) * 10
        
        # 难度或风险越高，越倾向于使用高级指纹
        if difficulty > 0.7 or risk > 0.5 or score_advanced > score_standard:
            return {'advanced': True}
        return {'advanced': False}
    
    def _select_delay_strategy(self, difficulty: float, preferred_strategies: Dict[str, float]) -> float:
        """选择延迟策略"""
        # 有一定概率探索新策略
        if random.random() < self.exploration_rate:
            return random.uniform(1.0, 8.0)
        
        # 基于难度和历史数据计算最佳延迟
        if difficulty > 0.8:
            # 高难度站点使用较长延迟
            return random.uniform(4.0, 8.0)
        elif difficulty > 0.5:
            # 中等难度站点使用中等延迟
            return random.uniform(2.0, 5.0)
        else:
            # 低难度站点使用较短延迟
            return random.uniform(1.0, 3.0)
    
    def _select_request_chain_strategy(self, difficulty: float, preferred_strategies: Dict[str, float]) -> List[str]:
        """选择请求链策略"""
        # 基础资源列表
        base_resources = global_config.get('behavior_simulation.pollution_resources', [
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'https://fonts.googleapis.com/css?family=Roboto',
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css'
        ])
        
        # 基于难度确定链长度
        if difficulty > 0.8:
            # 高难度站点使用较长请求链
            chain_length = random.randint(5, 8)
        elif difficulty > 0.5:
            # 中等难度站点使用中等请求链
            chain_length = random.randint(3, 5)
        else:
            # 低难度站点使用较短请求链
            chain_length = random.randint(1, 3)
        
        # 随机选择资源
        selected_resources = random.sample(base_resources, min(len(base_resources), chain_length))
        return selected_resources
    
    def _select_proxy_strategy(self, difficulty: float, preferred_strategies: Dict[str, float]) -> Any:
        """选择代理策略"""
        proxy_chain = global_config.get('proxy_chain', [])
        
        # 如果没有代理可用，直接返回None
        if not proxy_chain:
            return None
        
        # 基于难度选择代理策略
        if difficulty > 0.7:
            # 高难度站点使用代理链
            if len(proxy_chain) >= 2:
                return random.sample(proxy_chain, 2)
            return proxy_chain[0]
        elif difficulty > 0.4:
            # 中等难度站点使用单个代理
            return random.choice(proxy_chain)
        else:
            # 低难度站点可能不使用代理
            if random.random() < 0.7:
                return None
            return random.choice(proxy_chain)
    
    def detect_pattern_changes(self, url: str, recent_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        检测网站模式变化
        
        Args:
            url: 目标URL
            recent_results: 最近的爬取结果
            
        Returns:
            变化检测结果，包含是否有变化及详细信息
        """
        result = {
            'has_changes': False,
            'change_type': None,
            'confidence': 0.0,
            'details': {}
        }
        
        if len(recent_results) < 3:
            return result
        
        # 分析最近结果中的变化
        status_codes = [r.get('status_code') for r in recent_results]
        content_lengths = [len(r.get('content', '')) for r in recent_results]
        
        # 检测状态码突然变化
        if len(set(status_codes)) > 2 and status_codes[-1] != 200:
            result['has_changes'] = True
            result['change_type'] = 'status_code_change'
            result['confidence'] = 0.9
            result['details']['status_codes'] = status_codes
            self.logger.warning(f"检测到状态码模式变化: {status_codes}")
        
        # 检测内容长度突然变化（超过50%）
        if len(content_lengths) >= 3 and not result['has_changes']:
            recent_avg = sum(content_lengths[-3:-1]) / 2
            if recent_avg > 0:
                change_ratio = abs(content_lengths[-1] - recent_avg) / recent_avg
                if change_ratio > 0.5:
                    result['has_changes'] = True
                    result['change_type'] = 'content_length_change'
                    result['confidence'] = min(1.0, change_ratio)
                    result['details']['change_ratio'] = change_ratio
                    self.logger.warning(f"检测到内容长度变化: {change_ratio:.2%}")
        
        # 检测成功率变化
        success_rates = []
        window_size = 5
        for i in range(len(recent_results) - window_size + 1):
            window = recent_results[i:i+window_size]
            success_count = sum(1 for r in window if r.get('status_code') == 200)
            success_rates.append(success_count / window_size)
        
        if len(success_rates) >= 3 and not result['has_changes']:
            if success_rates[-1] < 0.4 and success_rates[0] > 0.6:
                result['has_changes'] = True
                result['change_type'] = 'success_rate_drop'
                result['confidence'] = 0.8
                result['details']['success_rate_drop'] = f"从 {success_rates[0]:.2f} 降至 {success_rates[-1]:.2f}"
                self.logger.warning(f"检测到成功率显著下降: {success_rates[0]:.2f} -> {success_rates[-1]:.2f}")
        
        return result
    
    def shift_behavior_pattern(self):
        """手动切换行为模式"""
        # 可用模式
        patterns = list(self.behavior_patterns.keys())
        patterns.remove(self.current_behavior_pattern)
        
        # 根据风险选择新模式
        risk = self.environment_awareness['detection_risk']
        
        if risk > 0.7:
            # 高风险时优先选择隐蔽模式
            if 'stealth' in patterns:
                self._change_behavior_pattern('stealth')
            else:
                self._change_behavior_pattern('careful')
        else:
            # 随机选择一个新模式
            new_pattern = random.choice(patterns)
            self._change_behavior_pattern(new_pattern)
    
    def get_metacognitive_insights(self) -> Dict[str, Any]:
        """
        获取元认知洞察报告
        
        Returns:
            包含系统状态、性能和建议的洞察报告
        """
        # 计算总体统计数据
        total_attempts = len(self.success_history) + len(self.failure_history)
        success_rate = len(self.success_history) / total_attempts if total_attempts > 0 else 0
        
        # 分析最佳策略
        best_strategies = self._analyze_best_strategies()
        
        # 识别高风险站点
        high_risk_sites = []
        for domain, profile in self.site_profiles.items():
            if profile.get('difficulty_level', 0) > 0.7:
                high_risk_sites.append({
                    'domain': domain,
                    'difficulty': profile['difficulty_level'],
                    'success_rate': profile['success_count'] / (profile['success_count'] + profile['failure_count']) if profile['success_count'] + profile['failure_count'] > 0 else 0,
                    'last_visit': profile['last_visit']
                })
        
        # 生成建议
        recommendations = self._generate_recommendations()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'system_state': {
                'detection_risk': self.environment_awareness['detection_risk'],
                'current_behavior_pattern': self.current_behavior_pattern,
                'resource_pressure': self.environment_awareness['resource_pressure'],
                'system_performance': self.environment_awareness['system_performance']
            },
            'statistics': {
                'total_attempts': total_attempts,
                'success_rate': success_rate,
                'known_sites': len(self.site_profiles),
                'high_risk_sites': len(high_risk_sites)
            },
            'best_strategies': best_strategies,
            'high_risk_sites': high_risk_sites,
            'recommendations': recommendations
        }
    
    def _analyze_best_strategies(self) -> Dict[str, Any]:
        """分析最佳策略"""
        # 分析策略成功率
        strategy_stats = {}
        
        # 统计成功的策略
        for record in self.success_history[-200:]:  # 分析最近200次成功
            for strategy_type, strategy_value in record.get('strategies', {}).items():
                strategy_name = self._get_strategy_name(strategy_type, strategy_value)
                if strategy_name not in strategy_stats:
                    strategy_stats[strategy_name] = {'success': 0, 'total': 0}
                strategy_stats[strategy_name]['success'] += 1
                strategy_stats[strategy_name]['total'] += 1
        
        # 统计失败的策略
        for record in self.failure_history[-200:]:  # 分析最近200次失败
            for strategy_type, strategy_value in record.get('strategies', {}).items():
                strategy_name = self._get_strategy_name(strategy_type, strategy_value)
                if strategy_name not in strategy_stats:
                    strategy_stats[strategy_name] = {'success': 0, 'total': 0}
                strategy_stats[strategy_name]['total'] += 1
        
        # 计算成功率并排序
        best_strategies = []
        for strategy, stats in strategy_stats.items():
            if stats['total'] >= 10:  # 至少10次尝试
                success_rate = stats['success'] / stats['total']
                best_strategies.append({
                    'strategy': strategy,
                    'success_rate': success_rate,
                    'total_attempts': stats['total']
                })
        
        # 按成功率排序
        best_strategies.sort(key=lambda x: x['success_rate'], reverse=True)
        
        return best_strategies[:5]  # 返回前5个最佳策略
    
    def _generate_recommendations(self) -> List[Dict[str, Any]]:
        """生成优化建议"""
        recommendations = []
        risk = self.environment_awareness['detection_risk']
        success_rate = self.environment_awareness['system_performance']['success_rate']
        resource_pressure = self.environment_awareness['resource_pressure']
        
        # 风险相关建议
        if risk > 0.8:
            recommendations.append({
                'level': 'critical',
                'message': '检测风险极高，系统可能面临被封禁的风险',
                'action': '立即切换到隐身模式，降低爬取频率，增加请求间隔至少到10秒'
            })
        elif risk > 0.6:
            recommendations.append({
                'level': 'warning',
                'message': '检测风险较高，建议调整策略',
                'action': '切换到谨慎模式，增加请求间隔，减少并发'
            })
        
        # 成功率相关建议
        if success_rate < 0.6 and success_rate > 0:
            recommendations.append({
                'level': 'warning',
                'message': '成功率较低，需要优化策略',
                'action': '分析失败原因，考虑使用更高级的指纹策略和代理链'
            })
        
        # 资源使用建议
        if resource_pressure['cpu'] > 0.8:
            recommendations.append({
                'level': 'warning',
                'message': 'CPU使用率过高',
                'action': '降低并发数，减少同时处理的任务'
            })
        
        if resource_pressure['memory'] > 0.8:
            recommendations.append({
                'level': 'warning',
                'message': '内存使用率过高',
                'action': '增加资源回收频率，减少缓存大小'
            })
        
        # 行为模式建议
        if self.current_behavior_pattern == 'hurried' and risk > 0.4:
            recommendations.append({
                'level': 'warning',
                'message': '当前使用匆忙模式但风险较高',
                'action': '建议切换到普通或谨慎模式'
            })
        
        return recommendations
    
    def shutdown(self):
        """关闭元认知引擎"""
        self.logger.info("正在关闭元认知引擎...")
        self._save_knowledge()
        self.logger.info("元认知引擎已关闭，知识库已保存")
    
    def generate_adaptive_response(self, url: str, detected_changes: bool = False) -> Dict[str, Any]:
        """
        生成自适应响应策略
        
        Args:
            url: 目标URL
            detected_changes: 是否检测到变化
            
        Returns:
            自适应响应策略
        """
        if detected_changes:
            print(f"[Metacognition] 为 {url} 生成紧急响应策略")
            # 紧急响应：显著改变策略
            return {
                'fingerprint_reset': True,
                'delay_increase_factor': 1.5,
                'request_chain_expand': True,
                'force_proxy_change': True,
                'behavior_shift': True
            }
        else:
            # 常规自适应：微调策略
            return {
                'fingerprint_reset': False,
                'delay_increase_factor': 1.0,
                'request_chain_expand': False,
                'force_proxy_change': False,
                'behavior_shift': False
            }