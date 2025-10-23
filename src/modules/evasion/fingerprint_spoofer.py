# PhantomCrawler - 动态指纹伪装模块
import random
import time
from typing import Dict, List, Optional
import httpx
import ssl
from urllib.parse import urlparse
from src.config import global_config

class FingerprintSpoofer:
    """动态生成和模拟浏览器指纹的核心类"""
    
    def __init__(self):
        # 从配置获取用户代理池
        self.user_agent_pool = global_config.get('user_agent_pool', [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Mobile Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/114.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
        ])
        self.accept_languages = global_config.get('fingerprint.accept_languages', ['en-US,en;q=0.9'])
        self.accept_encodings = global_config.get('fingerprint.accept_encodings', ['gzip', 'deflate', 'br'])
        self.session_headers = None
        
        # JA3指纹映射表（模拟不同浏览器的TLS握手特征）
        self.ja3_fingerprints = {
            'chrome': {
                'ciphers': '4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53',
                'extensions': '0-10-11-13-16-23-28-35-43-45',
                'curves': '29-23-24-25',
            },
            'firefox': {
                'ciphers': '4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53',
                'extensions': '0-10-11-13-16-23-28-35-43-45-51',
                'curves': '29-23-24-25-26',
            },
            'safari': {
                'ciphers': '4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53',
                'extensions': '0-10-11-13-16-23-28-35-43',
                'curves': '23-24-25',
            }
        }
    
    def generate_fingerprint(self, browser_type: Optional[str] = None) -> Dict[str, str]:
        """生成完整的浏览器指纹"""
        if not browser_type:
            browser_type = random.choice(['chrome', 'firefox', 'safari'])
        
        # 生成User-Agent
        if global_config.get('fingerprint.enable_dynamic_ua', True):
            user_agent = self._generate_user_agent(browser_type)
        else:
            user_agent = random.choice(self.user_agent_pool)
        
        # 构建完整的HTTP头
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': random.choice(self.accept_languages),
            'Accept-Encoding': ', '.join(self.accept_encodings),
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }
        
        # 添加浏览器特定的头部
        if browser_type == 'chrome':
            headers['Sec-Ch-Ua'] = '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"'
            headers['Sec-Ch-Ua-Mobile'] = '?0'
            headers['Sec-Ch-Ua-Platform'] = '"Windows"'
        elif browser_type == 'firefox':
            headers['TE'] = 'trailers'
        
        self.session_headers = headers
        return headers
    
    def _generate_user_agent(self, browser_type: str) -> str:
        """根据浏览器类型生成对应的User-Agent"""
        # 根据浏览器类型过滤UA池
        filtered_uas = [ua for ua in self.user_agent_pool if browser_type.lower() in ua.lower()]
        if filtered_uas:
            return random.choice(filtered_uas)
        else:
            # 如果没有匹配的，返回一个通用的UA
            return random.choice(self.user_agent_pool)
    
    def configure_httpx_client(self, client: httpx.Client) -> httpx.Client:
        """配置httpx客户端以模拟特定的TLS指纹"""
        if global_config.get('fingerprint.enable_ja3_simulation', True):
            # 选择随机浏览器的JA3指纹
            browser_type = random.choice(['chrome', 'firefox', 'safari'])
            ja3 = self.ja3_fingerprints[browser_type]
            
            # 配置TLS参数（httpx使用ssl模块，我们可以通过SSLContext配置）
            import ssl
            context = ssl.create_default_context()
            
            # 这里简化了JA3模拟，实际实现需要更复杂的TLS参数调整
            # 在实际使用中，可能需要使用如tls_client这样的第三方库来精确模拟JA3
            
            client._transport._pool._ssl_context = context
        
        # 设置之前生成的头部
        if self.session_headers:
            client.headers.update(self.session_headers)
        
        return client
    
    def get_playwright_fingerprint_overrides(self) -> Dict[str, any]:
        """获取Playwright浏览器指纹覆盖配置
        
        Returns:
            Playwright指纹覆盖配置字典
        """
        # 随机选择浏览器类型
        browser_type = random.choice(['chrome', 'firefox', 'safari'])
        
        # 模拟真实的浏览器特征
        overrides = {
            # 基础信息
            'userAgent': self._generate_detailed_user_agent(browser_type),
            'viewport': {
                'width': random.choice([1366, 1440, 1536, 1920, 2560]),
                'height': random.choice([768, 900, 1080, 1440])
            },
            
            # 语言设置
            'locale': random.choice(['en-US', 'zh-CN', 'ja-JP', 'en-GB', 'fr-FR', 'de-DE']),
            
            # 时区
            'timezoneId': random.choice([
                'America/New_York', 'Asia/Shanghai', 'Europe/London',
                'Asia/Tokyo', 'Europe/Paris', 'America/Los_Angeles'
            ]),
            
            # 设备内存
            'deviceMemory': random.choice([4, 8, 16]),
            
            # CPU核心数
            'hardwareConcurrency': random.choice([4, 6, 8, 12, 16]),
            
            # 媒体设备
            'mediaDevices': {
                'videoInputs': random.randint(1, 2),
                'audioInputs': random.randint(1, 2),
                'audioOutputs': random.randint(1, 2)
            },
            
            # 地理位置信息（随机但合理的位置）
            'geolocation': {
                'latitude': random.uniform(-90, 90),
                'longitude': random.uniform(-180, 180),
                'accuracy': random.uniform(50, 1000)
            }
        }
        
        # 根据浏览器类型添加特定配置
        if browser_type == 'chrome':
            overrides['acceptLanguage'] = random.choice(['en-US,en;q=0.9', 'zh-CN,zh;q=0.9'])
            overrides['userAgentMetadata'] = {
                'brands': [
                    {"brand": "Google Chrome", "version": str(random.randint(90, 120))},
                    {"brand": "Chromium", "version": str(random.randint(90, 120))},
                    {"brand": "Not A(Brand)", "version": "8"}
                ],
                'platform': random.choice(['Windows', 'macOS', 'Linux']),
                'platformVersion': str(random.randint(10, 11)) if 'Windows' in overrides['userAgentMetadata']['platform'] else '10.15',
                'architecture': random.choice(['x86', 'x86-64', 'ARM']),
                'model': '',
                'mobile': False
            }
        
        elif browser_type == 'firefox':
            overrides['acceptLanguage'] = random.choice(['en-US,en;q=0.5', 'zh-CN,zh;q=0.5'])
            
        elif browser_type == 'safari':
            overrides['acceptLanguage'] = random.choice(['en-US,en;q=0.9', 'zh-CN,zh;q=0.9'])
            overrides['userAgent'] = overrides['userAgent'].replace('AppleWebKit/605.1.15', f'AppleWebKit/{random.randint(600, 620)}.{random.randint(1, 20)}.{random.randint(1, 20)}')
        
        return overrides
    
    def _generate_detailed_user_agent(self, browser_type: str) -> str:
        """生成更详细的User-Agent字符串
        
        Args:
            browser_type: 浏览器类型（chrome, firefox, safari）
            
        Returns:
            详细的User-Agent字符串
        """
        if browser_type == 'chrome':
            versions = {
                'chrome': f'{random.randint(90, 120)}.0.{random.randint(0, 9999)}.{random.randint(0, 99)}',
                'webkit': f'537.{random.randint(1, 34)}',
                'gecko': f'20030107'
            }
            platforms = [
                f'Macintosh; Intel Mac OS X {random.randint(10, 15)}_{random.randint(0, 9)}_{random.randint(0, 9)}',
                f'Windows NT {random.randint(10, 11)}.0',
                f'X11; Linux x86_64',
                f'X11; CrOS {random.randint(8000, 9000)}.{random.randint(100, 999)}.0.0'
            ]
            return f'Mozilla/5.0 ({random.choice(platforms)}) AppleWebKit/{versions["webkit"]} (KHTML, like Gecko) Chrome/{versions["chrome"]} Safari/{versions["webkit"]}'
        
        elif browser_type == 'firefox':
            versions = {
                'firefox': f'{random.randint(80, 110)}.0',
                'gecko': f'{random.randint(20100101, 20231231)}'
            }
            platforms = [
                f'Windows NT {random.randint(10, 11)}.0; Win64; x64',
                f'Windows NT {random.randint(6, 10)}.0',
                f'Macintosh; Intel Mac OS X {random.randint(10, 15)}_{random.randint(0, 9)}_{random.randint(0, 9)}',
                f'X11; Linux x86_64'
            ]
            return f'Mozilla/5.0 ({random.choice(platforms)}) Gecko/{versions["gecko"]} Firefox/{versions["firefox"]}'
        
        elif browser_type == 'safari':
            versions = {
                'safari': f'{random.randint(14, 17)}.{random.randint(0, 9)}',
                'webkit': f'605.{random.randint(1, 15)}'
            }
            platforms = [
                f'Macintosh; Intel Mac OS X {random.randint(10, 15)}_{random.randint(0, 9)}_{random.randint(0, 9)}',
                f'iPad; CPU OS {random.randint(14, 16)}_{random.randint(0, 9)} like Mac OS X',
                f'iPhone; CPU iPhone OS {random.randint(14, 16)}_{random.randint(0, 9)} like Mac OS X'
            ]
            return f'Mozilla/5.0 ({random.choice(platforms)}) AppleWebKit/{versions["webkit"]} (KHTML, like Gecko) Version/{versions["safari"]} Safari/{versions["webkit"]}'
        
        # 默认返回Chrome UA
        return random.choice(self.user_agent_pool)
    
    def generate_dynamic_headers(self, url: str, referrer: Optional[str] = None) -> Dict[str, str]:
        """根据URL和referrer动态生成HTTP头部，增强版
        
        Args:
            url: 目标URL
            referrer: 引荐URL
            
        Returns:
            动态生成的HTTP头部字典
        """
        # 基础头部
        headers = self.generate_fingerprint()
        
        # 添加referrer信息 - 更智能的策略
        if referrer:
            # 检查是否是同一域名
            referrer_domain = urlparse(referrer).netloc
            target_domain = urlparse(url).netloc
            
            if referrer_domain != target_domain:
                # 跨域请求时，模拟真实浏览器的referrer策略
                if random.random() < 0.9:  # 90%概率保留完整referrer
                    headers['Referer'] = referrer
                else:  # 10%概率只保留域名部分
                    headers['Referer'] = f"{urlparse(referrer).scheme}://{referrer_domain}/"
            else:
                # 同域请求，总是保留完整referrer
                headers['Referer'] = referrer
        else:
            # 动态生成合理的referrer，基于目标URL的性质
            parsed_url = urlparse(url)
            
            # 针对不同类型网站的referrer策略
            if any(s in parsed_url.netloc for s in ['google', 'bing', 'baidu', 'yahoo']):
                # 搜索引擎页面通常没有referrer
                pass
            elif any(s in parsed_url.path for s in ['login', 'signin', 'auth']):
                # 登录页面通常来自主页或之前的页面
                possible_referrers = [
                    f"{parsed_url.scheme}://{parsed_url.netloc}/",
                    f"{parsed_url.scheme}://{parsed_url.netloc}/index.html"
                ]
                if random.random() < 0.4:  # 40%概率设置为主页
                    headers['Referer'] = random.choice(possible_referrers)
            else:
                # 常规页面
                possible_referrers = [
                    # 搜索引擎
                    f'https://www.google.com/search?q={self._generate_realistic_search_query()}',
                    f'https://www.bing.com/search?q={self._generate_realistic_search_query()}',
                    f'https://www.baidu.com/s?wd={self._generate_realistic_search_query()}',
                    
                    # 社交媒体和新闻网站
                    'https://www.reddit.com/',
                    'https://twitter.com/',
                    'https://www.facebook.com/',
                    'https://www.linkedin.com/',
                    'https://www.youtube.com/',
                    'https://news.google.com/',
                    'https://www.cnn.com/',
                    'https://www.nytimes.com/',
                    
                    # 技术网站
                    'https://github.com/',
                    'https://stackoverflow.com/',
                    'https://developer.mozilla.org/'
                ]
                
                # 基于目标网站类型选择合适的referrer
                if '.gov' in parsed_url.netloc:
                    # 政府网站更可能来自搜索引擎
                    if random.random() < 0.6:  # 60%概率设置为搜索引擎
                        headers['Referer'] = random.choice(possible_referrers[:3])
                elif '.edu' in parsed_url.netloc:
                    # 教育网站可能来自搜索引擎或其他教育网站
                    if random.random() < 0.7:  # 70%概率设置为搜索引擎或技术网站
                        headers['Referer'] = random.choice(possible_referrers[:3] + possible_referrers[-3:])
                else:
                    # 其他网站
                    if random.random() < 0.4:  # 40%概率设置为搜索引擎
                        headers['Referer'] = random.choice(possible_referrers)
        
        # 动态设置Sec-Fetch-Site
        if referrer:
            referrer_domain = urlparse(referrer).netloc
            target_domain = urlparse(url).netloc
            
            if referrer_domain == target_domain:
                headers['Sec-Fetch-Site'] = 'same-origin'
            elif referrer_domain.endswith(target_domain) or target_domain.endswith(referrer_domain):
                headers['Sec-Fetch-Site'] = 'same-site'
            else:
                headers['Sec-Fetch-Site'] = 'cross-site'
        else:
            headers['Sec-Fetch-Site'] = 'none'
        
        # 模拟缓存控制 - 更智能的策略
        if random.random() < 0.6:  # 提高概率到60%
            headers['Cache-Control'] = random.choice([
                'no-cache',
                'max-age=0',
                'private, max-age=0',
                'max-age=300',
                'max-age=600',
                'max-age=1800'
            ])
        
        # 随机添加一些可选头部
        optional_headers = {
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'DNT': '1',
            'Sec-Fetch-Dest': random.choice(['document', 'empty', 'image', 'script']),
            'Sec-Fetch-Mode': random.choice(['navigate', 'no-cors', 'cors']),
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-CH': 'UA, Platform, Width, Height, DPR',
            'Accept-CH-Lifetime': '86400'
        }
        
        # 随机选择1-3个可选头部添加
        optional_count = random.randint(1, 3)
        selected_optional = random.sample(list(optional_headers.items()), min(optional_count, len(optional_headers)))
        headers.update(dict(selected_optional))
        
        # 根据User-Agent调整头部
        user_agent = headers.get('User-Agent', '')
        if 'Chrome' in user_agent and 'Edg' not in user_agent:
            # Chrome特有头部
            if random.random() < 0.8:
                headers['Sec-Ch-Ua'] = f'"{self._generate_chrome_ua_string()}"'
                headers['Sec-Ch-Ua-Mobile'] = '?0'
                headers['Sec-Ch-Ua-Platform'] = f'"{self._generate_platform_string()}"'
        elif 'Firefox' in user_agent:
            # Firefox特有头部
            if random.random() < 0.7:
                headers['Sec-Fetch-Dest'] = 'document'
                headers['TE'] = 'trailers'
        elif 'Safari' in user_agent and 'Chrome' not in user_agent:
            # Safari特有头部
            if random.random() < 0.6:
                headers.pop('Sec-Fetch-User', None)  # Safari有时不发送这个头部
        
        return headers
    
    def _generate_realistic_search_query(self) -> str:
        """生成看起来更真实的搜索查询"""
        query_patterns = [
            'best restaurants near me',
            'how to fix {0}',
            'top {0} in {1}',
            'compare {0} vs {1}',
            'reviews for {0}',
            'when is {0}',
            'where to buy {0}',
            '{0} tutorial',
            'what is {0}',
            'why does {0} happen'
        ]
        
        common_nouns = ['phone', 'computer', 'car', 'book', 'movie', 'software', 'tool', 'service', 'product']
        common_verbs = ['crash', 'slow', 'break', 'work', 'function', 'improve']
        common_places = ['new york', 'london', 'tokyo', 'beijing', 'paris', 'berlin']
        common_years = [str(random.randint(2020, 2024))]
        
        pattern = random.choice(query_patterns)
        
        # 填充模板
        if '{0}' in pattern and '{1}' not in pattern:
            if 'fix' in pattern:
                return pattern.format(random.choice(common_verbs))
            elif 'in' in pattern:
                return pattern.format(random.choice(common_nouns), random.choice(common_places))
            else:
                return pattern.format(random.choice(common_nouns))
        elif '{0}' in pattern and '{1}' in pattern:
            return pattern.format(random.choice(common_nouns), random.choice(common_nouns))
        
        return pattern
    
    def _generate_chrome_ua_string(self) -> str:
        """生成真实的Chrome UA字符串"""
        versions = ['Chromium', 'Google Chrome', 'Not;A Brand']
        version_numbers = [f'{random.randint(100, 120)}.0.{random.randint(0, 9999)}.{random.randint(0, 99)}']
        return ", ".join([f"{v} {version_numbers[0]}" for v in versions])
    
    def _generate_platform_string(self) -> str:
        """生成平台字符串"""
        platforms = ['Windows', 'macOS', 'Linux']
        return random.choice(platforms)

    def generate_request_chain(self, target_url: str) -> List[str]:
        """生成请求链，先访问几个无关资源再访问目标URL，增强版
        
        Args:
            target_url: 目标URL
            
        Returns:
            请求链URL列表
        """
        if global_config.get('behavior_simulation.enable_request_chain_pollution', True):
            pollution_resources = global_config.get('behavior_simulation.pollution_resources', [])
            
            # 扩展污染资源列表，分为不同类型
            tracking_scripts = [
                'https://www.google-analytics.com/analytics.js',
                'https://connect.facebook.net/en_US/fbevents.js',
                'https://www.googletagmanager.com/gtag/js',
                'https://analytics.twitter.com/i/adsct',
                'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js',
                'https://bat.bing.com/bat.js',
                'https://static.cloudflareinsights.com/beacon.min.js',
                'https://cdn.amplitude.com/libs/amplitude-7.3.0-min.gz.js'
            ]
            
            css_resources = [
                'https://fonts.googleapis.com/css?family=Roboto',
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css',
                'https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css',
                'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
                'https://cdn.jsdelivr.net/npm/antd@4.24.8/dist/antd.min.css'
            ]
            
            js_resources = [
                'https://code.jquery.com/jquery-3.6.0.min.js',
                'https://cdn.jsdelivr.net/npm/vue@2.6.14/dist/vue.min.js',
                'https://cdn.jsdelivr.net/npm/react@17/umd/react.production.min.js',
                'https://cdn.jsdelivr.net/npm/react-dom@17/umd/react-dom.production.min.js',
                'https://cdn.jsdelivr.net/npm/axios@0.27.2/dist/axios.min.js',
                'https://cdn.jsdelivr.net/npm/lodash@4.17.21/lodash.min.js',
                'https://cdn.jsdelivr.net/npm/moment@2.29.3/moment.min.js'
            ]
            
            other_resources = [
                'https://www.youtube.com/iframe_api',
                'https://www.google.com/recaptcha/api.js',
                'https://cdn.jsdelivr.net/npm/socket.io-client@4.5.0/dist/socket.io.min.js',
                'https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js'
            ]
            
            # 合并所有资源
            all_resources = list(set(pollution_resources + tracking_scripts + css_resources + js_resources + other_resources))
            
            # 智能选择资源，确保多样性
            selected_count = random.randint(1, 3)  # 保持1-3个资源
            
            # 从不同类型中选择资源
            selected_resources = []
            resource_groups = [tracking_scripts, css_resources, js_resources, other_resources]
            
            for _ in range(selected_count):
                group = random.choice(resource_groups)
                if group and len(selected_resources) < selected_count:
                    selected = random.choice(group)
                    if selected not in selected_resources:
                        selected_resources.append(selected)
            
            # 如果资源不足，从所有资源中补充
            if len(selected_resources) < selected_count:
                remaining = [r for r in all_resources if r not in selected_resources]
                if remaining:
                    selected_resources.extend(random.sample(remaining, min(selected_count - len(selected_resources), len(remaining))))
            
            # 构建完整的请求链
            request_chain = []
            
            # 可选：添加一个搜索引擎页面作为起始点
            if random.random() < 0.6:  # 提高概率到60%
                search_engines = [
                    'https://www.google.com/',
                    'https://www.bing.com/',
                    'https://www.baidu.com/',
                    'https://duckduckgo.com/',
                    'https://yandex.com/',
                    'https://www.ecosia.org/'
                ]
                search_engine = random.choice(search_engines)
                
                # 为搜索引擎添加搜索参数
                if search_engine in ['https://www.google.com/', 'https://www.bing.com/', 'https://www.baidu.com/']:
                    query = self._generate_realistic_search_query()
                    if 'google.com' in search_engine:
                        search_engine = f"{search_engine}search?q={query}"
                    elif 'bing.com' in search_engine:
                        search_engine = f"{search_engine}search?q={query}"
                    elif 'baidu.com' in search_engine:
                        search_engine = f"{search_engine}s?wd={query}"
                
                request_chain.append(search_engine)
            
            # 添加污染资源
            request_chain.extend(selected_resources)
            
            # 添加目标URL作为链的最后一步
            request_chain.append(target_url)
            
            return request_chain
        return [target_url]
    
    def generate_request_signature(self) -> Dict[str, str]:
        """生成请求签名，模拟真实API请求的签名机制
        
        Returns:
            包含签名相关参数的字典
        """
        import time
        import hashlib
        import uuid
        
        # 生成时间戳
        timestamp = int(time.time() * 1000)
        
        # 生成随机nonce值
        nonce = str(uuid.uuid4())[:16]
        
        # 生成签名
        signature_data = f"{timestamp}{nonce}"
        signature = hashlib.md5(signature_data.encode()).hexdigest()
        
        return {
            'timestamp': str(timestamp),
            'nonce': nonce,
            'signature': signature
        }
    
    def is_captcha_url(self, url: str) -> bool:
        """根据URL检测是否为验证码页面
        
        Args:
            url: 要检测的URL
            
        Returns:
            是否为验证码URL
        """
        # 验证码URL常见模式
        captcha_url_patterns = [
            'captcha', 'verify', 'robot', 'security', 'recaptcha', 'hcaptcha',
            'distil', 'challenge', 'validation', 'auth', 'login', 'verification',
            'check', 'human', 'antibot', 'spam', 'robot', 'automated'
        ]
        
        url_lower = url.lower()
        for pattern in captcha_url_patterns:
            if pattern in url_lower:
                return True
        
        return False
    
    def is_captcha_page(self, content: str) -> bool:
        """检测页面是否包含验证码，增强版检测算法
        
        Args:
            content: 页面内容
            
        Returns:
            是否为验证码页面
        """
        # 1. 关键词检测
        captcha_keywords = [
            # 英文关键词
            'captcha', 'robot', 'automated', 'bot', 'security check',
            'recaptcha', 'hcaptcha', 'distil', 'please verify', 'prove you are human',
            'verify your humanity', 'human verification', 'suspicious activity',
            'unusual traffic', 'access denied', 'automation', 'spam protection',
            'anti-robot', 'not a robot', 'check box', 'select images', 'click all images',
            'complete the challenge', 'verify you are human', 'solve this puzzle',
            
            # 中文关键词
            '验证码', '人机验证', '请证明您不是机器人', '安全验证', '验证',
            '请点击验证', '滑动验证', '图形验证', '智能验证', '防爬虫',
            '访问受限', '异常访问', '可疑活动', '请完成验证', '拼图验证',
            '点选验证', '旋转验证', '拖拽验证', '请选择所有', '请滑动到右侧'
        ]
        
        content_lower = content.lower()
        for keyword in captcha_keywords:
            if keyword.lower() in content_lower:
                return True
        
        # 2. 验证码服务URL检测
        captcha_scripts = [
            'google.com/recaptcha', 'hcaptcha.com', 'cloudflare.com/turnstile',
            'distilnetworks.com', 'perimeterx.com', 'arkose.com',
            'cloudflare.com/v/challenge', 'geetest.com', 'yundama.com',
            'tencentcloud.com/captcha', 'baidu.com/anticrawler',
            'bing.com/sa/simg/hpcaptcha'
        ]
        
        for script in captcha_scripts:
            if script in content:
                return True
        
        # 3. HTML结构特征检测
        captcha_html_patterns = [
            'class="captcha', 'id="captcha', 'class="g-recaptcha',
            'id="g-recaptcha', 'class="h-captcha', 'id="h-captcha',
            'class="checkbox-recaptcha', 'class="captcha-container',
            'class="verification-code', 'id="verification-code',
            'name="captcha', 'data-sitekey="', 'data-captcha="',
            'captcha-image', 'captcha_input', 'verify-button',
            'slide-verify', 'drag-to-verify', 'rotate-to-verify',
            'puzzle-verify', 'click-verify', 'select-verify'
        ]
        
        for pattern in captcha_html_patterns:
            if pattern.lower() in content_lower:
                return True
        
        # 4. JavaScript函数名检测
        captcha_js_functions = [
            'grecaptcha.execute', 'grecaptcha.render', 'hcaptcha.execute',
            'hcaptcha.render', 'validateCaptcha', 'checkCaptcha',
            'verifyCaptcha', 'submitCaptcha', 'refreshCaptcha',
            'loadCaptcha', 'initCaptcha', 'validateUser',
            'checkHuman', 'verifyHumanity', 'solveChallenge',
            'startCaptcha', 'completeCaptcha', 'submitVerification'
        ]
        
        for func in captcha_js_functions:
            if func in content:
                return True
        
        # 5. 特征组合检测 - 验证码页面通常有特定组合
        if ('<input' in content and 
            'type="text"' in content and 
            ('captcha' in content_lower or 'verify' in content_lower) and 
            ('image' in content_lower or 'button' in content_lower)):
            return True
        
        # 6. 检查表单提交事件中的验证逻辑
        if ('form' in content_lower and 
            ('submit' in content_lower or 'onsubmit' in content_lower) and 
            ('captcha' in content_lower or 'verify' in content_lower)):
            return True
        
        return False
    
    def get_canvas_fingerprint_confusion_script(self) -> str:
        """获取Canvas指纹混淆脚本
        
        Returns:
            JavaScript代码字符串，用于混淆Canvas指纹
        """
        # Canvas指纹混淆数据
        canvas_noise_patterns = [
            'var noise = function() { return Math.random() * 0.01 - 0.005; };',
            'var noise = function() { return Math.sin(Date.now() * 0.001) * 0.003; };',
            'var noise = function() { return Math.cos(Date.now() * 0.0001) * 0.002; };'
        ]
        
        return f"""
            // Canvas指纹混淆
            (function() {{
                {random.choice(canvas_noise_patterns)}
                
                // 保存原始方法
                const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
                const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
                
                // 重写getImageData方法，添加噪声
                CanvasRenderingContext2D.prototype.getImageData = function(x, y, width, height) {{
                    const imageData = originalGetImageData.apply(this, arguments);
                    const data = imageData.data;
                    
                    // 为每个像素添加随机噪声
                    for (let i = 0; i < data.length; i += 4) {{
                        data[i] = Math.min(255, Math.max(0, data[i] + noise() * 255));
                        data[i+1] = Math.min(255, Math.max(0, data[i+1] + noise() * 255));
                        data[i+2] = Math.min(255, Math.max(0, data[i+2] + noise() * 255));
                    }}
                    
                    return imageData;
                }};
                
                // 重写toDataURL方法，添加噪声
                HTMLCanvasElement.prototype.toDataURL = function(type, quality) {{
                    // 添加一些随机变换
                    const ctx = this.getContext('2d');
                    const originalTransform = ctx.getTransform();
                    
                    // 应用微小的随机变换
                    ctx.translate(noise(), noise());
                    ctx.rotate(noise() * 0.01);
                    
                    const result = originalToDataURL.apply(this, arguments);
                    
                    // 恢复原始变换
                    ctx.setTransform(originalTransform);
                    
                    return result;
                }};
            }})();
        """
    
    def get_anti_detection_script(self, level: str = 'basic') -> str:
        """获取反检测脚本，根据安全级别返回不同强度的脚本
        
        Args:
            level: 安全级别 ('basic', 'advanced', 'maximum')
            
        Returns:
            JavaScript代码字符串，用于反检测
        """
        if level == 'maximum':
            return """
            // 最高级别的反检测脚本
            (function() {
                // 禁用所有常见的自动化检测
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(window, 'callPhantom', { get: () => undefined });
                Object.defineProperty(window, 'phantom', { get: () => undefined });
                Object.defineProperty(window, '__nightmare', { get: () => undefined });
                Object.defineProperty(document, 'doctype', { get: () => null });
                Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                
                // 伪造设备信息
                Object.defineProperty(navigator, 'platform', { value: 'Win32' });
                Object.defineProperty(navigator, 'productSub', { value: '20030107' });
                Object.defineProperty(window, 'chrome', { value: { runtime: {} } });
                Object.defineProperty(navigator, 'deviceMemory', { value: 8 });
                Object.defineProperty(navigator, 'hardwareConcurrency', { value: 8 });
                
                // 重写Date API以避免时间差异检测
                const originalNow = Date.now;
                const originalDate = Date;
                window.Date = function(...args) {
                    return new originalDate(...args);
                };
                window.Date.now = function() {
                    return originalNow() + Math.random() * 100;
                };
                
                // 模拟真实的window属性
                const originalOpen = window.open;
                window.open = function(...args) {
                    try {
                        return originalOpen.apply(this, args);
                    } catch (e) {
                        return null;
                    }
                };
                
                // 模拟真实的性能指标
                const originalPerformance = window.performance;
                if (originalPerformance) {
                    Object.defineProperty(window, 'performance', {
                        configurable: false,
                        enumerable: true,
                        writable: false,
                        value: {
                            ...originalPerformance,
                            now: function() {
                                return originalPerformance.now() + Math.random() * 50 - 25;
                            },
                            timing: {
                                ...originalPerformance.timing,
                                navigationStart: originalPerformance.timing.navigationStart + Math.random() * 1000
                            }
                        }
                    });
                }
                
                // 模拟真实的document对象
                const originalQuerySelector = document.querySelector;
                document.querySelector = function(selector) {
                    const result = originalQuerySelector.apply(this, arguments);
                    // 随机延迟返回结果，模拟真实浏览器行为
                    if (Math.random() < 0.2) {
                        return result;
                    }
                    return result;
                };
                
                // 伪造plugins
                Object.defineProperty(navigator, 'plugins', {
                    get: function() {
                        return { length: 3 };
                    }
                });
                
                // 伪造mimeTypes
                Object.defineProperty(navigator, 'mimeTypes', {
                    get: function() {
                        return { length: 5 };
                    }
                });
                
                // 检测并混淆自动化特征
                const isHeadless = navigator.userAgent.includes('HeadlessChrome');
                if (isHeadless) {
                    Object.defineProperty(navigator, 'userAgent', {
                        get: function() {
                            return navigator.userAgent.replace('HeadlessChrome', 'Chrome');
                        }
                    });
                }
                
                // 模拟真实的window大小变化
                let resizeTimeout;
                window.addEventListener('resize', function() {
                    clearTimeout(resizeTimeout);
                    resizeTimeout = setTimeout(() => {}, 100);
                });
                
                // 混淆事件处理
                const originalAddEventListener = EventTarget.prototype.addEventListener;
                EventTarget.prototype.addEventListener = function(type, listener, options) {
                    // 不处理某些可能用于检测的事件
                    const detectionEvents = ['blur', 'focus', 'mousemove'];
                    if (detectionEvents.includes(type) && Math.random() < 0.05) {
                        return;
                    }
                    return originalAddEventListener.apply(this, arguments);
                };
            })();
            """
        elif level == 'advanced':
            return """
            // 高级反检测脚本
            (function() {
                // 禁用常见的自动化检测
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(window, 'callPhantom', { get: () => undefined });
                Object.defineProperty(window, 'phantom', { get: () => undefined });
                Object.defineProperty(window, '__nightmare', { get: () => undefined });
                Object.defineProperty(document, 'doctype', { get: () => null });
                Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                
                // 伪造设备信息
                Object.defineProperty(navigator, 'platform', { value: 'Win32' });
                Object.defineProperty(navigator, 'productSub', { value: '20030107' });
                Object.defineProperty(window, 'chrome', { value: { runtime: {} } });
                Object.defineProperty(navigator, 'deviceMemory', { value: 8 });
                Object.defineProperty(navigator, 'hardwareConcurrency', { value: 8 });
                
                // 重写Date API以避免时间差异检测
                const originalNow = Date.now;
                const originalDate = Date;
                window.Date = function(...args) {
                    return new originalDate(...args);
                };
                window.Date.now = function() {
                    return originalNow() + Math.random() * 50;
                };
                
                // 模拟真实的window属性
                const originalOpen = window.open;
                window.open = function(...args) {
                    try {
                        return originalOpen.apply(this, args);
                    } catch (e) {
                        return null;
                    }
                };
                
                // 检测并混淆自动化特征
                const isHeadless = navigator.userAgent.includes('HeadlessChrome');
                if (isHeadless) {
                    Object.defineProperty(navigator, 'userAgent', {
                        get: function() {
                            return navigator.userAgent.replace('HeadlessChrome', 'Chrome');
                        }
                    });
                }
            })();
            """
        else:  # basic
            return """
            // 基础反检测脚本
            (function() {
                // 禁用常见的自动化检测
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(window, 'callPhantom', { get: () => undefined });
                Object.defineProperty(window, 'phantom', { get: () => undefined });
                Object.defineProperty(window, '__nightmare', { get: () => undefined });
                Object.defineProperty(document, 'doctype', { get: () => null });
                Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                
                // 伪造设备信息
                Object.defineProperty(navigator, 'platform', { value: 'Win32' });
                Object.defineProperty(navigator, 'productSub', { value: '20030107' });
                Object.defineProperty(window, 'chrome', { value: { runtime: {} } });
            })();
            """
            
    def get_webgl_fingerprint_confusion_script(self) -> str:
        """获取WebGL指纹混淆脚本
        
        Returns:
            JavaScript代码字符串，用于混淆WebGL指纹
        """
        return f"""
            // WebGL指纹混淆
            (function() {{
                // 保存原始方法
                const originalGetParameter = WebGLRenderingContext.prototype.getParameter;
                
                // 重写getParameter方法，修改返回值
                WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                    // 修改一些常用的指纹参数
                    const paramName = parameter.toString();
                    
                    // 重写渲染器信息
                    if (parameter === 37445) {{ // GL_RENDERER
                        return "WebKit WebGL" + (Math.random() > 0.5 ? " 1.0" : " 2.0");
                    }}
                    
                    // 重写供应商信息
                    if (parameter === 37446) {{ // GL_VENDOR
                        return ["WebKit", "Google Inc.", "Mozilla", "Intel Inc.", "NVIDIA Corporation"][Math.floor(Math.random() * 5)];
                    }}
                    
                    // 重写版本信息
                    if (parameter === 7938) {{ // GL_VERSION
                        return "WebGL " + (Math.random() > 0.5 ? "1.0" : "2.0");
                    }}
                    
                    // 重写着色器精度
                    if (parameter === 35724) {{ // GL_MAX_VERTEX_TEXTURE_IMAGE_UNITS
                        return Math.floor(Math.random() * 8) + 8;
                    }}
                    
                    // 重写纹理大小
                    if (parameter === 3379) {{ // GL_MAX_TEXTURE_SIZE
                        return [2048, 4096, 8192][Math.floor(Math.random() * 3)];
                    }}
                    
                    // 其他参数保持不变
                    return originalGetParameter.apply(this, arguments);
                }};
                
                // 同样处理WebGL2
                if (window.WebGL2RenderingContext) {{
                    const originalGetParameter2 = WebGL2RenderingContext.prototype.getParameter;
                    WebGL2RenderingContext.prototype.getParameter = function(parameter) {{
                        // 复用上面的逻辑
                        return WebGLRenderingContext.prototype.getParameter.apply(this, arguments);
                    }};
                }}
            }})();
        """