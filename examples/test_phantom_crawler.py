"""
PhantomCrawler测试脚本
用于验证爬虫框架的核心功能，包括指纹欺骗、行为模拟和请求拦截等
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from src.core.crawler import PhantomCrawler


def print_separator(title):
    """打印分隔符"""
    print(f"\n{'=' * 60}")
    print(f"{title.center(56)}")
    print(f"{'=' * 60}\n")


def test_basic_crawl():
    """测试基本爬取功能"""
    print_separator("测试基本爬取功能")
    
    crawler = PhantomCrawler()
    
    # 初始化爬虫
    if crawler.initialize():
        print(f"初始化成功，会话ID: {crawler.session_id}")
        
        # 爬取一个简单的页面
        test_url = "https://httpbin.org/user-agent"
        print(f"\n正在爬取: {test_url}")
        
        try:
            result = crawler.crawl(test_url)
            print(f"\n爬取结果:")
            print(f"状态码: {result['status_code']}")
            print(f"响应内容: {result['content'][:200]}...")
            print(f"User-Agent: {result.get('user_agent', 'N/A')}")
            print(f"\n爬取成功!")
            return True
        except Exception as e:
            print(f"\n爬取失败: {str(e)}")
            return False
        finally:
            crawler.close()
    else:
        print("初始化失败")
        return False


def test_advanced_features():
    """测试高级功能，包括指纹欺骗和行为模拟"""
    print_separator("测试高级功能")
    
    crawler = PhantomCrawler()
    crawler.initialize()
    
    try:
        # 打印爬虫统计信息
        stats = crawler.get_stats()
        print("\n爬虫统计信息:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # 测试指纹欺骗功能
        print("\n指纹欺骗功能测试:")
        fingerprint = crawler.fingerprint_spoofer.generate_fingerprint()
        print(f"生成的指纹:")
        for header, value in list(fingerprint.items())[:5]:  # 只显示部分头部
            print(f"  {header}: {value}")
        print(f"  ... 等更多头部")
        
        # 测试Canvas指纹混淆脚本
        canvas_script = crawler.fingerprint_spoofer.get_canvas_fingerprint_confusion_script()
        print(f"\nCanvas混淆脚本长度: {len(canvas_script)} 字符")
        print(canvas_script[:200] + "...")
        
        # 测试WebGL指纹混淆脚本
        webgl_script = crawler.fingerprint_spoofer.get_webgl_fingerprint_confusion_script()
        print(f"\nWebGL混淆脚本长度: {len(webgl_script)} 字符")
        print(webgl_script[:200] + "...")
        
        # 测试请求签名
        signature = crawler.fingerprint_spoofer.generate_request_signature()
        print(f"\n请求签名:")
        for key, value in signature.items():
            print(f"  {key}: {value}")
        
        # 测试行为模拟器统计
        behavior_stats = crawler.behavior_simulator.get_behavior_statistics()
        print(f"\n行为模拟器配置:")
        for key, value in behavior_stats.items():
            print(f"  {key}: {value}")
            
        return True
        
    except Exception as e:
        print(f"\n高级功能测试失败: {str(e)}")
        return False
    finally:
        crawler.close()


def test_request_chain():
    """测试请求链功能"""
    print_separator("测试请求链功能")
    
    crawler = PhantomCrawler()
    crawler.initialize()
    
    try:
        # 生成请求链
        test_url = "https://example.com"
        request_chain = crawler.fingerprint_spoofer.generate_request_chain(test_url)
        
        print(f"\n为 {test_url} 生成的请求链:")
        for i, url in enumerate(request_chain):
            print(f"  {i+1}. {url}")
        
        return True
    
    except Exception as e:
        print(f"\n请求链测试失败: {str(e)}")
        return False
    finally:
        crawler.close()


def test_proxy_rotation():
    """测试代理轮换功能"""
    print_separator("测试代理功能")
    
    crawler = PhantomCrawler()
    crawler.initialize()
    
    try:
        # 检查代理配置
        proxy_count = len(crawler.protocol_obfuscator.proxy_chain)
        print(f"\n当前配置的代理数量: {proxy_count}")
        
        if proxy_count > 0:
            print("代理列表:")
            for i, proxy in enumerate(crawler.protocol_obfuscator.proxy_chain):
                print(f"  {i+1}. {proxy}")
            
            # 测试代理轮换
            print("\n测试代理轮换...")
            crawler.protocol_obfuscator.rotate_proxy_chain()
            print("代理轮换成功")
        else:
            print("注意: 当前没有配置代理，代理功能未启用")
        
        return True
    
    except Exception as e:
        print(f"\n代理功能测试失败: {str(e)}")
        return False
    finally:
        crawler.close()


def test_captcha_detection():
    """测试验证码检测功能"""
    print_separator("测试验证码检测功能")
    
    crawler = PhantomCrawler()
    crawler.initialize()
    
    try:
        # 测试包含验证码关键词的HTML
        captcha_html = """
        <html>
        <body>
            <div class="captcha-container">
                <img src="captcha.jpg" alt="验证码">
                <div id="recaptcha-widget"></div>
                <script>
                    grecaptcha.execute('site-key');
                </script>
            </div>
            <h1>请完成安全验证</h1>
            <p>我们检测到不寻常的访问模式，请证明您不是机器人</p>
        </body>
        </html>
        """
        
        # 测试不含验证码的HTML
        normal_html = """
        <html>
        <body>
            <h1>欢迎访问</h1>
            <p>这是一个普通的网页内容</p>
        </body>
        </html>
        """
        
        is_captcha1 = crawler.fingerprint_spoofer.is_captcha_page(captcha_html)
        is_captcha2 = crawler.fingerprint_spoofer.is_captcha_page(normal_html)
        
        print(f"\n测试1 (包含验证码): {is_captcha1}")
        print(f"测试2 (普通页面): {is_captcha2}")
        
        # 测试URL检测
        captcha_url = "https://example.com/captcha?challenge=12345"
        normal_url = "https://example.com/home"
        
        is_captcha_url1 = crawler.fingerprint_spoofer.is_captcha_url(captcha_url)
        is_captcha_url2 = crawler.fingerprint_spoofer.is_captcha_url(normal_url)
        
        print(f"\nURL测试1 (验证码URL): {is_captcha_url1}")
        print(f"URL测试2 (普通URL): {is_captcha_url2}")
        
        return True
        
    except Exception as e:
        print(f"\n验证码检测功能测试失败: {str(e)}")
        return False
    finally:
        crawler.close()


def main():
    """主测试函数"""
    print("""
    ====================================================================
                   PhantomCrawler 功能测试套件
    ====================================================================
    此脚本将测试PhantomCrawler框架的核心功能，包括：
    - 基本爬取功能
    - 指纹欺骗与混淆
    - 行为模拟
    - 请求链生成
    - 验证码检测
    ====================================================================
    """)
    
    # 执行所有测试
    tests = [
        ("基本爬取功能", test_basic_crawl),
        ("高级功能测试", test_advanced_features),
        ("请求链功能测试", test_request_chain),
        ("代理功能测试", test_proxy_rotation),
        ("验证码检测功能", test_captcha_detection)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        print(f"\n[{time.strftime('%H:%M:%S')}] 执行测试: {name}")
        if test_func():
            passed += 1
            print(f"[{time.strftime('%H:%M:%S')}] ✅ 测试通过: {name}")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] ❌ 测试失败: {name}")
        
        # 测试之间添加延迟，避免请求过于频繁
        if test_func != tests[-1][1]:  # 不是最后一个测试
            print(f"\n等待 3 秒后继续下一个测试...")
            time.sleep(3)
    
    # 打印测试结果摘要
    print_separator("测试结果摘要")
    print(f"总测试数: {total}")
    print(f"通过测试数: {passed}")
    print(f"失败测试数: {total - passed}")
    
    if passed == total:
        print("🎉 所有测试通过! PhantomCrawler框架功能正常。")
    else:
        print("⚠️  部分测试失败，请检查相关功能。")
    
    print_separator("测试完成")


if __name__ == "__main__":
    main()