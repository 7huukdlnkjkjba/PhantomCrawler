#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PhantomCrawler - 元认知系统使用示例

这个示例展示了如何使用增强的元认知系统进行智能爬取，
包括环境感知、行为模式自适应和策略优化。
"""

import time
import random
from src.modules.behavior.behavior_simulator import BehaviorSimulator
from src.modules.intelligence.metacognition_engine import MetacognitionEngine


def run_metacognition_example():
    """
    运行元认知系统示例
    """
    print("=== PhantomCrawler 元认知系统示例 ===")
    print("初始化元认知引擎和行为模拟器...")
    
    # 初始化组件
    behavior_simulator = BehaviorSimulator()
    metacognition_engine = behavior_simulator.metacognition  # 使用同一个元认知引擎实例
    
    # 模拟几个不同的爬取场景
    test_urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3",
        "https://example.com/page4",
        "https://example.com/page5"
    ]
    
    print("开始模拟爬取场景...")
    print("=" * 60)
    
    # 模拟正常爬取场景
    print("场景1: 正常爬取场景")
    simulate_crawl_session(behavior_simulator, test_urls[:3], success_rate=0.9)
    
    # 打印初始元认知洞察
    print("\n初始元认知洞察:")
    print_metacognitive_insights(behavior_simulator)
    print("=" * 60)
    
    # 模拟高风险检测场景
    print("场景2: 高风险检测场景")
    # 注入一些失败和检测信号
    simulate_high_risk_scenario(behavior_simulator, test_urls[3:])
    
    # 打印高风险后的元认知洞察
    print("\n高风险后的元认知洞察:")
    print_metacognitive_insights(behavior_simulator)
    print("=" * 60)
    
    # 模拟恢复场景
    print("场景3: 策略调整和恢复")
    # 强制切换到更安全的行为模式
    behavior_simulator.shift_behavior_pattern()
    
    # 以新策略继续爬取
    simulate_crawl_session(behavior_simulator, test_urls[:2], success_rate=1.0)
    
    # 打印最终元认知洞察
    print("\n最终元认知洞察:")
    print_metacognitive_insights(behavior_simulator)
    
    # 展示模式变化历史
    print("\n行为模式变化历史:")
    for transition in metacognition_engine.behavior_transition_history:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(transition['timestamp']))
        print(f"[{timestamp}] 从 {transition['from']} 切换到 {transition['to']}，原因: {transition['reason']}")
    
    # 展示推荐策略
    print("\n推荐策略:")
    insights = behavior_simulator.get_behavior_statistics()
    for rec in insights.get('recommendations', []):
        print(f"- [{rec['level'].upper()}] {rec['message']} (行动: {rec['action']})")
    
    # 清理资源
    print("\n清理资源...")
    behavior_simulator.shutdown()
    print("示例完成！")


def simulate_crawl_session(simulator, urls, success_rate=0.8):
    """
    模拟爬取会话
    
    Args:
        simulator: 行为模拟器实例
        urls: 要爬取的URL列表
        success_rate: 成功概率
    """
    for url in urls:
        # 模拟爬取延迟
        time.sleep(random.uniform(1.0, 2.0))
        
        # 生成爬取结果
        is_success = random.random() < success_rate
        response_time = random.uniform(0.5, 3.0)
        
        # 准备上下文信息
        context = {
            'url': url,
            'success': is_success,
            'response_time': response_time,
            'blocked': not is_success and random.random() < 0.3,  # 30%概率被检测到
            'recent_failures': sum(1 for _ in range(10) if random.random() > 0.9)
        }
        
        # 模拟页面导航
        result = simulator.simulate_page_navigation(url, context=context)
        
        # 更新环境感知
        simulator._update_environment_awareness(context)
        
        status = "成功" if is_success else "失败"
        print(f"爬取 {url} - 状态: {status}, 响应时间: {response_time:.2f}s, 当前模式: {simulator.behavior_pattern}")


def simulate_high_risk_scenario(simulator, urls):
    """
    模拟高风险场景
    
    Args:
        simulator: 行为模拟器实例
        urls: 要爬取的URL列表
    """
    for url in urls:
        # 模拟快速爬取（增加风险）
        time.sleep(random.uniform(0.2, 0.5))
        
        # 高失败率
        is_success = random.random() < 0.3  # 30%成功率
        response_time = random.uniform(2.0, 5.0)  # 较慢的响应时间
        
        # 准备高风险上下文
        context = {
            'url': url,
            'success': is_success,
            'response_time': response_time,
            'blocked': not is_success,  # 失败即被检测
            'recent_failures': 3,  # 多次失败
            'result': {
                'status': 'error' if not is_success else 'success',
                'error': 'captcha_detected' if not is_success else None,
                'response_time': response_time
            },
            'strategies': {
                'delay': random.uniform(0.5, 1.0),
                'fingerprint': {'advanced': False}
            }
        }
        
        # 模拟页面导航
        result = simulator.simulate_page_navigation(url, context=context)
        
        # 更新环境感知
        simulator._update_environment_awareness(context)
        
        risk_level = simulator.environment_awareness['detection_risk']
        status = "成功" if is_success else "被检测到"
        print(f"爬取 {url} - 状态: {status}, 风险等级: {risk_level:.2f}, 当前模式: {simulator.behavior_pattern}")


def print_metacognitive_insights(simulator):
    """
    打印元认知洞察
    
    Args:
        simulator: 行为模拟器实例
    """
    stats = simulator.get_behavior_statistics()
    
    # 系统状态
    print("系统状态:")
    system_state = stats.get('environment_awareness', {})
    print(f"  - 当前行为模式: {stats.get('current_pattern', 'unknown')}")
    print(f"  - 检测风险: {system_state.get('detection_risk', 0):.2f}")
    print(f"  - 资源压力: CPU={system_state.get('resource_pressure', {}).get('cpu', 0):.2f}, "
          f"内存={system_state.get('resource_pressure', {}).get('memory', 0):.2f}")
    print(f"  - 平均响应时间: {system_state.get('system_performance', {}).get('avg_response_time', 0):.2f}s")
    
    # 最佳策略
    best_strategies = stats.get('best_strategies', {})
    if best_strategies:
        print("\n推荐策略:")
        for strategy, score in best_strategies.items():
            print(f"  - {strategy}: 得分 {score:.2f}")


if __name__ == "__main__":
    try:
        run_metacognition_example()
    except KeyboardInterrupt:
        print("\n示例被用户中断")
    except Exception as e:
        print(f"运行示例时出错: {e}")