#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PhantomCrawler - 隐匿爬虫框架
一键调用入口 | 七宗欲核心引擎 | 实战优化版
"""

import os
import sys
import argparse
import json
import time
from typing import List, Dict, Any, Optional, Callable

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入核心模块
from src.core.crawler import PhantomCrawler
from src.configs.config import global_config


def print_banner():
    """打印程序横幅"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║                     PhantomCrawler                            ║
    ║             高级隐匿爬虫框架 | 七宗欲核心引擎                 ║
    ║                                                               ║
    ║    动态指纹伪装 | 行为模拟 | 协议混淆 | 元认知系统            ║
    ║                                                               ║
    ║          警告: 请在合法授权范围内使用此工具                   ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def load_config_from_file(config_file: str) -> Dict[str, Any]:
    """从配置文件加载配置"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[!] 配置文件加载失败: {str(e)}")
        return {}


def save_config_to_file(config: Dict[str, Any], config_file: str) -> bool:
    """保存配置到文件"""
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[!] 配置文件保存失败: {str(e)}")
        return False


def setup_crawler_config(args: argparse.Namespace) -> None:
    """设置爬虫配置"""
    # 基础配置
    if args.timeout:
        global_config.set('request_timeout', args.timeout)
    
    if args.retries:
        global_config.set('max_retries', args.retries)
    
    # 指纹伪装配置
    global_config.set('fingerprint.enable_dynamic_ua', args.dynamic_ua)
    global_config.set('fingerprint.enable_ja3_simulation', args.ja3)
    global_config.set('fingerprint.enable_browser_fingerprint_spoofing', args.browser_fp)
    
    # 行为模拟配置
    global_config.set('behavior_simulation.enable_human_delay', args.human_delay)
    global_config.set('behavior_simulation.use_gamma_distribution', args.gamma_delay)
    
    if args.min_delay:
        global_config.set('behavior_simulation.min_delay', args.min_delay)
    
    if args.max_delay:
        global_config.set('behavior_simulation.max_delay', args.max_delay)
    
    # 请求链污染
    global_config.set('behavior_simulation.enable_request_chain_pollution', args.request_chain)
    
    # 元认知系统
    global_config.set('metacognition.enabled', args.metacognition)


def process_single_url(crawler: PhantomCrawler, url: str, output_file: Optional[str] = None) -> None:
    """处理单个URL爬取"""
    print(f"\n[*] 开始爬取: {url}")
    start_time = time.time()
    
    try:
        # 定义回调函数
        def response_callback(response: Dict[str, Any]) -> None:
            elapsed = time.time() - start_time
            print(f"[✓] 爬取完成: {url}")
            print(f"[*] 状态码: {response.get('status_code')}")
            print(f"[*] 响应大小: {len(response.get('content', ''))} 字节")
            print(f"[*] 耗时: {elapsed:.2f} 秒")
            
            if output_file:
                # 保存结果到文件
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(response, f, indent=2, ensure_ascii=False)
                print(f"[*] 结果已保存至: {output_file}")
        
        # 执行爬取
        crawler.crawl(url, response_callback=response_callback)
        
    except Exception as e:
        print(f"[✗] 爬取失败: {str(e)}")


def process_url_list(crawler: PhantomCrawler, url_list: List[str], output_dir: Optional[str] = None) -> None:
    """处理URL列表爬取"""
    total = len(url_list)
    success = 0
    
    print(f"\n[*] 开始批量爬取: {total} 个URL")
    
    for i, url in enumerate(url_list, 1):
        print(f"\n[{i}/{total}] 开始爬取: {url}")
        start_time = time.time()
        
        try:
            # 准备输出文件
            output_file = None
            if output_dir:
                # 生成安全的文件名
                safe_filename = f"{i:04d}_{url.replace('://', '_').replace('/', '_').replace('?', '_').replace('&', '_')[:50]}.json"
                output_file = os.path.join(output_dir, safe_filename)
            
            # 定义回调函数
            def response_callback(response: Dict[str, Any], idx=i) -> None:
                nonlocal success
                success += 1
                elapsed = time.time() - start_time
                print(f"[✓] 爬取完成 [{idx}/{total}]: {url}")
                print(f"[*] 状态码: {response.get('status_code')}")
                print(f"[*] 耗时: {elapsed:.2f} 秒")
                
                if output_file:
                    # 保存结果到文件
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(response, f, indent=2, ensure_ascii=False)
            
            # 执行爬取
            crawler.crawl(url, response_callback=response_callback)
            
        except Exception as e:
            print(f"[✗] 爬取失败 [{i}/{total}]: {str(e)}")
        
        # 添加延迟避免请求过于频繁
        if i < total:
            delay = global_config.get('behavior_simulation.min_delay', 1.0)
            print(f"[*] 等待 {delay} 秒后继续...")
            time.sleep(delay)
    
    print(f"\n[*] 批量爬取完成")
    print(f"[*] 成功: {success}, 失败: {total - success}")


def main():
    """主函数"""
    print_banner()
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='PhantomCrawler - 高级隐匿爬虫框架', 
                                     formatter_class=argparse.RawTextHelpFormatter)
    
    # URL参数组
    url_group = parser.add_mutually_exclusive_group(required=True)
    url_group.add_argument('-u', '--url', type=str, help='单个爬取目标URL')
    url_group.add_argument('-l', '--list', type=str, help='包含URL列表的文本文件路径')
    
    # 配置参数
    parser.add_argument('-c', '--config', type=str, help='自定义JSON配置文件路径')
    parser.add_argument('-s', '--save-config', type=str, help='保存当前配置到指定文件')
    
    # 输出参数
    parser.add_argument('-o', '--output', type=str, help='输出文件路径 (单个URL时使用)')
    parser.add_argument('-d', '--output-dir', type=str, help='输出目录路径 (批量URL时使用)')
    
    # 功能开关
    parser.add_argument('--no-dynamic-ua', dest='dynamic_ua', action='store_false', 
                       help='禁用动态User-Agent')
    parser.add_argument('--no-ja3', dest='ja3', action='store_false', 
                       help='禁用JA3指纹模拟')
    parser.add_argument('--no-browser-fp', dest='browser_fp', action='store_false', 
                       help='禁用浏览器指纹欺骗')
    parser.add_argument('--no-human-delay', dest='human_delay', action='store_false', 
                       help='禁用人类延迟模拟')
    parser.add_argument('--no-gamma', dest='gamma_delay', action='store_false', 
                       help='禁用伽马分布延迟')
    parser.add_argument('--no-request-chain', dest='request_chain', action='store_false', 
                       help='禁用请求链污染')
    parser.add_argument('--no-metacognition', dest='metacognition', action='store_false', 
                       help='禁用元认知系统')
    
    # 数值参数
    parser.add_argument('--timeout', type=int, help='请求超时时间 (秒)')
    parser.add_argument('--retries', type=int, help='最大重试次数')
    parser.add_argument('--min-delay', type=float, help='最小延迟时间 (秒)')
    parser.add_argument('--max-delay', type=float, help='最大延迟时间 (秒)')
    
    # 模式选择
    parser.add_argument('--stealth', action='store_true', help='启用最高级别的隐匿模式')
    parser.add_argument('--aggressive', action='store_true', help='启用激进爬取模式')
    parser.add_argument('--balanced', action='store_true', help='启用平衡模式 (默认)')
    
    # 设置默认值
    parser.set_defaults(
        dynamic_ua=True,
        ja3=True,
        browser_fp=True,
        human_delay=True,
        gamma_delay=True,
        request_chain=True,
        metacognition=True
    )
    
    args = parser.parse_args()
    
    # 如果指定了配置文件，加载它
    if args.config:
        custom_config = load_config_from_file(args.config)
        # 应用自定义配置到全局配置
        for key, value in custom_config.items():
            global_config.set(key, value)
    
    # 根据模式预设配置
    if args.stealth:
        print("\n[*] 启用隐匿模式 - 最高级别反检测配置")
        args.dynamic_ua = True
        args.ja3 = True
        args.browser_fp = True
        args.human_delay = True
        args.gamma_delay = True
        args.request_chain = True
        args.metacognition = True
        if not args.min_delay:
            args.min_delay = 2.0
        if not args.max_delay:
            args.max_delay = 8.0
    
    elif args.aggressive:
        print("\n[*] 启用激进模式 - 追求速度和效率")
        args.human_delay = False
        args.request_chain = False
        if not args.timeout:
            args.timeout = 15
        if not args.retries:
            args.retries = 2
    
    elif args.balanced or not any([args.stealth, args.aggressive]):
        print("\n[*] 启用平衡模式 - 性能与隐匿性的平衡")
        # 默认就是平衡模式，不需要特别设置
    
    # 设置爬虫配置
    setup_crawler_config(args)
    
    # 如果需要保存配置
    if args.save_config:
        # 获取当前配置
        current_config = {
            'fingerprint.enable_dynamic_ua': args.dynamic_ua,
            'fingerprint.enable_ja3_simulation': args.ja3,
            'fingerprint.enable_browser_fingerprint_spoofing': args.browser_fp,
            'behavior_simulation.enable_human_delay': args.human_delay,
            'behavior_simulation.use_gamma_distribution': args.gamma_delay,
            'behavior_simulation.enable_request_chain_pollution': args.request_chain,
            'metacognition.enabled': args.metacognition
        }
        
        if args.timeout:
            current_config['request_timeout'] = args.timeout
        if args.retries:
            current_config['max_retries'] = args.retries
        if args.min_delay:
            current_config['behavior_simulation.min_delay'] = args.min_delay
        if args.max_delay:
            current_config['behavior_simulation.max_delay'] = args.max_delay
        
        save_config_to_file(current_config, args.save_config)
        print(f"\n[*] 配置已保存至: {args.save_config}")
    
    # 确保输出目录存在
    if args.output_dir and not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir, exist_ok=True)
    
    # 创建并初始化爬虫
    print("\n[*] 初始化PhantomCrawler...")
    crawler = PhantomCrawler()
    
    if not crawler.initialize():
        print("\n[✗] 爬虫初始化失败！")
        sys.exit(1)
    
    print("[✓] 爬虫初始化成功！")
    
    try:
        # 处理爬取任务
        if args.url:
            # 单个URL爬取
            process_single_url(crawler, args.url, args.output)
        elif args.list:
            # 批量URL爬取
            try:
                with open(args.list, 'r', encoding='utf-8') as f:
                    urls = [line.strip() for line in f if line.strip()]
                
                if not urls:
                    print("\n[!] URL列表文件为空！")
                    sys.exit(1)
                
                process_url_list(crawler, urls, args.output_dir)
                
            except Exception as e:
                print(f"\n[✗] URL列表文件读取失败: {str(e)}")
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n[*] 用户中断操作")
    except Exception as e:
        print(f"\n[✗] 发生未预期的错误: {str(e)}")
    finally:
        print("\n[*] PhantomCrawler 已关闭")


if __name__ == "__main__":
    main()