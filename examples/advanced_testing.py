#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级测试模块 使用示例

警告：此模块展示了高级压力测试和安全评估功能，仅供授权测试使用！
在未获得明确授权的情况下，请勿对任何系统使用这些功能！
"""

import sys
import os
import time

# 将项目根目录添加到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.crawler import PhantomCrawler
from src.modules.intelligence.metacognition_engine import SevenDesiresEngine


def main():
    """
    高级测试模块使用示例主函数
    """
    print("=" * 60)
    print("⚠️  警告：此脚本包含高风险安全测试功能！")
    print("⚠️  仅允许在授权环境中进行安全评估使用！")
    print("⚠️  未授权使用可能违反法律法规！")
    print("=" * 60)
    print()
    
    # 用户确认
    confirm = input("请输入 'YES' 以继续: ")
    if confirm.upper() != 'YES':
        print("操作已取消")
        return
    
    try:
        # 初始化爬虫
        print("[*] 初始化PhantomCrawler...")
        crawler = PhantomCrawler()
        
        if not crawler.initialize():
            print("[✗] 爬虫初始化失败！")
            return
        
        print("[✓] 爬虫初始化成功")
        
        # 示例1: 激活高级测试模块
        print("\n" + "-" * 50)
        print("示例1: 激活高级测试模块")
        print("-" * 50)
        
        if hasattr(crawler.seven_desires, 'activate_advanced_testing'):
            crawler.seven_desires.activate_advanced_testing()
            print(f"[✓] 高级测试模式已激活")
            print(f"[*] 当前运行模式: {crawler.seven_desires.dominant_desire}")
        elif hasattr(crawler.seven_desires, 'awaken_hatred'):  # 兼容旧方法
            print("[*] 使用兼容模式激活高级测试功能...")
            crawler.seven_desires.awaken_hatred()
            print(f"[✓] 高级测试模式已激活")
            print(f"[*] 当前运行模式: {crawler.seven_desires.dominant_desire}")
        else:
            print("[✗] 高级测试模块未找到")
            return
        
        # 示例2: 执行资源压力测试
        print("\n" + "-" * 50)
        print("示例2: 执行资源压力测试")
        print("-" * 50)
        
        # 注意：这里仅使用example.com作为演示，请勿对未授权系统使用
        target_url = "http://example.com"
        print(f"[*] 对目标执行压力测试: {target_url}")
        print("[!] 注意：在实际环境中，这将执行并发请求测试！")
        print("[!] 此处为演示，仅执行单次请求测试")
        
        # 执行单次爬取（在实际激活恨世引擎后，这会自动执行并发压力测试）
        result = crawler.crawl(target_url)
        print(f"[*] 测试结果: {result.get('status', '未知')}")
        print(f"[*] 状态码: {result.get('status_code', '未知')}")
        
        # 示例3: 递归路径测试
        print("\n" + "-" * 50)
        print("示例3: 递归路径测试")
        print("-" * 50)
        
        if hasattr(crawler, 'crawl_iterative'):
            print(f"[*] 开始递归路径测试，起始URL: {target_url}")
            print("[!] 设置较低的深度和URL数量限制以避免过度测试")
            
            # 执行递归路径测试（限制深度和URL数量以安全演示）
            test_results = crawler.crawl_iterative(
                target_url,
                max_depth=1,  # 限制深度
                max_urls=5    # 限制URL数量
            )
            
            print("\n[*] 递归路径测试完成！")
            print(f"[*] 总计测试URL: {test_results.get('total_processed', 0)}")
            print(f"[*] 失败URL: {test_results.get('total_errors', 0)}")
            print(f"[*] 达到深度: {test_results.get('depth_reached', 0)}")
        else:
            print("[✗] 递归路径测试功能不可用")
        
        # 示例4: 智能测试策略优化
        print("\n" + "-" * 50)
        print("示例4: 智能测试策略优化")
        print("-" * 50)
        
        if hasattr(crawler.seven_desires, 'evolve_malicious_strategy'):
            # 模拟失败学习
            print("[*] 模拟失败情况，触发智能策略优化...")
            crawler.seven_desires.evolve_malicious_strategy("示例失败: 被WAF拦截")
            print("[✓] 测试策略已优化更新")
            
            # 显示策略数量
            if hasattr(crawler.seven_desires, 'malicious_strategies'):
                print(f"[*] 当前测试策略数量: {len(crawler.seven_desires.malicious_strategies)}")
        
        # 示例5: 会话重置与日志管理
        print("\n" + "-" * 50)
        print("示例5: 会话重置与日志管理")
        print("-" * 50)
        
        # 测试日志管理功能
        if hasattr(crawler.seven_desires, 'clear_logs'):
            print("[*] 执行会话重置与日志清理...")
            crawler.seven_desires.clear_logs()
            print("[✓] 会话重置完成")
        
        print("\n" + "=" * 60)
        print("安全测试演示完成！")
        print("重要提示：这些高级安全测试功能必须在获得明确授权的环境中使用！")
        print("未授权使用可能违反法律法规并导致严重后果！")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n[*] 用户中断操作")
    except Exception as e:
        print(f"\n[✗] 发生错误: {str(e)}")
        # 触发智能策略优化学习错误
        if 'crawler' in locals() and hasattr(crawler.seven_desires, 'evolve_malicious_strategy'):
            crawler.seven_desires.evolve_malicious_strategy(str(e))


if __name__ == "__main__":
    main()