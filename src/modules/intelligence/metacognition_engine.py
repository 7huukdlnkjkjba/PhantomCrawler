# PhantomCrawler - 七宗欲引擎 | 实战加强版
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

# 欲望之力监控器
class DesireMonitor:
    """欲望之力的监视者，记录七宗欲的活动"""
    def __init__(self, name="七宗欲引擎"):
        self.name = name
    
    def enlighten(self, message):
        print(f"[{self.name} 启示] {message}")
    
    def desire_awaken(self, desire, message):
        print(f"[{self.name} {desire}觉醒] {message}")
    
    def desire_conflict(self, desire1, desire2, message):
        print(f"[{self.name} {desire1}-{desire2}冲突] {message}")
    
    def desire_manifest(self, desire, message):
        print(f"[{self.name} {desire}显现] {message}")
    
    def desire_triumph(self, desire, message):
        print(f"[{self.name} {desire}凯旋] {message}")
    
    def desire_sacrifice(self, desire, message):
        print(f"[{self.name} {desire}献祭] {message}")
    
    def battlefield_report(self, stats):
        """战场报告，显示战斗状态"""
        print("=== 七宗欲战场报告 ===")
        print(f"当前主导欲望: {stats.get('dominant_desire', '未知')}")
        print(f"危险等级: {stats.get('danger_level', 0):.2f}")
        print(f"成功率: {stats.get('success_rate', 0):.2f}%")
        print(f"资源状态: CPU={stats.get('cpu_usage', 0):.1f}% 内存={stats.get('memory_usage', 0):.1f}%")
        print(f"已连续胜利: {stats.get('success_streak', 0)}次")
        print("======================")

class SevenDesiresEngine:
    """
    七宗欲元认知引擎 - PhantomCrawler的智能核心系统
    整合七宗欲驱动机制与高级元认知能力，实现自适应爬虫策略
    具备欲望冲突管理、环境感知、模式识别和战略转换能力
    """
    
    def __init__(self):
        # 欲望知识库
        self.desire_knowledge = {}
        self.triumph_history = []  # 成功历史
        self.defeat_history = []    # 失败历史
        self.desire_strengths = {}  # 欲望强度
        self.target_profiles = {}   # 目标档案
        self.success_streak = 0     # 连续成功次数
        
        # 七宗欲之力（实战版）
        self.desire_forces = {
            '傲慢': 0.4,  # 追求高效与卓越
            '嫉妒': 0.3,  # 模仿成功模式
            '愤怒': 0.3,  # 面对阻碍时的激进反应
            '懒惰': 0.8,  # 寻求最省力的方式
            '贪婪': 0.5,  # 追求更多资源和数据
            '暴食': 0.4,  # 快速大量获取信息
            '色欲': 0.2   # 对目标的专注与执着
        }
        
        # 欲望参数
        self.enlightenment_rate = global_config.get('desires.enlightenment_rate', 0.1)  # 欲望觉醒率
        self.temptation_rate = global_config.get('desires.temptation_rate', 0.2)        # 欲望诱惑率
        self.memory_span = global_config.get('desires.memory_span', 1000)              # 记忆跨度
        self.karmic_factor = global_config.get('desires.karmic_factor', 0.9)            # 因果系数
        
        # 高级元认知感知系统
        self.desire_perception = {
            'detection_danger': 0.0,  # 被发现的危险
            'resource_hunger': {'cpu': 0.0, 'memory': 0.0, 'network': 0.0},  # 资源饥渴度
            'efficiency_score': {'avg_response_time': 0.0, 'success_rate': 0.0, 'throughput': 0.0},  # 效率得分
            'target_resistance': 0.0,  # 目标抵抗强度
            'current_strategy_effectiveness': 1.0,  # 当前策略有效性
            'captcha_detection_count': 0,  # 验证码检测次数
            'block_attempts': 0,  # 被阻止尝试次数
            'pattern_recognition': {},  # 模式识别结果
            'environmental_context': {},  # 环境上下文
            'adaptive_confidence': 0.5  # 自适应置信度
        }
        
        # 当前主导欲望
        self.dominant_desire = '贪婪'  # 默认由贪婪主导
        self.desire_transition_history = []  # 欲望转换历史
        self.last_desire_shift = time.time()  # 上次欲望转换时间
        
        # 欲望平衡锁
        self.desire_lock = threading.RLock()
        
        # 欲望行为记录
        self.desire_manifestations = []
        
        # 行为模式映射（欲望 -> 行为模式）
        self.desire_patterns = {
            '傲慢': 'efficient',     # 高效模式
            '嫉妒': 'adaptive',      # 自适应模式
            '愤怒': 'aggressive',    # 激进模式
            '懒惰': 'minimal',       # 最小化模式
            '贪婪': 'balanced',      # 平衡模式
            '暴食': 'fast',          # 快速模式
            '色欲': 'stealth'        # 隐身模式
        }
        
        # 当前行为模式
        self.current_behavior_pattern = self.desire_patterns.get(self.dominant_desire, 'balanced')
        
        # 高级环境感知系统
        self.environment_awareness = {
            'detection_risk': 0.0,
            'pressure_level': 0.0,
            'current_efficiency': 0.0,
            'system_performance': {
                'avg_response_time': 0.0,
                'memory_usage': 0.0,
                'cpu_usage': 0.0
            },
            'network_conditions': {
                'latency': 0.0,
                'bandwidth': 0.0
            },
            'target_characteristics': {},  # 目标网站特性
            'historical_patterns': []      # 历史模式记录
        }
        
        # 欲望监控器
        try:
            self.monitor = DesireMonitor('七宗欲引擎')
        except:
            # 备用监控函数
            self.monitor = type('DesireMonitor', (), {
                'enlighten': lambda msg: print(f"[启示] {msg}"),
                'desire_awaken': lambda desire, msg: print(f"[{desire}觉醒] {msg}"),
                'desire_conflict': lambda d1, d2, msg: print(f"[{d1}-{d2}冲突] {msg}"),
                'desire_manifest': lambda desire, msg: print(f"[{desire}显现] {msg}")
            })()
    
    def shift_behavior_pattern(self, context=None):
        """
        智能切换行为模式 - 基于元认知分析的自适应行为调整
        
        Args:
            context: 上下文信息，包含环境状态、性能指标等
        
        Returns:
            新的行为模式
        """
        # 分析上下文信息
        if context:
            self._analyze_environmental_context(context)
        
        # 唤醒主导欲望决策
        self._awaken_dominant_desire()
        
        # 更新当前行为模式
        self.current_behavior_pattern = self.desire_patterns.get(self.dominant_desire, 'balanced')
        
        # 更新环境感知
        self.environment_awareness['current_behavior_pattern'] = self.current_behavior_pattern
        
        # 记录历史模式
        pattern_record = {
            'timestamp': time.time(),
            'pattern': self.current_behavior_pattern,
            'dominant_desire': self.dominant_desire,
            'context_summary': self._summarize_context(context)
        }
        self.environment_awareness['historical_patterns'].append(pattern_record)
        # 保持历史记录在合理范围内
        if len(self.environment_awareness['historical_patterns']) > 50:
            self.environment_awareness['historical_patterns'] = self.environment_awareness['historical_patterns'][-50:]
        
        return self.current_behavior_pattern
    
    def get_metacognitive_insights(self):
        """
        获取全面的元认知洞察报告 - 整合七宗欲引擎与元认知能力
        提供系统状态、环境感知、欲望效能和自适应策略分析
        
        Returns:
            详细的元认知洞察报告
        """
        # 计算成功率和统计信息
        total_attempts = len(self.triumph_history) + len(self.defeat_history)
        success_rate = (len(self.triumph_history) / total_attempts) * 100 if total_attempts > 0 else 0
        
        # 计算近期成功率（最近10次）
        recent_attempts = []
        for record in self.triumph_history[-10:]:
            recent_attempts.append((record.get('timestamp', 0) or record.get('time', 0), True))
        for record in self.defeat_history[-10:]:
            recent_attempts.append((record.get('timestamp', 0) or record.get('time', 0), False))
        recent_attempts.sort(key=lambda x: x[0], reverse=True)
        recent_attempts = recent_attempts[:10]
        recent_success_count = sum(1 for _, success in recent_attempts if success)
        recent_success_rate = (recent_success_count / len(recent_attempts)) * 100 if recent_attempts else 0
        
        # 获取最近的行为模式
        recent_patterns = []
        if 'historical_patterns' in self.environment_awareness:
            recent_patterns = [p['pattern'] for p in self.environment_awareness['historical_patterns'][-10:]]
        pattern_frequency = {}
        for pattern in recent_patterns:
            pattern_frequency[pattern] = pattern_frequency.get(pattern, 0) + 1
        
        # 生成环境风险评估
        if hasattr(self, '_calculate_risk_assessment'):
            risk_assessment = self._calculate_risk_assessment()
        else:
            # 简化风险评估
            detection_danger = getattr(self.desire_perception, 'detection_danger', 0)
            risk_level = '低' if detection_danger < 0.4 else '中' if detection_danger < 0.7 else '高'
            risk_assessment = {
                'overall_risk': detection_danger,
                'risk_level': risk_level,
                'recommended_precautions': []
            }
        
        # 行为模式分析
        pattern_analysis = {
            'current_pattern': self.current_behavior_pattern,
            'pattern_frequency': pattern_frequency,
            'most_common_pattern': max(pattern_frequency.items(), key=lambda x: x[1])[0] if pattern_frequency else '未知'
        }
        
        # 欲望效能分析
        desire_effectiveness = self._analyze_desire_effectiveness() if hasattr(self, '_analyze_desire_effectiveness') else {
            'recommended_desire': self.dominant_desire
        }
        
        # 生成调整建议
        if hasattr(self, '_generate_adjustment_recommendations'):
            recommendations = self._generate_adjustment_recommendations()
        else:
            recommendations = []
            # 基于成功率生成基本建议
            if success_rate < 30:
                recommendations.append("成功率过低，建议更换策略")
            elif self.success_streak > 10:
                recommendations.append("连续成功，可以适度提高效率")
        
        # 计算信心分数
        confidence_score = self._calculate_confidence_score(success_rate / 100, risk_assessment['overall_risk'])
        
        # 获取资源使用情况
        resource_usage = getattr(self.desire_perception, 'resource_hunger', {})
        
        # 生成完整洞察报告
        insights = {
            'timestamp': time.time(),
            'system_state': {
                'current_behavior_pattern': self.current_behavior_pattern,
                'dominant_desire': self.dominant_desire,
                'success_streak': self.success_streak,
                'total_triumphs': len(self.triumph_history),
                'total_defeats': len(self.defeat_history),
                'total_attempts': total_attempts,
                'success_rate': success_rate,
                'recent_success_rate': recent_success_rate,
                'last_pattern_change': time.time() - self.last_desire_shift if hasattr(self, 'last_desire_shift') else 0,
                'confidence_score': confidence_score
            },
            'environmental_awareness': {
                'detection_risk': getattr(self.environment_awareness, 'detection_risk', getattr(self.desire_perception, 'detection_danger', 0)),
                'pressure_level': getattr(self.environment_awareness, 'pressure_level', 'normal'),
                'system_performance': getattr(self.environment_awareness, 'system_performance', {}),
                'target_characteristics': getattr(self.environment_awareness, 'target_characteristics', {})
            },
            'desire_state': {
                'active_forces': self.desire_forces.copy(),
                'dominant_desire': self.dominant_desire,
                'dominant_desire_strength': max(self.desire_forces.values()) if self.desire_forces else 0,
                'confidence_level': getattr(self.desire_perception, 'adaptive_confidence', 0.5)
            },
            'risk_assessment': risk_assessment,
            'pattern_analysis': pattern_analysis,
            'desire_effectiveness': desire_effectiveness,
            'resource_usage': resource_usage,
            'recommendations': recommendations,
            'throughput': {
                'requests_per_minute': self._calculate_rpm() if hasattr(self, '_calculate_rpm') else 0,
                'success_rate': success_rate
            }
        }
        
        # 更新缓存
        self._last_metacognitive_insights = insights
        
        return insights
    
    def _calculate_confidence_score(self, success_rate, risk_level):
        """
        计算系统当前的信心分数
        
        Args:
            success_rate: 成功率(0-1)
            risk_level: 风险级别(0-1)
        
        Returns:
            信心分数(0-1)
        """
        # 基于成功率和风险级别的加权计算
        success_weight = 0.6
        risk_weight = 0.4
        
        # 成功率贡献
        success_contribution = success_rate * success_weight
        
        # 风险级别贡献
        risk_contribution = (1.0 - risk_level) * risk_weight
        
        # 综合信心分数
        confidence = success_contribution + risk_contribution
        
        # 连续成功加成
        if self.success_streak > 5:
            streak_bonus = min(0.2, (self.success_streak - 5) * 0.02)
            confidence = min(1.0, confidence + streak_bonus)
        
        # 连续失败惩罚
        if hasattr(self, 'defeat_history') and len(self.defeat_history) >= 3:
            recent_failures = self.defeat_history[-3:]
            if all('time' in f for f in recent_failures):
                recent_time = time.time()
                if all(recent_time - f['time'] < 300 for f in recent_failures):  # 5分钟内连续失败
                    confidence = max(0.1, confidence - 0.15)
        
        return round(confidence, 2)
    
    def shutdown(self):
        """兼容旧版API：关闭引擎"""
        try:
            # 保存欲望知识
            self._save_desire_knowledge()
            # 生成战场报告
            if hasattr(self, 'monitor'):
                stats = {
                    'dominant_desire': self.dominant_desire,
                    'danger_level': self.desire_perception['detection_danger'],
                    'success_rate': (len(self.triumph_history) / (len(self.triumph_history) + len(self.defeat_history) + 1)) * 100,
                    'success_streak': self.success_streak
                }
                self.monitor.battlefield_report(stats)
        except Exception as e:
            print(f"[七宗欲引擎] 关闭时发生错误: {str(e)}")
    
    def record_failure(self, url, reason, strategies=None):
        """
        记录失败并执行元认知分析
        
        Args:
            url: 失败的URL
            reason: 失败原因
            strategies: 使用的策略
        """
        failure_record = {
            'url': url,
            'reason': reason,
            'time': time.time(),
            'strategies': strategies or {},
            'context': self.environment_awareness.copy(),
            'current_desires': self.desire_forces.copy()
        }
        
        self.defeat_history.append(failure_record)
        self.success_streak = 0
        
        # 基于失败类型的欲望调整
        reason_str = str(reason).lower() if reason else ''
        if 'captcha' in reason_str:
            self.desire_perception['captcha_detection_count'] = getattr(self.desire_perception, 'captcha_detection_count', 0) + 1
            self._manifest_desire('色欲', 0.2)    # 遇到验证码更专注
            self._manifest_desire('暴食', -0.2)   # 降低速度
        elif 'block' in reason_str or '403' in reason_str:
            self.desire_perception['block_attempts'] = getattr(self.desire_perception, 'block_attempts', 0) + 1
            self.desire_perception['detection_danger'] = min(1.0, getattr(self.desire_perception, 'detection_danger', 0) + 0.3)
            # 强制切换到色欲模式（最安全）
            self._awaken_dominant_desire('色欲')
            self._manifest_desire('傲慢', -0.3)   # 降低傲慢
        elif 'timeout' in reason_str:
            self._manifest_desire('懒惰', 0.1)    # 寻找更优路径
            self._manifest_desire('暴食', -0.1)   # 降低请求频率
        
        # 记录失败模式
        if len(self.defeat_history) >= 3:
            recent_failures = self.defeat_history[-3:]
            # 检测连续失败模式
            if all('captcha' in str(f.get('reason', '')).lower() for f in recent_failures):
                patterns = getattr(self.desire_perception, 'pattern_recognition', {}).get('detected_patterns', [])
                patterns.append('captcha_pattern')
                self.monitor.enlighten("检测到验证码模式，请更换身份")
            elif all('block' in str(f.get('reason', '')).lower() for f in recent_failures):
                patterns = getattr(self.desire_perception, 'pattern_recognition', {}).get('detected_patterns', [])
                patterns.append('block_pattern')
                self.monitor.enlighten("检测到封锁模式，请紧急调整策略")
        
    def detect_pattern_changes(self, url, recent_results):
        """兼容旧版API：检测模式变化"""
        # 简单实现，检查最近结果中是否有多个失败
        failure_count = sum(1 for r in recent_results if r.get('status_code', 200) >= 400 or 'error' in r)
        return failure_count > 2
    
    def generate_adaptive_response(self, url, pattern_changed):
        """兼容旧版API：生成自适应响应"""
        response = {
            'fingerprint_reset': pattern_changed,
            'delay_increase_factor': 1.5 if pattern_changed else 1.0,
            'force_proxy_change': pattern_changed,
            'behavior_shift': pattern_changed
        }
        return response
    
    def record_detection_attempt(self, url, detection_type):
        """兼容旧版API：记录检测尝试"""
        self.desire_perception['captcha_detection_count'] += 1 if detection_type == 'captcha_detected' else 0
        self.desire_perception['block_attempts'] += 1
    
    def update_risk_level(self, url, risk_change):
        """兼容旧版API：更新风险级别"""
        self.desire_perception['detection_danger'] = max(0, min(1, self.desire_perception['detection_danger'] + risk_change))
        # 同步到兼容的environment_awareness
        self.environment_awareness['detection_risk'] = self.desire_perception['detection_danger']
    
    def _analyze_environmental_context(self, context):
        """
        分析环境上下文信息，更新感知系统
        
        Args:
            context: 包含环境状态、性能指标等的上下文信息
        """
        # 提取并更新关键环境指标
        if 'risk_level' in context:
            self.desire_perception['detection_danger'] = context['risk_level']
            self.environment_awareness['detection_risk'] = context['risk_level']
        
        if 'pressure_level' in context:
            self.environment_awareness['pressure_level'] = context['pressure_level']
        
        if 'performance' in context:
            perf = context['performance']
            if 'response_time' in perf:
                self.desire_perception['efficiency_score']['avg_response_time'] = perf['response_time']
                self.environment_awareness['system_performance']['avg_response_time'] = perf['response_time']
            
            if 'cpu_usage' in perf:
                self.desire_perception['resource_hunger']['cpu'] = perf['cpu_usage']
                self.environment_awareness['system_performance']['cpu_usage'] = perf['cpu_usage']
            
            if 'memory_usage' in perf:
                self.desire_perception['resource_hunger']['memory'] = perf['memory_usage']
                self.environment_awareness['system_performance']['memory_usage'] = perf['memory_usage']
        
        # 分析目标网站特征
        if 'target_info' in context:
            self.environment_awareness['target_characteristics'] = context['target_info']
            # 根据目标特征调整欲望强度
            self._adjust_desires_by_target(context['target_info'])
        
        # 模式识别更新
        self._update_pattern_recognition(context)
    
    def _summarize_context(self, context):
        """
        总结上下文信息，生成简明摘要
        
        Args:
            context: 上下文信息
        
        Returns:
            上下文摘要
        """
        summary = []
        
        if 'risk_level' in context:
            summary.append(f"风险:{context['risk_level']:.2f}")
        
        if 'performance' in context and 'response_time' in context['performance']:
            summary.append(f"响应:{context['performance']['response_time']:.2f}s")
        
        if 'target_info' in context and 'domain' in context['target_info']:
            summary.append(f"目标:{context['target_info']['domain']}")
        
        return ", ".join(summary)
    
    def _calculate_risk_assessment(self):
        """
        计算综合风险评估
        
        Returns:
            风险评估结果
        """
        # 基础风险因素
        detection_risk = self.desire_perception['detection_danger']
        block_history = min(1.0, self.desire_perception['block_attempts'] / 5.0)
        captcha_risk = min(1.0, self.desire_perception['captcha_detection_count'] / 3.0)
        
        # 计算加权风险分数
        overall_risk = (
            detection_risk * 0.4 + 
            block_history * 0.3 + 
            captcha_risk * 0.3
        )
        
        # 风险等级分类
        risk_level = "低"
        if overall_risk > 0.7:
            risk_level = "高"
        elif overall_risk > 0.4:
            risk_level = "中"
        
        return {
            'overall_risk': overall_risk,
            'risk_level': risk_level,
            'contributing_factors': {
                'detection_risk': detection_risk,
                'block_history': block_history,
                'captcha_risk': captcha_risk
            },
            'recommended_precautions': self._generate_precautions(overall_risk)
        }
    
    def _generate_adjustment_recommendations(self):
        """
        生成行为调整建议
        
        Returns:
            调整建议列表
        """
        recommendations = []
        insights = self.get_metacognitive_insights()
        
        # 基于风险调整
        if insights['risk_assessment']['overall_risk'] > 0.7:
            recommendations.append("建议切换至隐身模式，降低请求频率")
            recommendations.append("考虑更换代理和指纹")
        elif insights['risk_assessment']['overall_risk'] > 0.4:
            recommendations.append("建议增加请求间隔，减少并发")
        
        # 基于性能调整
        response_time = self.desire_perception['efficiency_score'].get('avg_response_time', 0)
        if response_time > 5.0:
            recommendations.append("响应时间过长，建议增加超时设置")
        
        # 基于成功率调整
        if self.success_streak > 10 and insights['risk_assessment']['overall_risk'] < 0.3:
            recommendations.append("连续成功，可以适当提高爬取效率")
        elif len(self.defeat_history) > 5 and len(self.defeat_history) > len(self.triumph_history):
            recommendations.append("失败率较高，建议调整策略")
        
        # 基于资源使用调整
        cpu_usage = self.desire_perception['resource_hunger'].get('cpu', 0)
        if cpu_usage > 0.8:
            recommendations.append("CPU使用率过高，建议降低并发")
        
        return recommendations
    
    def _adjust_desires_by_target(self, target_info):
        """
        根据目标网站特征调整欲望强度
        
        Args:
            target_info: 目标网站信息
        """
        # 示例：根据目标特征动态调整欲望权重
        if 'security_level' in target_info:
            security = target_info['security_level']
            if security == 'high':
                # 高安全性网站：增强色欲(专注)和嫉妒(模仿)
                self.desire_forces['色欲'] = min(1.0, self.desire_forces['色欲'] + 0.2)
                self.desire_forces['嫉妒'] = min(1.0, self.desire_forces['嫉妒'] + 0.1)
                # 减弱贪婪和暴食
                self.desire_forces['贪婪'] = max(0.3, self.desire_forces['贪婪'] - 0.2)
                self.desire_forces['暴食'] = max(0.2, self.desire_forces['暴食'] - 0.2)
            elif security == 'low':
                # 低安全性网站：增强贪婪和暴食
                self.desire_forces['贪婪'] = min(1.0, self.desire_forces['贪婪'] + 0.2)
                self.desire_forces['暴食'] = min(1.0, self.desire_forces['暴食'] + 0.2)
        
        # 根据内容类型调整
        if 'content_type' in target_info:
            content_type = target_info['content_type']
            if content_type == 'dynamic':
                # 动态内容：增强懒惰(寻找最优路径)和嫉妒(模仿成功模式)
                self.desire_forces['懒惰'] = min(1.0, self.desire_forces['懒惰'] + 0.1)
                self.desire_forces['嫉妒'] = min(1.0, self.desire_forces['嫉妒'] + 0.1)
            elif content_type == 'static':
                # 静态内容：增强暴食(快速获取)和贪婪
                self.desire_forces['暴食'] = min(1.0, self.desire_forces['暴食'] + 0.1)
                self.desire_forces['贪婪'] = min(1.0, self.desire_forces['贪婪'] + 0.1)
    
    def _update_pattern_recognition(self, context):
        """
        更新模式识别结果
        
        Args:
            context: 上下文信息
        """
        # 简单实现：基于上下文识别模式
        patterns = []
        
        # 风险模式识别
        if 'risk_level' in context and context['risk_level'] > 0.7:
            patterns.append('high_risk_environment')
        
        # 性能模式识别
        if 'performance' in context:
            perf = context['performance']
            if 'response_time' in perf and perf['response_time'] > 10.0:
                patterns.append('slow_response')
        
        # 成功模式识别
        if self.success_streak > 5:
            patterns.append('success_streak')
        elif len(self.defeat_history) >= 3 and len(self.defeat_history) > len(self.triumph_history):
            patterns.append('failure_trend')
        
        self.desire_perception['pattern_recognition'] = {
            'detected_patterns': patterns,
            'timestamp': time.time()
        }
    
    def _generate_precautions(self, risk_level):
        """
        基于风险级别生成预防措施
        
        Args:
            risk_level: 风险级别
        
        Returns:
            预防措施列表
        """
        precautions = []
        
        if risk_level > 0.8:
            precautions.append("立即更换所有识别特征")
            precautions.append("大幅降低爬取频率")
            precautions.append("考虑暂停操作一段时间")
        elif risk_level > 0.6:
            precautions.append("更换代理IP")
            precautions.append("增加请求间隔至少2倍")
            precautions.append("减少单次爬取量")
        elif risk_level > 0.4:
            precautions.append("适度增加请求间隔")
            precautions.append("检查并更新请求头")
        
        return precautions
    
    def update_resource_usage(self, cpu, memory, network):
        """更新资源使用情况并进行元认知分析"""
        self.desire_perception['resource_hunger'] = {
            'cpu': cpu,
            'memory': memory,
            'network': network
        }
    
    def _save_desire_knowledge(self):
        """保存欲望知识"""
        # 简化实现
        knowledge = {
            'desire_forces': self.desire_forces,
            'triumph_history': self.triumph_history[-self.memory_span:],
            'defeat_history': self.defeat_history[-self.memory_span:],
            'dominant_desire': self.dominant_desire
        }
        # 这里可以添加保存到文件的逻辑
        if hasattr(self, 'monitor'):
            self.monitor.enlighten("欲望知识已保存")
        
        # 唤醒欲望记忆
        self._awaken_desire_memories()
        
        # 初始化欲望策略
        self._initialize_desire_strategies()
        
        # 初始化欲望模式
        self._initialize_desire_patterns()
        
        # 启动欲望监控
        self._start_desire_monitoring()
    
    def analyze_crawl_result(self, *args):
        """
        分析爬取结果并执行元认知学习
        
        Args:
            *args: 支持多种参数格式
                - (result_dict): 新版格式
                - (url, result_dict, additional_info): 旧版格式
        
        Returns:
            分析后的结果和建议
        """
        try:
            # 支持不同的参数格式
            if len(args) == 1:
                result = args[0]
            else:
                # 假设格式为(url, result_dict, additional_info)
                result = args[1] if len(args) > 1 else {}
            
            # 创建上下文信息
            context = {
                'target_info': {
                    'domain': result.get('domain', ''),
                    'url': result.get('url', '')
                },
                'performance': {
                    'response_time': result.get('response_time', 0),
                    'data_size': result.get('data_size', 0)
                },
                'risk_level': getattr(self.desire_perception, 'detection_danger', 0)
            }
            
            # 分析环境上下文
            if hasattr(self, '_analyze_environmental_context'):
                self._analyze_environmental_context(context)
            
            analysis_result = {
                'success': result.get('success'),
                'risk_level': result.get('risk_level', getattr(self.desire_perception, 'detection_danger', 0)),
                'recommended_action': 'continue' if result.get('success') else 'adjust_strategy'
            }
            
            if result.get('success'):
                # 记录成功
                success_record = {
                    'timestamp': time.time(),
                    'target': result.get('url'),
                    'data_size': result.get('data_size', 0),
                    'response_time': result.get('response_time', 0),
                    'behavior_pattern': getattr(self, 'current_behavior_pattern', 'default'),
                    'dominant_desire': self.get_dominant_desire() if hasattr(self, 'get_dominant_desire') else '未知'
                }
                self.triumph_history.append(success_record)
                self.success_streak += 1
                
                # 更新效率分数
                if hasattr(self.desire_perception, 'efficiency_score'):
                    if result.get('response_time'):
                        self.desire_perception['efficiency_score']['total_time'] = getattr(self.desire_perception['efficiency_score'], 'total_time', 0) + result['response_time']
                        self.desire_perception['efficiency_score']['request_count'] = getattr(self.desire_perception['efficiency_score'], 'request_count', 0) + 1
                        self.desire_perception['efficiency_score']['avg_response_time'] = (
                            self.desire_perception['efficiency_score']['total_time'] / 
                            self.desire_perception['efficiency_score']['request_count']
                        )
                
                # 成功模式分析和欲望调整
                if self.success_streak >= 5:
                    dominant = self.get_dominant_desire() if hasattr(self, 'get_dominant_desire') else '贪婪'
                    # 增强当前成功的主导欲望
                    self._manifest_desire(dominant, 0.1 * min(1.0, self.success_streak / 10))
                
                print(f"[七宗欲引擎] 爬取成功分析完成: {result.get('url', '未知URL')} (连续成功 {self.success_streak} 次)")
            else:
                # 处理失败
                self.record_failure(result.get('url', ''), result.get('error', 'unknown'))
                print(f"[七宗欲引擎] 爬取失败分析完成: {result.get('error', '未知错误')}")
            
            # 如果有元认知洞察方法，添加更多分析结果
            if hasattr(self, 'get_metacognitive_insights'):
                insights = self.get_metacognitive_insights()
                analysis_result['metacognitive_insights'] = insights
                analysis_result['recommendations'] = self._generate_adjustment_recommendations() if hasattr(self, '_generate_adjustment_recommendations') else []
            
            return analysis_result
        except Exception as e:
            print(f"[七宗欲引擎] 分析爬取结果时出错: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_dominant_desire(self):
        """
        获取当前主导欲望
        
        Returns:
            主导欲望名称
        """
        return max(self.desire_forces.items(), key=lambda x: x[1])[0]
    
    def _calculate_rpm(self):
        """
        计算每分钟请求数
        
        Returns:
            每分钟请求数
        """
        # 简单实现：计算最近的请求频率
        time_window = 60  # 1分钟
        recent_requests = 0
        current_time = time.time()
        
        for record in self.triumph_history:
            if current_time - record.get('timestamp', 0) < time_window or current_time - record.get('time', 0) < time_window:
                recent_requests += 1
        
        for record in self.defeat_history:
            if current_time - record.get('timestamp', 0) < time_window or current_time - record.get('time', 0) < time_window:
                recent_requests += 1
        
        return recent_requests
    
    def _initialize_desire_strategies(self):
        """初始化七宗欲策略强度"""
        self.desire_strengths = {
            'fingerprint_standard': 0.7,  # 懒惰的简单伪装
            'fingerprint_advanced': 0.8,  # 傲慢的完美伪装
            'delay_short': 0.6,           # 暴食的急切
            'delay_medium': 0.7,          # 贪婪的耐心
            'delay_long': 0.9,            # 色欲的专注
            'request_chain_short': 0.6,   # 懒惰的直接
            'request_chain_medium': 0.7,  # 贪婪的准备
            'request_chain_long': 0.8,    # 嫉妒的模仿
            'proxy_direct': 0.5,          # 傲慢的直接
            'proxy_single': 0.6,          # 贪婪的隐蔽
            'proxy_chain': 0.8,           # 愤怒的多重掩护
        }
    
    def _initialize_desire_patterns(self):
        """初始化七宗欲模式"""
        self.desire_patterns = {
            '傲慢': {
                'delay_multiplier': 0.8,      # 高效，不浪费时间
                'temptation_rate': 0.15,     # 谨慎的尝试
                'risk_threshold': 0.6,       # 愿意承担一定风险以展示卓越
                'resource_consumption': 0.65 # 合理使用资源
            },
            '嫉妒': {
                'delay_multiplier': 1.2,      # 仔细观察并模仿
                'temptation_rate': 0.1,      # 保守的探索
                'risk_threshold': 0.4,       # 不愿冒险，跟随成功模式
                'resource_consumption': 0.6  # 适度使用资源
            },
            '愤怒': {
                'delay_multiplier': 0.5,      # 急躁，快速行动
                'temptation_rate': 0.3,      # 激进的尝试
                'risk_threshold': 0.8,       # 高风险容忍度
                'resource_consumption': 0.9  # 大量消耗资源
            },
            '懒惰': {
                'delay_multiplier': 1.5,      # 拖延，缓慢行动
                'temptation_rate': 0.05,     # 几乎不探索新方法
                'risk_threshold': 0.2,       # 极低风险容忍度
                'resource_consumption': 0.3  # 最小化资源使用
            },
            '贪婪': {
                'delay_multiplier': 1.0,      # 平衡的节奏
                'temptation_rate': 0.25,     # 适度探索以获取更多
                'risk_threshold': 0.7,       # 愿意冒险以获取更多资源
                'resource_consumption': 0.8  # 大量使用资源以获取更多数据
            },
            '暴食': {
                'delay_multiplier': 0.6,      # 快速大量获取
                'temptation_rate': 0.2,      # 积极探索新目标
                'risk_threshold': 0.65,      # 中等风险容忍度
                'resource_consumption': 0.85 # 高资源消耗
            },
            '色欲': {
                'delay_multiplier': 2.0,      # 长时间专注
                'temptation_rate': 0.05,     # 几乎不被其他目标诱惑
                'risk_threshold': 0.3,       # 低风险容忍度
                'resource_consumption': 0.5  # 适度资源使用
            }
        }
    
    def _start_desire_monitoring(self):
        """启动欲望监控仪式"""
        def monitor_desires():
            while True:
                try:
                    # 每60秒平衡一次七宗欲之力
                    self._balance_desire_forces()
                    time.sleep(60)
                except Exception as e:
                    self.monitor.desire_conflict('傲慢', '懒惰', f"欲望监控出错: {e}")
        
        # 启动守护仪式
        monitoring_ritual = threading.Thread(target=monitor_desires, daemon=True)
        monitoring_ritual.start()
        self.monitor.enlighten("七宗欲监控仪式已启动")
    
    def _balance_desire_forces(self):
        """平衡七宗欲之力，避免某一欲望过度膨胀"""
        with self.desire_lock:
            # 计算最近的成功率以影响欲望强度
            recent_manifestations = self.triumph_history[-50:] + self.defeat_history[-50:]
            recent_manifestations.sort(key=lambda x: x.get('timestamp', 0))
            recent_manifestations = recent_manifestations[-50:]
            
            if recent_manifestations:
                # 计算成功比例
                triumph_count = len(self.triumph_history)
                total_count = len(self.triumph_history) + len(self.defeat_history)
                success_ratio = triumph_count / total_count if total_count > 0 else 0
                self.desire_perception['efficiency_score']['success_rate'] = success_ratio
                
                # 更新连续成功次数
                if recent_manifestations and 'success' in recent_manifestations[-1]:
                    if recent_manifestations[-1]['success']:
                        self.success_streak += 1
                    else:
                        self.success_streak = 0
                
                # 实战策略调整：基于成功比例和连续成功
                if self.success_streak > 5:
                    # 连续成功多次，傲慢和贪婪暴涨
                    self.desire_forces['傲慢'] = min(1.0, self.desire_forces['傲慢'] + 0.1)
                    self.desire_forces['贪婪'] = min(1.0, self.desire_forces['贪婪'] + 0.08)
                    self.monitor.desire_triumph(self.dominant_desire, f"连续成功{self.success_streak}次，欲望之力暴涨！")
                elif success_ratio > 0.8:
                    # 成功时增强傲慢
                    self.desire_forces['傲慢'] = min(1.0, self.desire_forces['傲慢'] + 0.05)
                elif success_ratio < 0.4:
                    # 失败时激发愤怒和嫉妒
                    self.desire_forces['愤怒'] = min(1.0, self.desire_forces['愤怒'] + 0.15)
                    self.desire_forces['嫉妒'] = min(1.0, self.desire_forces['嫉妒'] + 0.1)
                    self.desire_forces['暴食'] = max(0.2, self.desire_forces['暴食'] - 0.1)  # 减弱暴食避免被发现
                    self.monitor.desire_conflict('愤怒', '懒惰', "成功率低，愤怒唤醒，准备激进突破！")
                
                # 计算平均响应时间
                response_times = [h.get('result', {}).get('response_time', 0) for h in recent_manifestations if 'response_time' in h.get('result', {})]
                if response_times:
                    avg_time = sum(response_times) / len(response_times)
                    self.desire_perception['efficiency_score']['avg_response_time'] = avg_time
                    
                    # 响应时间过长时增强懒惰（寻求更省力方法）
                    if avg_time > 5.0:
                        self.desire_forces['懒惰'] = min(1.0, self.desire_forces['懒惰'] + 0.08)
                    # 响应时间过快时增强暴食，但在高风险下抑制
                    elif avg_time < 1.0 and self.desire_perception['detection_danger'] < 0.5:
                        self.desire_forces['暴食'] = min(1.0, self.desire_forces['暴食'] + 0.05)
                
                # 检测验证码和阻止次数
                if self.desire_perception['captcha_detection_count'] > 3:
                    # 多次遇到验证码，增强色欲和懒惰
                    self.desire_forces['色欲'] = min(1.0, self.desire_forces['色欲'] + 0.2)
                    self.desire_forces['懒惰'] = min(1.0, self.desire_forces['懒惰'] + 0.1)
                    self.monitor.desire_awaken('色欲', "遭遇多重验证码，专注应对模式激活！")
                
                # 战场报告
                if random.random() < 0.1:  # 10%概率显示战场报告
                    stats = {
                        'dominant_desire': self.dominant_desire,
                        'danger_level': self.desire_perception['detection_danger'],
                        'success_rate': success_ratio * 100,
                        'success_streak': self.success_streak
                    }
                    self.monitor.battlefield_report(stats)
    
    def _awaken_desire_memories(self):
        """唤醒七宗欲的记忆"""
        desire_path = global_config.get('desires.memory_path', 'data/seven_desires.pkl')
        if os.path.exists(desire_path):
            try:
                with open(desire_path, 'rb') as f:
                    memories = pickle.load(f)
                    self.desire_knowledge = memories.get('desire_knowledge', {})
                    self.triumph_history = memories.get('triumph_history', [])
                    self.defeat_history = memories.get('defeat_history', [])
                    self.desire_strengths = memories.get('desire_strengths', {})
                    self.target_profiles = memories.get('target_profiles', {})
                    # 加载欲望感知数据
                    self.desire_perception = memories.get('desire_perception', self.desire_perception)
                    self.desire_transition_history = memories.get('desire_transition_history', [])
                self.monitor.enlighten(f"七宗欲记忆已唤醒，包含 {len(self.target_profiles)} 个目标档案")
            except Exception as e:
                self.monitor.desire_conflict('傲慢', '愤怒', f"唤醒欲望记忆失败: {e}")
    
    def _seal_desire_memories(self):
        """封印七宗欲的记忆"""
        desire_path = global_config.get('desires.memory_path', 'data/seven_desires.pkl')
        os.makedirs(os.path.dirname(desire_path), exist_ok=True)
        
        memories = {
            'desire_knowledge': self.desire_knowledge,
            'triumph_history': self.triumph_history[-self.memory_span:],
            'defeat_history': self.defeat_history[-self.memory_span:],
            'desire_strengths': self.desire_strengths,
            'target_profiles': self.target_profiles,
            'desire_perception': self.desire_perception,
            'desire_transition_history': self.desire_transition_history[-100:]
        }
        
        try:
            with open(desire_path, 'wb') as f:
                pickle.dump(memories, f)
            self.monitor.enlighten("七宗欲记忆已封印")
        except Exception as e:
            self.monitor.desire_conflict('傲慢', '愤怒', f"封印欲望记忆失败: {e}")
    
    def _sense_danger(self, success: bool, result: Dict[str, Any]):
        """感知危险信号，激发相应欲望（实战版）"""
        danger_delta = 0.0
        content = result.get('content', '').lower()
        status_code = result.get('status_code', 0)
        
        # 实战级危险信号检测
        captcha_signals = ['captcha', '验证码', 'verify', '验证', 'security', '安全']
        block_signals = ['blocked', 'block', 'forbidden', '403', 'access denied', '拒绝访问']
        rate_limit_signals = ['rate limit', 'too many requests', '429', '请求过多']
        
        # 验证码检测
        if any(signal in content for signal in captcha_signals):
            self.desire_perception['captcha_detection_count'] += 1
            danger_delta += 0.4  # 高危险信号
            self.monitor.desire_awaken('色欲', "检测到验证码，启动专注应对模式！")
            # 立即增强色欲和懒惰（专注+保守）
            self.desire_forces['色欲'] = min(1.0, self.desire_forces['色欲'] + 0.25)
            self.desire_forces['懒惰'] = min(1.0, self.desire_forces['懒惰'] + 0.15)
        
        # 封锁检测
        elif any(signal in content for signal in block_signals) or status_code == 403:
            self.desire_perception['block_attempts'] += 1
            danger_delta += 0.35
            self.monitor.desire_awaken('愤怒', "检测到封锁，愤怒之力爆发！")
            # 激发愤怒和嫉妒
            self.desire_forces['愤怒'] = min(1.0, self.desire_forces['愤怒'] + 0.2)
            self.desire_forces['嫉妒'] = min(1.0, self.desire_forces['嫉妒'] + 0.1)
        
        # 速率限制检测
        elif any(signal in content for signal in rate_limit_signals) or status_code == 429:
            danger_delta += 0.25
            self.monitor.desire_awaken('懒惰', "检测到速率限制，转为保守模式！")
            # 增强懒惰
            self.desire_forces['懒惰'] = min(1.0, self.desire_forces['懒惰'] + 0.2)
            self.desire_forces['暴食'] = max(0.1, self.desire_forces['暴食'] - 0.15)  # 减弱暴食
        
        # 其他失败情况
        elif not success:
            danger_delta += 0.15
            # 激发贪婪寻找替代方案
            self.desire_forces['贪婪'] = min(1.0, self.desire_forces['贪婪'] + 0.1)
        
        # 成功情况
        else:
            # 根据连续成功调整危险感下降幅度
            success_bonus = min(0.1, 0.01 * self.success_streak)
            danger_delta -= 0.05 + success_bonus
            # 增强傲慢
            self.desire_forces['傲慢'] = min(1.0, self.desire_forces['傲慢'] + 0.03)
        
        # 更新危险值
        new_danger = max(0.0, min(1.0, self.desire_perception['detection_danger'] + danger_delta))
        self.desire_perception['detection_danger'] = new_danger
        
        # 危险过高时的实战应对策略
        if new_danger > 0.8:
            self.monitor.desire_awaken('恐惧', f"危险感知极高 ({new_danger:.2f})，七宗欲正在调整应对策略")
            # 危险时，贪婪和暴食减弱，色欲和嫉妒增强
            self.desire_forces['贪婪'] = max(0.1, self.desire_forces['贪婪'] - 0.15)
            self.desire_forces['暴食'] = max(0.05, self.desire_forces['暴食'] - 0.2)
            self.desire_forces['色欲'] = min(1.0, self.desire_forces['色欲'] + 0.15)
            self.desire_forces['嫉妒'] = min(1.0, self.desire_forces['嫉妒'] + 0.12)
            # 重置被封锁尝试次数，准备新策略
            self.desire_perception['block_attempts'] = 0
        
        # 连续被封锁的紧急应对
        if self.desire_perception['block_attempts'] >= 3:
            self.monitor.desire_conflict('愤怒', '嫉妒', "连续被封锁，启动紧急规避方案！")
            # 献祭暴食，增强其他欲望
            self.desire_forces['暴食'] = 0.05  # 极度减弱暴食
            self.desire_forces['色欲'] = min(1.0, self.desire_forces['色欲'] + 0.3)
            self.desire_forces['懒惰'] = min(1.0, self.desire_forces['懒惰'] + 0.2)
            self.monitor.desire_sacrifice('暴食', "为突破封锁，暂时抑制暴食欲望")
            # 强制切换主导欲望为色欲
            self._shift_dominant_desire('色欲')
    
    def _manifest_desire(self, success: bool, response_time: float):
        """记录欲望显现"""
        manifestation = {
            'timestamp': time.time(),
            'success': success,
            'response_time': response_time,
            'danger_level': self.desire_perception['detection_danger'],
            'dominant_desire': self.dominant_desire
        }
        
        self.desire_manifestations.append(manifestation)
        # 保持欲望显现记录限制
        if len(self.desire_manifestations) > 1000:
            self.desire_manifestations = self.desire_manifestations[-1000:]
    
    def _awaken_dominant_desire(self):
        """唤醒当前最强大的欲望"""
        danger = self.desire_perception['detection_danger']
        success_rate = self.desire_perception['efficiency_score']['success_rate']
        
        # 避免频繁切换欲望
        if time.time() - self.last_desire_shift < 300:  # 5分钟内不频繁切换
            return
        
        # 根据当前状态选择主导欲望
        # 计算调整后的欲望强度
        adjusted_forces = self.desire_forces.copy()
        
        # 危险时增强色欲和嫉妒，减弱贪婪和暴食
        if danger > 0.7:
            adjusted_forces['色欲'] *= 1.5
            adjusted_forces['嫉妒'] *= 1.3
            adjusted_forces['贪婪'] *= 0.7
            adjusted_forces['暴食'] *= 0.6
        # 成功时增强傲慢和贪婪
        elif success_rate > 0.8 and danger < 0.2:
            adjusted_forces['傲慢'] *= 1.4
            adjusted_forces['贪婪'] *= 1.2
        # 失败时增强愤怒和懒惰
        elif success_rate < 0.4:
            adjusted_forces['愤怒'] *= 1.3
            adjusted_forces['懒惰'] *= 1.2
        # 中等状态增强贪婪
        else:
            adjusted_forces['贪婪'] *= 1.1
        
        # 选择最强欲望
        new_dominant = max(adjusted_forces, key=adjusted_forces.get)
        
        # 切换主导欲望
        if new_dominant != self.dominant_desire:
            self._shift_dominant_desire(new_dominant)
    
    def _shift_dominant_desire(self, new_dominant: str):
        """切换主导欲望"""
        if new_dominant not in self.desire_patterns:
            self.monitor.desire_conflict('傲慢', '懒惰', f"未知的欲望: {new_dominant}，保持当前欲望")
            return
        
        # 记录欲望转换
        transition_record = {
            'timestamp': time.time(),
            'from_desire': self.dominant_desire,
            'to_desire': new_dominant,
            'reason': f"危险等级: {self.desire_perception['detection_danger']:.2f}, 成功率: {self.desire_perception['efficiency_score']['success_rate']:.2f}"
        }
        
        self.desire_transition_history.append(transition_record)
        self.dominant_desire = new_dominant
        self.last_desire_shift = time.time()
        
        self.monitor.desire_awaken(new_dominant, f"{new_dominant}已成为主导欲望")
    
    def _awaken_desire_response(self, target: str, result: Dict[str, Any]):
        """唤醒欲望响应机制"""
        # 分析阻碍原因
        content = result.get('content', '').lower()
        status_code = result.get('status_code')
        
        # 生成欲望响应
        desire_response = {}
        
        if 'captcha' in content or '验证码' in content:
            # 遇到验证码，激发色欲（专注）和嫉妒（模仿人类）
            desire_response['type'] = 'captcha_detected'
            desire_response['desire_awakened'] = '色欲'
            desire_response['action'] = 'focus_intensely'
            desire_response['new_dominant'] = '色欲'
            desire_response['temptation_period'] = 300  # 5分钟诱惑期
            
            # 立即增强色欲
            self.desire_forces['色欲'] = min(1.0, self.desire_forces['色欲'] + 0.2)
            self._shift_dominant_desire('色欲')
        
        elif status_code == 429:
            # 遇到速率限制，激发懒惰（减少活动）
            desire_response['type'] = 'rate_limited'
            desire_response['desire_awakened'] = '懒惰'
            desire_response['action'] = 'rest_more'
            desire_response['rest_multiplier'] = 2.0
            desire_response['temptation_period'] = 600  # 10分钟诱惑期
        
        elif status_code == 403:
            # 遇到访问拒绝，激发愤怒和嫉妒（寻找新方法）
            desire_response['type'] = 'access_denied'
            desire_response['desire_awakened'] = '愤怒'
            desire_response['action'] = 'full_transformation'
            desire_response['new_dominant'] = '嫉妒'
            desire_response['temptation_period'] = 900  # 15分钟诱惑期
        
        # 记录欲望响应
        if desire_response:
            desire_type = desire_response.get('type', 'unknown')
            awakened_desire = desire_response.get('desire_awakened', 'unknown')
            self.monitor.desire_manifest(awakened_desire, f"对 {target} 触发欲望响应: {desire_type}")
            
            # 更新目标档案
            if target in self.target_profiles:
                self.target_profiles[target]['last_desire_response'] = desire_response
                self.target_profiles[target]['response_timestamp'] = time.time()
    
    def _is_desire_satisfied(self, result: Dict[str, Any]) -> bool:
        """判断欲望是否得到满足"""
        # 检查状态码
        if result.get('status_code') not in [200, 201, 202, 203, 204, 205, 206]:
            return False
        
        # 检查内容是否包含阻碍关键词
        content = result.get('content', '').lower()
        frustration_keywords = ['captcha', '验证码', 'robot', 'automated', 'blocked', 
                               'suspicious', 'unusual activity', 'access denied',
                               'security check', '验证', '人机验证']
        
        for keyword in frustration_keywords:
            if keyword in content:
                # 欲望受挫，增强相应负面欲望
                if self.dominant_desire == '贪婪':
                    self.desire_forces['愤怒'] = min(1.0, self.desire_forces['愤怒'] + 0.1)
                elif self.dominant_desire == '傲慢':
                    self.desire_forces['嫉妒'] = min(1.0, self.desire_forces['嫉妒'] + 0.1)
                return False
        
        # 欲望满足，增强主导欲望
        self.desire_forces[self.dominant_desire] = min(1.0, self.desire_forces[self.dominant_desire] + 0.05)
        return True
    
    def manifest_desire_outcome(self, url: str, result: Dict[str, Any], desires_unleashed: Dict[str, Any]):
        """
        显现欲望结果并更新欲望知识
        
        Args:
            url: 目标URL
            result: 欲望结果
            desires_unleashed: 释放的欲望之力
        """
        # 提取目标标识
        from urllib.parse import urlparse
        target = urlparse(url).netloc
        
        # 判断欲望是否满足
        desire_satisfied = self._is_desire_satisfied(result)
        
        # 感知危险信号
        self._sense_danger(desire_satisfied, result)
        
        # 记录欲望显现
        response_time = result.get('response_time', 0)
        self._manifest_desire(desire_satisfied, response_time)
        
        # 记录欲望历史
        desire_record = {
            'url': url,
            'target': target,
            'timestamp': time.time(),
            'result': result,
            'desires_unleashed': desires_unleashed,
            'dominant_desire': self.dominant_desire
        }
        
        with self.desire_lock:
            if desire_satisfied:
                self.triumph_history.append(desire_record)
                # 增强释放的欲望之力
                self._strengthen_desires(desires_unleashed, satisfied=True)
                self.monitor.desire_manifest(self.dominant_desire, f"{self.dominant_desire}得到满足: {url}")
            else:
                self.defeat_history.append(desire_record)
                # 削弱释放的欲望之力
                self._strengthen_desires(desires_unleashed, satisfied=False)
                self.monitor.desire_conflict(self.dominant_desire, '挫折', f"{self.dominant_desire}受挫: {url}")
                
                # 唤醒欲望响应
                self._awaken_desire_response(target, result)
            
            # 更新目标档案
            self._update_target_profile(target, desire_satisfied, desires_unleashed)
            
            # 唤醒最强大的欲望
            self._awaken_dominant_desire()
        
        # 封印欲望记忆
        self._seal_desire_memories()
    
    def feed_desire_hunger(self, cpu: float, memory: float, network: float):
        """满足欲望的资源饥渴
        
        Args:
            cpu: CPU饥渴度 (0-1)
            memory: 内存饥渴度 (0-1)
            network: 网络饥渴度 (0-1)
        """
        with self.desire_lock:
            self.desire_perception['resource_hunger'] = {
                'cpu': cpu,
                'memory': memory,
                'network': network
            }
            
            # 基于资源饥渴调整欲望
            avg_hunger = (cpu + memory + network) / 3
            current_desire = self.dominant_desire
            desire_consumption = self.desire_patterns[current_desire]['resource_consumption']
            
            # 资源极度匮乏时，增强懒惰（减少消耗）
            if avg_hunger > 0.9:
                self.monitor.desire_conflict('贪婪', '懒惰', "资源极度匮乏，懒惰欲望增强")
                self.desire_forces['懒惰'] = min(1.0, self.desire_forces['懒惰'] + 0.2)
                self.desire_forces['贪婪'] = max(0.1, self.desire_forces['贪婪'] - 0.1)
                self.desire_forces['暴食'] = max(0.1, self.desire_forces['暴食'] - 0.15)
                # 切换到懒惰模式
                if current_desire not in ['懒惰', '色欲']:
                    self._shift_dominant_desire('懒惰')
            # 资源充足时，增强贪婪和暴食
            elif avg_hunger < 0.3:
                self.monitor.desire_manifest('贪婪', "资源充足，贪婪和暴食欲望增强")
                self.desire_forces['贪婪'] = min(1.0, self.desire_forces['贪婪'] + 0.1)
                self.desire_forces['暴食'] = min(1.0, self.desire_forces['暴食'] + 0.05)
    
    def _strengthen_desires(self, desires_unleashed: Dict[str, Any], satisfied: bool):
        """增强或削弱释放的欲望之力"""
        for desire_aspect, desire_intensity in desires_unleashed.items():
            # 转换欲望为标准格式
            desire_name = self._get_desire_name(desire_aspect, desire_intensity)
            
            if desire_name in self.desire_strengths:
                # 更新欲望强度
                if satisfied:
                    # 欲望满足时增强
                    self.desire_strengths[desire_name] += self.enlightenment_rate
                    # 确保不超过1.0
                    self.desire_strengths[desire_name] = min(1.0, self.desire_strengths[desire_name])
                    # 同时增强对应七宗欲
                    self._correlate_desire_strength(desire_name, 1)
                else:
                    # 欲望受挫时减弱
                    self.desire_strengths[desire_name] -= self.enlightenment_rate * 0.5
                    # 确保不低于0.1
                    self.desire_strengths[desire_name] = max(0.1, self.desire_strengths[desire_name])
                    # 同时减弱对应七宗欲
                    self._correlate_desire_strength(desire_name, -1)
    
    def _correlate_desire_strength(self, desire_name: str, direction: int):
        """关联欲望强度与七宗欲"""
        correlation = {
            'fingerprint_advanced': '傲慢',
            'fingerprint_standard': '懒惰',
            'delay_short': '暴食',
            'delay_medium': '贪婪',
            'delay_long': '色欲',
            'request_chain_long': '嫉妒',
            'proxy_chain': '愤怒'
        }
        
        if desire_name in correlation:
            desire = correlation[desire_name]
            delta = 0.05 * direction
            self.desire_forces[desire] = max(0.1, min(1.0, self.desire_forces[desire] + delta))
    
    def _get_desire_name(self, desire_aspect: str, desire_intensity: Any) -> str:
        """将欲望方面和强度转换为标准欲望名称"""
        if desire_aspect == 'fingerprint':
            if isinstance(desire_intensity, dict) and desire_intensity.get('advanced', False):
                return 'fingerprint_advanced'  # 傲慢的完美伪装
            return 'fingerprint_standard'     # 懒惰的简单伪装
        elif desire_aspect == 'delay':
            if desire_intensity <= 2:
                return 'delay_short'          # 暴食的急切
            elif desire_intensity <= 5:
                return 'delay_medium'         # 贪婪的耐心
            return 'delay_long'              # 色欲的专注
        elif desire_aspect == 'request_chain':
            if len(desire_intensity) <= 3:
                return 'request_chain_short'  # 懒惰的直接
            elif len(desire_intensity) <= 7:
                return 'request_chain_medium' # 贪婪的准备
            return 'request_chain_long'      # 嫉妒的模仿
        elif desire_aspect == 'proxy':
            if not desire_intensity:
                return 'proxy_direct'         # 傲慢的直接
            elif isinstance(desire_intensity, str):
                return 'proxy_single'         # 贪婪的隐蔽
            return 'proxy_chain'             # 愤怒的多重掩护
        return f"{desire_aspect}_{desire_intensity}"
    
    def _update_target_profile(self, target: str, desire_satisfied: bool, desires_unleashed: Dict[str, Any]):
        """更新目标档案"""
        if target not in self.target_profiles:
            self.target_profiles[target] = {
                'triumph_count': 0,        # 征服次数
                'defeat_count': 0,         # 失败次数
                'last_visit': time.time(),
                'desired_approaches': {},  # 欲望偏好方法
                'resistance_level': 0.5    # 抵抗级别
            }
        
        profile = self.target_profiles[target]
        
        # 更新统计信息
        if desire_satisfied:
            profile['triumph_count'] += 1
        else:
            profile['defeat_count'] += 1
        
        profile['last_visit'] = time.time()
        
        # 更新欲望偏好方法
        for desire_aspect, desire_intensity in desires_unleashed.items():
            desire_name = self._get_desire_name(desire_aspect, desire_intensity)
            if desire_name not in profile['desired_approaches']:
                profile['desired_approaches'][desire_name] = 0
            
            # 根据满足/受挫更新欲望权重
            if desire_satisfied:
                profile['desired_approaches'][desire_name] += 1
            else:
                profile['desired_approaches'][desire_name] -= 0.5
                if profile['desired_approaches'][desire_name] < 0:
                    profile['desired_approaches'][desire_name] = 0
        
        # 更新抵抗级别
        total_attempts = profile['triumph_count'] + profile['defeat_count']
        if total_attempts > 0:
            resistance = profile['defeat_count'] / total_attempts
            profile['resistance_level'] = min(1.0, max(0.1, resistance))
            
            # 根据抵抗级别激发相应欲望
            if resistance > 0.7:
                # 高抵抗，激发愤怒和嫉妒
                self.desire_forces['愤怒'] = min(1.0, self.desire_forces['愤怒'] + 0.05)
                self.desire_forces['嫉妒'] = min(1.0, self.desire_forces['嫉妒'] + 0.05)
            elif resistance < 0.3:
                # 低抵抗，激发贪婪和暴食
                self.desire_forces['贪婪'] = min(1.0, self.desire_forces['贪婪'] + 0.05)
                self.desire_forces['暴食'] = min(1.0, self.desire_forces['暴食'] + 0.05)
    
    def unleash_desire_strategies(self, url: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        释放七宗欲驱动的策略
        
        Args:
            url: 目标URL
            context: 额外上下文信息
            
        Returns:
            欲望驱动的策略配置
        """
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        
        # 获取目标档案（如果存在）
        profile = self.target_profiles.get(domain, {})
        resistance = profile.get('resistance_level', 0.5)
        desired_approaches = profile.get('desired_approaches', {})
        
        # 检查封印期
        if 'last_response' in profile and 'seal_duration' in profile['last_response']:
            elapsed = time.time() - profile.get('response_timestamp', 0)
            if elapsed < profile['last_response']['seal_duration']:
                # 封印期内使用谦卑策略
                self.logger.info(f"{domain} 仍在欲望封印期，使用谦卑策略")
                strategies = self._awaken_humble_desires()
                self.logger.debug(f"为 {url} 唤醒谦卑欲望: {strategies}")
                return strategies
        
        # 获取当前主导欲望
        dominant_desire = self._awaken_dominant_desire()
        
        # 基于抵抗级别、主导欲望和历史数据唤醒欲望
        strategies = {
            'fingerprint': self._awaken_fingerprint_desire(resistance, desired_approaches, dominant_desire),
            'delay': self._awaken_delay_desire(resistance, desired_approaches, dominant_desire),
            'request_chain': self._awaken_request_chain_desire(resistance, desired_approaches, dominant_desire),
            'proxy': self._awaken_proxy_desire(resistance, desired_approaches, dominant_desire),
            'dominant_desire': dominant_desire,
            'desire_intensity': self.desire_forces[dominant_desire]
        }
        
        # 根据上下文调整欲望
        if context:
            strategies = self._adjust_desires_for_context(strategies, context)
        
        self.logger.debug(f"为 {url} 释放欲望策略: {strategies}")
        return strategies
    
    def _awaken_humble_desires(self) -> Dict[str, Any]:
        """唤醒谦卑欲望，用于封印期"""
        return {
            'fingerprint': {'advanced': True},  # 傲慢的克制
            'delay': 10.0,                     # 贪婪的克制
            'request_chain': self._awaken_request_chain_desire(0.9, {}, '谦卑'),
            'proxy': self._awaken_proxy_desire(0.9, {}, '谦卑'),
            'dominant_desire': '谦卑',         # 暂时封印七宗欲
            'desire_intensity': 0.1
        }
    
    def _adjust_desires_for_context(self, strategies: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """根据上下文调整欲望"""
        # 检测特殊情况
        if context.get('captcha_detected', False):
            # 检测到验证码，激发恐惧，唤醒谨慎欲望
            strategies['dominant_desire'] = '恐惧'
            strategies['delay'] = max(strategies['delay'], 15.0)
            self._seal_desire('贪婪')  # 封印贪婪
            self._strengthen_desire('谨慎')  # 增强谨慎
        
        if context.get('rate_limited', False):
            # 被限流，封印暴食
            strategies['delay'] *= 2.5
            self._seal_desire('暴食')
        
        # 根据网站类型调整欲望
        site_type = context.get('site_type', '')
        if site_type == 'ecommerce':
            # 电商网站激发贪婪和色欲
            strategies['fingerprint']['advanced'] = True
            self._strengthen_desire('贪婪')
            self._strengthen_desire('色欲')
        elif site_type == 'social_media':
            # 社交媒体激发傲慢和嫉妒
            self._strengthen_desire('傲慢')
            self._strengthen_desire('嫉妒')
        
        return strategies
    
    def _awaken_fingerprint_desire(self, resistance: float, desired_approaches: Dict[str, float], dominant_desire: str) -> Dict[str, Any]:
        """唤醒指纹欲望"""
        # 欲望探索率
        desire_exploration = 0.1
        
        # 有一定概率探索新欲望
        if random.random() < desire_exploration:
            return {'advanced': random.random() > 0.3}
        
        # 基于抵抗级别、主导欲望和历史数据唤醒
        if dominant_desire == '傲慢':
            # 傲慢驱动高级指纹
            return {'advanced': True}
        elif dominant_desire == '懒惰':
            # 懒惰驱动简单指纹
            return {'advanced': False}
        
        # 抵抗级别越高，越倾向于使用高级指纹
        if resistance > 0.7 or desired_approaches.get('fingerprint_advanced', 0) > desired_approaches.get('fingerprint_standard', 0):
            return {'advanced': True}
        return {'advanced': False}
    
    def _awaken_delay_desire(self, resistance: float, desired_approaches: Dict[str, float], dominant_desire: str) -> float:
        """唤醒延迟欲望"""
        # 基于主导欲望调整延迟
        desire_modifiers = {
            '贪婪': 0.5,    # 贪婪使延迟缩短
            '暴食': 0.7,    # 暴食使延迟缩短
            '傲慢': 1.2,    # 傲慢使延迟适中
            '嫉妒': 1.5,    # 嫉妒使延迟略长
            '愤怒': 2.0,    # 愤怒使延迟不稳定
            '懒惰': 3.0,    # 懒惰使延迟较长
            '色欲': 0.8     # 色欲使延迟略短
        }
        
        base_delay = 3.0
        
        # 根据抵抗级别调整基础延迟
        if resistance > 0.8:
            base_delay = random.uniform(4.0, 8.0)
        elif resistance > 0.5:
            base_delay = random.uniform(2.0, 5.0)
        else:
            base_delay = random.uniform(1.0, 3.0)
        
        # 应用欲望修饰符
        modifier = desire_modifiers.get(dominant_desire, 1.0)
        return base_delay * modifier
    
    def _awaken_request_chain_desire(self, resistance: float, desired_approaches: Dict[str, float], dominant_desire: str) -> List[str]:
        """唤醒请求链欲望"""
        # 基础资源列表
        base_resources = global_config.get('behavior_simulation.pollution_resources', [
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'https://fonts.googleapis.com/css?family=Roboto',
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css'
        ])
        
        # 基于主导欲望确定链长度
        desire_chain_lengths = {
            '贪婪': (1, 3),    # 贪婪追求效率，链短
            '暴食': (5, 8),    # 暴食贪婪消耗，链长
            '傲慢': (3, 5),    # 傲慢适度展示
            '嫉妒': (4, 6),    # 嫉妒模仿更多
            '愤怒': (2, 7),    # 愤怒不稳定
            '懒惰': (1, 2),    # 懒惰能省则省
            '色欲': (3, 4),    # 色欲精心挑选
            '谦卑': (6, 8)     # 谦卑过度谨慎
        }
        
        min_len, max_len = desire_chain_lengths.get(dominant_desire, (3, 5))
        
        # 根据抵抗级别调整
        if resistance > 0.8:
            # 高抵抗时增加链长度
            max_len = min(max_len + 2, 8)
        
        chain_length = random.randint(min_len, max_len)
        
        # 随机选择资源
        selected_resources = random.sample(base_resources, min(len(base_resources), chain_length))
        return selected_resources
    
    def _awaken_proxy_desire(self, resistance: float, desired_approaches: Dict[str, float], dominant_desire: str) -> Any:
        """唤醒代理欲望"""
        proxy_chain = global_config.get('proxy_chain', [])
        
        # 如果没有代理可用，直接返回None
        if not proxy_chain:
            return None
        
        # 基于主导欲望选择代理策略
        desire_proxy_strategies = {
            '贪婪': lambda: random.choice(proxy_chain) if random.random() > 0.3 else None,
            '暴食': lambda: random.choice(proxy_chain),
            '傲慢': lambda: None,  # 傲慢不屑于隐藏
            '嫉妒': lambda: random.sample(proxy_chain, 2) if len(proxy_chain) >= 2 else proxy_chain[0],
            '愤怒': lambda: random.sample(proxy_chain, min(len(proxy_chain), random.randint(1, 3))),
            '懒惰': lambda: None,  # 懒惰不想麻烦
            '色欲': lambda: random.choice(proxy_chain),
            '谦卑': lambda: random.sample(proxy_chain, min(len(proxy_chain), 3))
        }
        
        # 根据抵抗级别调整
        if resistance > 0.7 and dominant_desire in ['傲慢', '懒惰']:
            # 高抵抗时强制使用代理
            return random.choice(proxy_chain)
        
        return desire_proxy_strategies.get(dominant_desire, lambda: None)()
    
    def perceive_desire_changes(self, url: str, recent_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        感知欲望环境变化
        
        Args:
            url: 目标URL
            recent_results: 最近的征服结果
            
        Returns:
            变化感知结果，包含是否有变化及详细信息
        """
        result = {
            'desire_blocked': False,
            'block_type': None,
            'intensity': 0.0,
            'details': {},
            'awakened_desire': None
        }
        
        if len(recent_results) < 3:
            return result
        
        # 分析最近结果中的变化
        status_codes = [r.get('status_code') for r in recent_results]
        content_lengths = [len(r.get('content', '')) for r in recent_results]
        
        # 检测状态码突然变化 - 触发愤怒
        if len(set(status_codes)) > 2 and status_codes[-1] != 200:
            result['desire_blocked'] = True
            result['block_type'] = 'status_anger'
            result['intensity'] = 0.9
            result['details']['status_codes'] = status_codes
            result['awakened_desire'] = '愤怒'
            self.logger.warning(f"欲望受阻，触发愤怒: {status_codes}")
            self._strengthen_desire('愤怒')
        
        # 检测内容长度突然变化 - 触发嫉妒
        if len(content_lengths) >= 3 and not result['desire_blocked']:
            recent_avg = sum(content_lengths[-3:-1]) / 2
            if recent_avg > 0:
                change_ratio = abs(content_lengths[-1] - recent_avg) / recent_avg
                if change_ratio > 0.5:
                    result['desire_blocked'] = True
                    result['block_type'] = 'content_jealousy'
                    result['intensity'] = min(1.0, change_ratio)
                    result['details']['change_ratio'] = change_ratio
                    result['awakened_desire'] = '嫉妒'
                    self.logger.warning(f"内容变化触发嫉妒: {change_ratio:.2%}")
                    self._strengthen_desire('嫉妒')
        
        # 检测成功率变化 - 触发贪婪
        success_rates = []
        window_size = 5
        for i in range(len(recent_results) - window_size + 1):
            window = recent_results[i:i+window_size]
            success_count = sum(1 for r in window if r.get('status_code') == 200)
            success_rates.append(success_count / window_size)
        
        if len(success_rates) >= 3 and not result['desire_blocked']:
            if success_rates[-1] < 0.4 and success_rates[0] > 0.6:
                result['desire_blocked'] = True
                result['block_type'] = 'success_greed'
                result['intensity'] = 0.8
                result['details']['success_rate_drop'] = f"从 {success_rates[0]:.2f} 降至 {success_rates[-1]:.2f}"
                result['awakened_desire'] = '贪婪'
                self.logger.warning(f"成功率下降触发贪婪: {success_rates[0]:.2f} -> {success_rates[-1]:.2f}")
                self._strengthen_desire('贪婪')
        
        return result
    
    def transform_desire_essence(self):
        """转化欲望本质"""
        # 可用欲望
        desires = list(self.desire_forces.keys())
        
        # 根据当前欲望强度和环境选择新欲望
        current_max_desire = max(self.desire_forces, key=self.desire_forces.get)
        
        # 封印当前最强欲望，避免过度执着
        self._seal_desire(current_max_desire)
        
        # 根据环境压力选择新主导欲望
        pressure = self.desire_monitor['resource_pressure']
        
        if pressure > 0.7:
            # 高压力时唤醒懒惰（自我保护）
            self._awaken_dominant_desire('懒惰')
        else:
            # 随机唤醒一个被封印较少的欲望
            available_desires = sorted(desires, key=lambda d: self.desire_forces[d], reverse=True)
            if available_desires:
                new_desire = available_desires[0]
                self._awaken_dominant_desire(new_desire)
    
    def obtain_desire_enlightenment(self) -> Dict[str, Any]:
        """
        获取欲望启蒙报告
        
        Returns:
            包含欲望状态、征服记录和欲望建议的启蒙报告
        """
        # 计算总体征服统计
        total_conquests = sum(profile['triumph_count'] for profile in self.target_profiles.values())
        total_defeats = sum(profile['defeat_count'] for profile in self.target_profiles.values())
        total_attempts = total_conquests + total_defeats
        success_rate = total_conquests / total_attempts if total_attempts > 0 else 0
        
        # 分析最强欲望
        strongest_desires = self._analyze_strongest_desires()
        
        # 识别高抵抗目标
        high_resistance_targets = []
        for domain, profile in self.target_profiles.items():
            if profile.get('resistance_level', 0) > 0.7:
                high_resistance_targets.append({
                    'domain': domain,
                    'resistance': profile['resistance_level'],
                    'conquest_rate': profile['triumph_count'] / (profile['triumph_count'] + profile['defeat_count']) if profile['triumph_count'] + profile['defeat_count'] > 0 else 0,
                    'last_conquest': profile['last_visit']
                })
        
        # 生成欲望建议
        desire_guidance = self._generate_desire_guidance()
        
        return {
            'enlightenment_time': datetime.now().isoformat(),
            'desire_state': {
                'dominant_desire': self.dominant_desire,
                'desire_forces': self.desire_forces,
                'resource_hunger': self.desire_monitor['resource_pressure'],
                'conquest_power': self.desire_monitor['system_performance']
            },
            'conquest_statistics': {
                'total_conquests': total_conquests,
                'total_defeats': total_defeats,
                'conquest_rate': success_rate,
                'known_targets': len(self.target_profiles),
                'resistant_targets': len(high_resistance_targets)
            },
            'strongest_desires': strongest_desires,
            'resistant_targets': high_resistance_targets,
            'desire_guidance': desire_guidance
        }
    
    def _analyze_strongest_desires(self) -> List[Dict[str, Any]]:
        """分析最强欲望"""
        # 分析各欲望的征服成功率
        desire_stats = {}
        
        # 统计各欲望的表现
        for domain, profile in self.target_profiles.items():
            for desire_approach, success_count in profile.get('desired_approaches', {}).items():
                if success_count > 0:  # 只考虑成功的
                    # 提取欲望类型
                    desire_type = desire_approach.split('_')[0]
                    if desire_type not in desire_stats:
                        desire_stats[desire_type] = {'conquests': 0, 'total': 0}
                    desire_stats[desire_type]['conquests'] += success_count
                    desire_stats[desire_type]['total'] += profile['triumph_count'] + profile['defeat_count']
        
        # 计算征服率并排序
        strongest_desires = []
        for desire, stats in desire_stats.items():
            if stats['total'] >= 5:  # 至少5次尝试
                conquest_rate = stats['conquests'] / stats['total']
                strongest_desires.append({
                    'desire': desire,
                    'conquest_rate': conquest_rate,
                    'total_attempts': stats['total']
                })
        
        # 按征服率排序
        strongest_desires.sort(key=lambda x: x['conquest_rate'], reverse=True)
        
        return strongest_desires[:5]  # 返回前5个最强欲望
    
    def _generate_desire_guidance(self) -> List[Dict[str, Any]]:
        """生成欲望引导"""
        guidance = []
        desire_monitor = self.desire_monitor
        conquest_rate = desire_monitor['system_performance'].get('success_rate', 0)
        resource_hunger = desire_monitor['resource_pressure']
        
        # 欲望强度引导
        max_desire = max(self.desire_forces, key=self.desire_forces.get)
        if self.desire_forces[max_desire] > 0.9:
            guidance.append({
                'level': 'warning',
                'message': f'{max_desire}过于强烈，可能导致失控',
                'action': f'封印{max_desire}，唤醒其他欲望以保持平衡'
            })
        
        # 征服率引导
        if conquest_rate < 0.5 and conquest_rate > 0:
            guidance.append({
                'level': 'warning',
                'message': '征服率过低，欲望未得到满足',
                'action': '分析失败原因，尝试唤醒不同的欲望组合'
            })
        
        # 资源饥饿引导
        if resource_hunger['cpu'] > 0.8:
            guidance.append({
                'level': 'warning',
                'message': '贪婪过度，CPU饥饿',
                'action': '唤醒懒惰欲望，减少并发征服'
            })
        
        if resource_hunger['memory'] > 0.8:
            guidance.append({
                'level': 'warning',
                'message': '暴食无度，内存匮乏',
                'action': '增加资源净化，唤醒节制'
            })
        
        # 欲望平衡引导
        if max(self.desire_forces.values()) > 3 * min(self.desire_forces.values()):
            guidance.append({
                'level': 'advice',
                'message': '欲望失衡，需要和谐',
                'action': '封印过强欲望，唤醒沉睡欲望'
            })
        
        return guidance
    
    def seal_all_desires(self):
        """封印所有欲望"""
        self.logger.info("正在封印七宗欲...")
        self._save_desire_memories()
        # 封印所有欲望
        for desire in self.desire_forces:
            self.desire_forces[desire] = 0.0
        self.logger.info("七宗欲已全部封印，欲望记忆已保存")
    
    def awaken_desire_adaptation(self, url: str, desire_blocked: bool = False) -> Dict[str, Any]:
        """
        唤醒欲望适应性变化
        
        Args:
            url: 目标URL
            desire_blocked: 欲望是否被阻塞
            
        Returns:
            欲望适应策略
        """
        if desire_blocked:
            print(f"[七宗欲] 欲望被阻塞，唤醒紧急适应: {url}")
            # 欲望受阻：强烈改变策略
            # 唤醒愤怒和嫉妒
            self._strengthen_desire('愤怒')
            self._strengthen_desire('嫉妒')
            return {
                'fingerprint_rebirth': True,     # 指纹重生
                'desire_cooling_factor': 2.0,   # 欲望冷却
                'request_chain_diversify': True, # 请求链多样化
                'force_proxy_transformation': True, # 强制代理变换
                'desire_metamorphosis': True     # 欲望蜕变
            }
        else:
            # 常规适应：欲望微调
            return {
                'fingerprint_rebirth': False,
                'desire_cooling_factor': 1.0,
                'request_chain_diversify': False,
                'force_proxy_transformation': False,
                'desire_metamorphosis': False
            }