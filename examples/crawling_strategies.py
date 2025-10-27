#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PhantomCrawler - 七宗欲实战示例

这个示例展示如何使用七宗欲增强版的PhantomCrawler进行实战爬取。
七宗欲引擎为爬虫提供了七种不同的欲望模式，每种模式都有独特的爬取策略。
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import json
from src.core.crawler import PhantomCrawler

def print_separator():
    """打印分隔线"""
    print("="*80)

def demonstrate_seven_desires_crawling():
    """演示七宗欲爬虫的使用"""
    print_separator()
    print("🚀 PhantomCrawler - 七宗欲实战演示")
    print_separator()
    
    # 创建爬虫实例
    crawler = PhantomCrawler()
    
    # 测试目标URL列表
    test_urls = [
        "https://www.example.com",  # 基础测试
        "https://www.wikipedia.org"  # 复杂页面测试
    ]
    
    # 记录每种欲望模式的成功率
    results = {}
    
    for url in test_urls:
        print(f"\n🔍 开始测试目标: {url}")
        print_separator()
        
        # 执行爬取
        try:
            print(f"[七宗欲爬虫] 开始爬取 - 自动选择欲望模式")
            start_time = time.time()
            result = crawler.crawl(url)
            end_time = time.time()
            
            # 显示结果
            print(f"✅ 爬取成功！耗时: {end_time - start_time:.2f}秒")
            print(f"📊 状态码: {result.get('status_code')}")
            print(f"📱 当前主导欲望: {getattr(crawler.seven_desires, 'dominant_desire', '未知')}")
            print(f"🛡️  当前风险等级: {getattr(crawler.seven_desires, 'desire_perception', {}).get('detection_danger', 0):.2f}")
            
            # 保存结果
            results[url] = {
                'success': True,
                'status_code': result.get('status_code'),
                'time': end_time - start_time,
                'dominant_desire': getattr(crawler.seven_desires, 'dominant_desire', '未知'),
                'risk_level': getattr(crawler.seven_desires, 'desire_perception', {}).get('detection_danger', 0)
            }
            
            # 短暂休息
            print(f"⏸️  休息5秒...")
            time.sleep(5)
            
        except Exception as e:
            print(f"❌ 爬取失败: {str(e)}")
            results[url] = {
                'success': False,
                'error': str(e)
            }
    
    print_separator()
    print("📊 爬取结果汇总")
    print_separator()
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    # 分析结果
    success_count = sum(1 for r in results.values() if r.get('success'))
    total_urls = len(results)
    success_rate = (success_count / total_urls) * 100 if total_urls > 0 else 0
    
    print_separator()
    print(f"🎯 总体成功率: {success_rate:.1f}% ({success_count}/{total_urls})")
    print(f"🔥 七宗欲引擎实战测试完成！")
    print_separator()

def test_different_desire_patterns():
    """测试不同欲望模式的效果（通过手动触发）"""
    print("\n" + "="*80)
    print("🎭 测试不同欲望模式的效果")
    print("="*80)
    
    crawler = PhantomCrawler()
    test_url = "https://www.example.com"
    
    # 获取七宗欲引擎
    seven_desires = crawler.seven_desires
    
    if hasattr(seven_desires, 'force_dominant_desire'):
        print("\n⚠️  注意：七宗欲引擎支持强制欲望模式切换")
        print("   在生产环境中，请让引擎自动选择欲望模式以获得最佳效果")
    else:
        print("\nℹ️  七宗欲引擎当前使用自动欲望切换模式")
    
    print("\n💡 实战建议:")
    print("1. 对于高防护网站，建议让七宗欲引擎自动选择欲望模式")
    print("2. 连续失败时，引擎会自动切换到更适合的欲望模式")
    print("3. 每个欲望模式有独特的策略组合，针对不同的反爬机制")
    print("4. 长期运行时，引擎会学习并优化策略选择")
    print_separator()

def main():
    """主函数"""
    print("\n" + "="*80)
    print("👿 PhantomCrawler - 七宗欲引擎实战版")
    print("🚀 超越普通爬虫的反检测能力")
    print("✅ 适用于高难度网站爬取场景")
    print("="*80)
    
    # 执行基础测试
    demonstrate_seven_desires_crawling()
    
    # 测试不同欲望模式
    test_different_desire_patterns()
    
    print("\n✨ 演示完成！")
    print("📚 更多用法请参考文档")
    print("🔒 七宗欲引擎将持续学习并优化爬取策略")

if __name__ == "__main__":
    main()