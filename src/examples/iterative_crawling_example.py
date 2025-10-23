#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PhantomCrawler - 迭代爬取示例

此示例演示如何使用PhantomCrawler的迭代爬取功能，
自动从起始URL开始，提取链接并递归爬取整个网站。
"""

import time
from core.crawler import PhantomCrawler

def main():
    """主函数，演示迭代爬取功能"""
    print("=== PhantomCrawler 迭代爬取示例 ===")
    print()
    
    # 初始化爬虫实例
    crawler = PhantomCrawler()
    
    # 示例1: 基础迭代爬取（仅同一域名，深度2，最多10个URL）
    print("[示例1] 基础迭代爬取")
    print("-" * 50)
    
    start_url = "https://example.com"  # 替换为你想爬取的网站
    results = crawler.crawl_iterative(
        start_url=start_url,
        max_depth=2,               # 最大爬取深度
        same_domain_only=True,     # 只爬取相同域名
        max_urls=10                # 最多爬取10个URL
    )
    
    # 打印结果摘要
    summary = results['summary']
    print(f"\n爬取结果摘要:")
    print(f"- 总爬取URL数: {summary['total_urls']}")
    print(f"- 成功爬取: {summary['successful_urls']}")
    print(f"- 爬取失败: {summary['failed_urls']}")
    print(f"- 达到最大深度: {summary['max_depth_reached']}")
    print(f"- 已访问URL列表: {', '.join(summary['visited_urls'][:5])}...")
    print()
    
    # 示例2: 高级迭代爬取（使用URL过滤模式）
    print("[示例2] 高级迭代爬取（使用URL过滤）")
    print("-" * 50)
    
    # 只爬取包含"blog"或"article"的URL，排除"login"或"admin"的URL
    results_advanced = crawler.crawl_iterative(
        start_url=start_url,
        max_depth=3,
        same_domain_only=True,
        include_patterns=["blog", "article", "news"],
        exclude_patterns=["login", "admin", "logout", "cart"],
        max_urls=20
    )
    
    # 打印高级爬取结果
    summary_advanced = results_advanced['summary']
    print(f"\n高级爬取结果摘要:")
    print(f"- 总爬取URL数: {summary_advanced['total_urls']}")
    print(f"- 成功爬取: {summary_advanced['successful_urls']}")
    print(f"- 已访问URL列表: {', '.join(summary_advanced['visited_urls'][:5])}...")
    print()
    
    # 示例3: 爬取指定URL模式的页面内容
    print("[示例3] 内容提取示例")
    print("-" * 50)
    
    # 假设我们想提取所有博客文章的标题（这里只是示例逻辑）
    blog_results = crawler.crawl_iterative(
        start_url=start_url,
        max_depth=1,
        same_domain_only=True,
        include_patterns=["blog", "article"],
        max_urls=5
    )
    
    print("\n提取到的文章页面:")
    for url, result in blog_results['results'].items():
        if result.get('success') and 'content' in result:
            print(f"- 成功爬取: {url}")
            # 这里可以添加内容提取逻辑，如使用正则表达式或其他解析方法
    
    print()
    print("=== 迭代爬取示例完成 ===")

if __name__ == "__main__":
    main()