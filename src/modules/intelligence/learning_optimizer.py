# PhantomCrawler - 学习与优化模块
import numpy as np
import random
import time
from typing import Dict, List, Any, Optional, Tuple
from collections import deque
import heapq

class LearningOptimizer:
    """
    学习与优化器 - 基于强化学习的策略优化系统
    使用Q-learning和经验回放来优化爬取策略
    """
    
    def __init__(self, state_dim: int = 8, action_dim: int = 6):
        # Q-learning参数
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.exploration_rate = 0.2
        self.exploration_decay = 0.995
        self.min_exploration_rate = 0.05
        
        # Q-表初始化
        self.q_table = np.zeros((state_dim, action_dim))
        
        # 经验回放缓冲区
        self.replay_buffer = deque(maxlen=1000)
        self.batch_size = 32
        
        # 策略评估
        self.strategy_performance = {}
        self.best_strategies = []
        
        # 学习状态
        self.current_state = 0
        self.previous_state = 0
        self.previous_action = 0
        
        # 初始化策略性能记录
        self._initialize_strategy_performance()
    
    def _initialize_strategy_performance(self):
        """初始化策略性能记录"""
        strategy_types = [
            'fingerprint_strategies',
            'delay_strategies',
            'request_chain_strategies',
            'proxy_strategies',
            'behavior_strategies'
        ]
        
        for strategy_type in strategy_types:
            self.strategy_performance[strategy_type] = {
                'total_attempts': 0,
                'successful_attempts': 0,
                'success_rate': 0.0,
                'average_reward': 0.0,
                'rewards_history': []
            }
    
    def encode_state(self, observation: Dict[str, Any]) -> int:
        """
        将观察到的环境状态编码为状态索引
        
        Args:
            observation: 环境观察（包含各种指标）
            
        Returns:
            状态索引
        """
        # 提取关键指标
        success_rate = observation.get('success_rate', 1.0)
        response_time = observation.get('avg_response_time', 2.0)
        error_rate = observation.get('error_rate', 0.0)
        resource_pressure = observation.get('resource_pressure', 0.0)
        
        # 将连续值离散化为状态
        # 0: 最优状态 (高成功率, 低响应时间, 低错误率)
        # 1-7: 不同级别的退化状态
        
        if success_rate > 0.9 and response_time < 3 and error_rate < 0.05:
            return 0
        elif success_rate > 0.8 and response_time < 5 and error_rate < 0.1:
            return 1
        elif success_rate > 0.7 and response_time < 8 and error_rate < 0.2:
            return 2
        elif success_rate > 0.6 and response_time < 10 and error_rate < 0.3:
            return 3
        elif success_rate > 0.5 and response_time < 15 and error_rate < 0.4:
            return 4
        elif success_rate > 0.4:
            return 5
        elif success_rate > 0.2:
            return 6
        else:
            return 7  # 最差状态
    
    def select_action(self, state: int) -> int:
        """
        根据ε-贪婪策略选择动作
        
        Args:
            state: 当前状态索引
            
        Returns:
            动作索引
        """
        # 探索
        if random.random() < self.exploration_rate:
            return random.randint(0, self.action_dim - 1)
        # 利用
        else:
            return np.argmax(self.q_table[state])
    
    def decode_action(self, action: int) -> Dict[str, Any]:
        """
        将动作索引解码为具体的策略调整
        
        Args:
            action: 动作索引
            
        Returns:
            策略调整字典
        """
        # 定义可能的动作
        actions = {
            0: {'adjustment_type': 'fingerprint', 'action': 'enhance', 'intensity': 0.2},
            1: {'adjustment_type': 'delay', 'action': 'increase', 'intensity': 0.3},
            2: {'adjustment_type': 'request_chain', 'action': 'lengthen', 'intensity': 0.4},
            3: {'adjustment_type': 'proxy', 'action': 'change', 'intensity': 1.0},
            4: {'adjustment_type': 'behavior', 'action': 'humanize', 'intensity': 0.3},
            5: {'adjustment_type': 'conservative', 'action': 'reduce_speed', 'intensity': 0.5}
        }
        
        return actions.get(action, actions[0])
    
    def calculate_reward(self, success: bool, metrics: Dict[str, Any]) -> float:
        """
        计算当前动作的奖励值
        
        Args:
            success: 是否成功
            metrics: 包含各种指标的字典
            
        Returns:
            奖励值
        """
        base_reward = 10.0 if success else -15.0
        
        # 响应时间惩罚
        response_time = metrics.get('response_time', 2.0)
        time_penalty = min(5.0, response_time * 0.5)
        
        # 资源使用惩罚
        resource_usage = metrics.get('resource_usage', 0.3)
        resource_penalty = resource_usage * 2.0
        
        # 连续成功奖励
        streak = metrics.get('success_streak', 1)
        streak_bonus = min(10.0, streak * 0.5)
        
        # 组合奖励
        total_reward = base_reward - time_penalty - resource_penalty + streak_bonus
        
        # 确保奖励在合理范围内
        return max(-20.0, min(20.0, total_reward))
    
    def learn(self, state: int, action: int, reward: float, next_state: int):
        """
        更新Q-表
        
        Args:
            state: 当前状态
            action: 执行的动作
            reward: 获得的奖励
            next_state: 下一个状态
        """
        # Q-learning更新公式
        old_value = self.q_table[state, action]
        next_max = np.max(self.q_table[next_state])
        
        new_value = old_value + self.learning_rate * (reward + self.discount_factor * next_max - old_value)
        self.q_table[state, action] = new_value
        
        # 衰减探索率
        self.exploration_rate = max(
            self.min_exploration_rate,
            self.exploration_rate * self.exploration_decay
        )
    
    def store_experience(self, state: int, action: int, reward: float, next_state: int):
        """
        将经验存储到回放缓冲区
        
        Args:
            state: 当前状态
            action: 执行的动作
            reward: 获得的奖励
            next_state: 下一个状态
        """
        self.replay_buffer.append((state, action, reward, next_state))
    
    def replay_experiences(self):
        """
        从经验回放缓冲区中学习
        """
        if len(self.replay_buffer) < self.batch_size:
            return
        
        # 随机采样批次
        batch = random.sample(self.replay_buffer, self.batch_size)
        
        for state, action, reward, next_state in batch:
            self.learn(state, action, reward, next_state)
    
    def update_strategy_performance(self, strategy_type: str, success: bool, reward: float):
        """
        更新策略性能记录
        
        Args:
            strategy_type: 策略类型
            success: 是否成功
            reward: 获得的奖励
        """
        if strategy_type not in self.strategy_performance:
            self.strategy_performance[strategy_type] = {
                'total_attempts': 0,
                'successful_attempts': 0,
                'success_rate': 0.0,
                'average_reward': 0.0,
                'rewards_history': []
            }
        
        perf = self.strategy_performance[strategy_type]
        perf['total_attempts'] += 1
        
        if success:
            perf['successful_attempts'] += 1
        
        perf['success_rate'] = perf['successful_attempts'] / perf['total_attempts']
        perf['rewards_history'].append(reward)
        
        # 计算平均奖励
        if len(perf['rewards_history']) > 0:
            perf['average_reward'] = sum(perf['rewards_history'][-100:]) / len(perf['rewards_history'][-100:])
        
        # 更新最佳策略列表
        self._update_best_strategies(strategy_type, perf)
    
    def _update_best_strategies(self, strategy_type: str, performance: Dict[str, Any]):
        """
        更新最佳策略堆
        """
        # 使用成功率作为主要评分，平均奖励作为次要评分
        score = performance['success_rate'] * 0.7 + performance['average_reward'] * 0.3
        
        # 保留前5个最佳策略
        heapq.heappush(self.best_strategies, (-score, strategy_type, time.time()))
        
        # 只保留最近的记录
        self.best_strategies = [(s, t, ts) for s, t, ts in self.best_strategies if time.time() - ts < 3600][:5]
    
    def get_best_strategies(self, top_n: int = 3) -> List[Tuple[str, float]]:
        """
        获取表现最好的策略
        
        Args:
            top_n: 返回前N个策略
            
        Returns:
            策略类型和得分的列表
        """
        # 从堆中提取排序后的策略
        sorted_strategies = sorted(self.best_strategies, key=lambda x: (x[0], -x[2]))
        
        # 转换为正得分并返回
        return [(strategy_type, -score) for score, strategy_type, _ in sorted_strategies[:top_n]]
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """
        获取学习过程摘要
        
        Returns:
            学习摘要字典
        """
        # 计算整体性能指标
        total_success = sum(p['successful_attempts'] for p in self.strategy_performance.values())
        total_attempts = sum(p['total_attempts'] for p in self.strategy_performance.values())
        
        overall_success_rate = total_success / total_attempts if total_attempts > 0 else 0
        
        return {
            'learning_parameters': {
                'learning_rate': self.learning_rate,
                'exploration_rate': self.exploration_rate,
                'discount_factor': self.discount_factor
            },
            'performance': {
                'overall_success_rate': overall_success_rate,
                'best_strategies': self.get_best_strategies(),
                'strategy_details': {k: {
                    'success_rate': v['success_rate'],
                    'average_reward': v['average_reward'],
                    'attempts': v['total_attempts']
                } for k, v in self.strategy_performance.items()}
            },
            'q_table_stats': {
                'average_q_value': np.mean(self.q_table),
                'max_q_value': np.max(self.q_table),
                'min_q_value': np.min(self.q_table)
            }
        }
    
    def suggest_adaptation(self, current_performance: Dict[str, Any]) -> Dict[str, Any]:
        """
        根据当前性能建议适应性调整
        
        Args:
            current_performance: 当前性能指标
            
        Returns:
            建议的调整方案
        """
        success_rate = current_performance.get('success_rate', 0.8)
        response_time = current_performance.get('avg_response_time', 3.0)
        error_rate = current_performance.get('error_rate', 0.0)
        pattern = current_performance.get('current_pattern', 'normal')
        
        adaptations = []
        
        # 基于成功率的调整
        if success_rate < 0.6:
            adaptations.append({
                'priority': 'high',
                'type': 'drastic_change',
                'description': '成功率过低，建议全面调整策略',
                'actions': ['change_fingerprint', 'switch_proxy', 'increase_delay']
            })
        elif success_rate < 0.8:
            adaptations.append({
                'priority': 'medium',
                'type': 'moderate_change',
                'description': '成功率一般，建议适度调整',
                'actions': ['enhance_fingerprint', 'lengthen_request_chain']
            })
        
        # 使用辅助方法生成适应建议
        # 基于响应时间的调整
        if response_time > 8.0 and success_rate > 0.8:
            adaptations.append(self._create_adaptation_suggestion(
                priority='low',
                type_='efficiency_improvement',
                description='响应时间过长但成功率高，可适度优化效率',
                actions=['optimize_delay', 'reduce_request_chain']
            ))
        
        # 基于错误率的调整
        if error_rate > 0.3:
            adaptations.append(self._create_adaptation_suggestion(
                priority='high',
                type_='stability_improvement',
                description='错误率过高，建议提高稳定性',
                actions=['increase_retry', 'improve_error_handling']
            ))
        
        # 基于检测模式的调整
        if pattern == 'blocked':
            adaptations.append(self._create_adaptation_suggestion(
                priority='critical',
                type_='emergency_evasion',
                description='检测到被封锁，执行紧急规避',
                actions=['reset_all', 'use_stealth_mode', 'reduce_frequency']
            ))
        elif pattern == 'suspicious':
            adaptations.append(self._create_adaptation_suggestion(
                priority='high',
                type_='evasion_tactics',
                description='检测到可疑行为，执行规避策略',
                actions=['change_behavior_pattern', 'vary_request_timing']
            ))
        
        # 如果没有特定调整建议，提供常规优化
        if not adaptations:
            adaptations.append(self._create_adaptation_suggestion(
                priority='low',
                type_='routine_optimization',
                description='性能良好，执行常规优化',
                actions=['fine_tune_parameters', 'update_fingerprints']
            ))
        
        return {
            'timestamp': time.time(),
            'current_performance': current_performance,
            'suggested_adaptations': adaptations,
            'confidence': self._calculate_adaptation_confidence(adaptations)
        }
    
    def _create_adaptation_suggestion(self, priority: str, type_: str, description: str, actions: List[str]) -> Dict[str, Any]:
        """
        创建适应建议条目
        
        Args:
            priority: 优先级（critical/high/low）
            type_: 调整类型
            description: 描述
            actions: 建议执行的操作列表
            
        Returns:
            适应建议字典
        """
        return {
            'priority': priority,
            'type': type_,
            'description': description,
            'actions': actions
        }
    
    def _calculate_adaptation_confidence(self, adaptations: List[Dict[str, Any]]) -> float:
        """
        计算适应建议的置信度
        
        Args:
            adaptations: 适应建议列表
            
        Returns:
            置信度值（0-1）
        """
        # 基于优先级和历史学习计算置信度
        priority_weights = {
            'critical': 0.95,
            'high': 0.9,
            'medium': 0.75,
            'low': 0.6
        }
        
        if not adaptations:
            return 0.5
        
        # 取最高优先级的置信度，并结合学习状态
        highest_priority = max(adaptations, key=lambda x: priority_weights.get(x['priority'], 0.6))
        base_confidence = priority_weights.get(highest_priority['priority'], 0.6)
        
        # 考虑探索率对置信度的影响
        confidence = base_confidence * (1 - self.exploration_rate * 0.5)
        
        return min(1.0, max(0.1, confidence))
    
    def reset_learning(self):
        """
        重置学习状态
        """
        self.q_table = np.zeros((self.state_dim, self.action_dim))
        self.replay_buffer.clear()
        self.exploration_rate = 0.2
        self._initialize_strategy_performance()
        print("[LearningOptimizer] 学习状态已重置")