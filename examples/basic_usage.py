#!/usr/bin/env python3
# PhantomCrawler - 使用示例脚本

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.crawler import PhantomCrawler
from src.configs.config import global_config

def main():
    """PhantomCrawler使用示例"""
    print("=" * 60)
    print("        PhantomCrawler - 幽灵爬虫框架示例")
    print("=" * 60)
    print("这是一个高级隐匿爬虫框架，具备规避、持久化和自适应能力")
    print("\n注意：请确保在合法授权的范围内使用此工具")
    print("=" * 60)
    
    # 配置爬虫参数
    print("\n[*] 配置爬虫参数...")
    
    # 启用指纹伪装
    global_config.set('fingerprint.enable_dynamic_ua', True)
    global_config.set('fingerprint.enable_ja3_simulation', True)
    
    # 启用行为模拟
    global_config.set('behavior_simulation.enable_human_delay', True)
    global_config.set('behavior_simulation.use_gamma_distribution', True)
    
    # 启用请求链污染
    global_config.set('behavior_simulation.enable_request_chain_pollution', True)
    
    # 创建爬虫实例
    print("\n[*] 初始化PhantomCrawler...")
    crawler = PhantomCrawler()
    
    # 初始化爬虫
    if not crawler.initialize():
        print("[!] 爬虫初始化失败")
        return
    
    try:
        # 示例1: 单URL爬取
        print("\n[*] 示例1: 单URL爬取")
        test_url = "http://httpbin.org/anything"
        print(f"[*] 正在爬取: {test_url}")
        
        # 定义回调函数处理响应
        def process_response(response_data):
            print(f"[+] 爬取成功，状态码: {response_data['status_code']}")
            print(f"[+] 响应长度: {len(response_data['content'])} 字节")
            print(f"[+] 服务端看到的请求头摘要:")
            # 在实际使用中，这里可以提取和处理数据
        
        # 执行爬取
        result = crawler.crawl(test_url, callback=process_response)
        
        # 示例2: 批量爬取
        print("\n[*] 示例2: 批量爬取")
        batch_urls = [
            "http://httpbin.org/ip",
            "http://httpbin.org/user-agent",
            "http://httpbin.org/headers"
        ]
        
        print(f"[*] 正在批量爬取 {len(batch_urls)} 个URL...")
        batch_results = crawler.crawl_batch(batch_urls, max_concurrent=2)
        
        print(f"[+] 批量爬取完成，成功: {len(batch_results)} 个")
        
        # 显示统计信息
        print("\n[*] 爬虫统计信息:")
        stats = crawler.get_stats()
        for key, value in stats.items():
            print(f"    {key}: {value}")
            
    except KeyboardInterrupt:
        print("\n[!] 用户中断操作")
    except Exception as e:
        print(f"\n[!] 发生错误: {str(e)}")
    finally:
        # 关闭爬虫
        print("\n[*] 正在关闭爬虫...")
        crawler.close()
        print("[+] 爬虫已安全关闭")

def advanced_usage_example():
    """高级使用示例 - 配置代理链和自定义选项"""
    print("\n" + "=" * 60)
    print("        高级使用示例 - 配置代理链")
    print("=" * 60)
    
    # 配置代理链
    proxies = [
        {
            'type': 'http',
            'host': '127.0.0.1',
            'port': 8080,
            'username': '',
            'password': ''
        },
        {
            'type': 'socks5',
            'host': '127.0.0.1',
            'port': 1080,
            'username': '',
            'password': ''
        }
    ]
    
    # 设置代理链
    global_config.set('proxy_chain', proxies)
    
    # 创建协议混淆器
    from src.modules.evasion.protocol_obfuscator import ProtocolObfuscator
    obfuscator = ProtocolObfuscator()
    
    # 构建优化的代理链
    optimized_chain = obfuscator.build_proxy_chain(proxies)
    print(f"[*] 优化后的代理链: {[f'{p['type']}://{p['host']}:{p['port']}' for p in optimized_chain]}")
    
    print("\n[*] 高级配置完成")

if __name__ == "__main__":
    main()
    
    # 询问是否展示高级使用示例
    if input("\n是否查看高级使用示例？(y/n): ").lower() == 'y':
        advanced_usage_example()
    
    print("\n" + "=" * 60)
    print("示例运行完成。请参考源代码了解更多高级功能")
    print("=" * 60)