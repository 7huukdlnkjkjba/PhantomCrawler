#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试高级测试模块

此脚本用于测试PhantomCrawler的高级测试模块功能
包含压力测试、递归路径测试和智能策略优化等安全评估功能
仅用于授权的安全测试环境
"""

import sys
import os
import time

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.crawler import PhantomCrawler
from src.modules.intelligence.metacognition_engine import SevenDesiresEngine

def test_advanced_testing():
    """测试高级测试模块功能"""
    print("========== 测试高级测试模块 ==========")
    print("警告：以下测试将执行高级安全评估功能，仅用于授权测试环境！")
    
    # 初始化爬虫
    crawler = PhantomCrawler(auto_initialize=True)
    
    # 激活高级测试模式
    print("\n[测试] 激活高级测试模式...")
    if hasattr(crawler.seven_desires, 'activate_advanced_testing'):
        crawler.seven_desires.activate_advanced_testing()
        print(f"[测试] 当前运行模式: {crawler.seven_desires.dominant_desire}")
    elif hasattr(crawler.seven_desires, 'awaken_hatred'):  # 兼容旧方法名
        print("[测试] 使用兼容模式激活高级测试功能...")
        crawler.seven_desires.awaken_hatred()
        print(f"[测试] 当前运行模式: {crawler.seven_desires.dominant_desire}")
    else:
        print("[测试] 高级测试模式激活功能未找到！")
        return
    
    # 测试递归路径测试功能（在安全的测试域名上）
    print("\n[测试] 开始测试递归路径测试...")
    test_url = "http://example.com"
    try:
        print(f"[测试] 开始递归测试目标: {test_url}")
        # 使用深度为1进行简单测试
        results = crawler.crawl_iterative(test_url, max_depth=1, max_urls=5)
        print(f"[测试] 测试完成，总计处理URL数: {len(results.get('results', {}))}")
    except Exception as e:
        print(f"[测试] 测试过程中发生错误: {str(e)}")
    
    # 检查策略优化情况
    print("\n[测试] 检查策略优化状态...")
    if hasattr(crawler.seven_desires, 'testing_strategies'):
        print(f"[测试] 优化策略数量: {len(crawler.seven_desires.testing_strategies)}")
    elif hasattr(crawler.seven_desires, 'malicious_strategies'):  # 兼容旧策略名
        print(f"[测试] 优化策略数量: {len(crawler.seven_desires.malicious_strategies)}")
    
    print("\n========== 测试完成 ==========")

if __name__ == "__main__":
    test_advanced_testing()