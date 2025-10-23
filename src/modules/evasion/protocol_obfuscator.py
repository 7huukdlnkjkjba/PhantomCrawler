# PhantomCrawler - 协议级混淆模块
import random
import socket
import ssl
import time
from typing import List, Dict, Optional, Any
import httpx
import socks
from src.config import global_config

class ProtocolObfuscator:
    """实现协议级混淆和代理链功能"""
    
    def __init__(self):
        # 代理链配置
        self.proxy_chain = global_config.get('proxy_chain', [])
        self.current_proxy_index = 0
        
        # WebSocket配置
        self.websocket_enabled = False
        self.websocket_endpoint = None
    
    def get_next_proxy(self) -> Optional[Dict[str, str]]:
        """获取代理链中的下一个代理"""
        if not self.proxy_chain:
            return None
        
        # 轮询选择代理
        proxy = self.proxy_chain[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxy_chain)
        return proxy
    
    def build_proxy_chain(self, proxies: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """构建代理链，确保不同类型的代理正确排序"""
        # 分离不同类型的代理
        http_proxies = [p for p in proxies if p.get('type') == 'http']
        socks5_proxies = [p for p in proxies if p.get('type') == 'socks5']
        
        # 推荐的代理链顺序：HTTP -> SOCKS5 -> HTTP
        # 这样可以最大化混淆流量来源
        proxy_chain = []
        
        if http_proxies:
            proxy_chain.append(random.choice(http_proxies))
        
        if socks5_proxies:
            # 可以添加多个SOCKS5代理
            num_socks5 = random.randint(1, min(2, len(socks5_proxies)))
            for _ in range(num_socks5):
                proxy = random.choice(socks5_proxies)
                proxy_chain.append(proxy)
                socks5_proxies.remove(proxy)  # 避免重复
        
        if http_proxies and len(proxy_chain) > 0:
            # 如果已经有代理，再添加一个HTTP代理作为出口
            last_proxy = random.choice(http_proxies)
            if last_proxy != proxy_chain[0]:  # 避免和第一个代理重复
                proxy_chain.append(last_proxy)
        
        return proxy_chain
    
    def create_proxied_httpx_client(self) -> httpx.Client:
        """创建配置了代理链的httpx客户端"""
        client_kwargs = {}
        
        # 设置超时
        client_kwargs['timeout'] = httpx.Timeout(global_config.get('request_timeout', 30.0))
        
        # 只有在有代理链时才添加代理配置
        if self.proxy_chain:
            # 获取下一个代理
            proxy = self.get_next_proxy()
            
            # 构建代理URL
            if proxy and proxy.get('type') == 'http':
                proxy_url = f"http://{proxy.get('host')}:{proxy.get('port')}"
                if proxy.get('username') and proxy.get('password'):
                    proxy_url = f"http://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"
            elif proxy and proxy.get('type') == 'socks5':
                proxy_url = f"socks5://{proxy.get('host')}:{proxy.get('port')}"
                if proxy.get('username') and proxy.get('password'):
                    proxy_url = f"socks5://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"
            else:
                proxy_url = None
            
            if proxy_url:
                client_kwargs['proxies'] = {
                    "http://": proxy_url,
                    "https://": proxy_url,
                }
        
        # 创建客户端
        client = httpx.Client(**client_kwargs)
        
        # 添加请求前的钩子，用于进一步混淆
        client.event_hooks['request'] = [self._request_hook]
        
        return client
    
    def _request_hook(self, request: httpx.Request) -> None:
        """请求前的钩子，用于添加额外的混淆"""
        # 随机添加一些无害的头部来混淆指纹
        obfuscation_headers = {
            'X-Requested-With': random.choice(['XMLHttpRequest', ''],),
            'X-Forwarded-For': self._generate_spoofed_ip(),
            'Accept-CH': random.choice(['Sec-CH-UA, Sec-CH-UA-Mobile, Sec-CH-UA-Platform', ''],),
        }
        
        # 只添加一部分头部，增加随机性
        headers_to_add = random.sample(list(obfuscation_headers.items()), 
                                      k=random.randint(0, len(obfuscation_headers)))
        
        for header, value in headers_to_add:
            if value:
                request.headers[header] = value
    
    def _generate_spoofed_ip(self) -> str:
        """生成伪造的IP地址"""
        # 生成看起来真实的IP地址，但避免使用私有IP范围
        first_octet = random.choice([x for x in range(1, 224) if x not in [10, 127, 172, 192]])
        if first_octet == 172:
            second_octet = random.choice([x for x in range(0, 256) if x not in range(16, 32)])
        elif first_octet == 192:
            second_octet = random.choice([x for x in range(0, 256) if x != 168])
        else:
            second_octet = random.randint(0, 255)
        
        return f"{first_octet}.{second_octet}.{random.randint(0, 255)}.{random.randint(0, 255)}"
    
    def setup_websocket_channel(self, endpoint: str) -> bool:
        """设置WebSocket通道用于HTTP请求伪装"""
        self.websocket_endpoint = endpoint
        self.websocket_enabled = True
        # 在实际实现中，这里应该建立WebSocket连接
        return True
    
    def send_via_websocket(self, http_request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """通过WebSocket发送HTTP请求（实验性功能）"""
        if not self.websocket_enabled or not self.websocket_endpoint:
            return None
        
        # 这里是简化实现，实际需要使用websocket库建立连接并发送数据
        # 1. 将HTTP请求序列化为JSON
        # 2. 通过WebSocket发送
        # 3. 等待并解析响应
        
        # 模拟WebSocket通信
        print(f"[实验性功能] 通过WebSocket发送HTTP请求到 {http_request.get('url')}")
        
        # 在实际实现中，这里应该有真实的WebSocket通信代码
        # 为了演示，我们返回None
        return None
    
    def create_socks_proxy_connection(self, proxy: Dict[str, str], target_host: str, target_port: int) -> socket.socket:
        """创建通过SOCKS代理的TCP连接"""
        # 创建SOCKS5连接
        sock = socks.socksocket()
        sock.set_proxy(
            proxy_type=socks.SOCKS5,
            addr=proxy.get('host'),
            port=proxy.get('port'),
            username=proxy.get('username'),
            password=proxy.get('password')
        )
        
        # 连接到目标
        sock.connect((target_host, target_port))
        return sock
    
    def create_ssl_wrapped_socket(self, sock: socket.socket, hostname: str) -> ssl.SSLSocket:
        """创建SSL包装的socket，用于TLS指纹模拟"""
        # 创建SSL上下文
        context = ssl.create_default_context()
        
        # 配置TLS参数以模拟浏览器
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.set_ciphers('ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256')
        
        # 包装socket
        ssl_sock = context.wrap_socket(sock, server_hostname=hostname)
        return ssl_sock
    
    def rotate_proxy_chain(self) -> None:
        """旋转代理链，改变使用顺序"""
        if self.proxy_chain:
            random.shuffle(self.proxy_chain)
    
    def force_proxy_change(self) -> Optional[Dict[str, str]]:
        """强制更换到下一个代理
        
        Returns:
            新的代理配置，如果没有代理则返回None
        """
        return self.get_next_proxy()
    
    def rotate_proxy(self) -> None:
        """旋转代理，强制切换到下一个代理并重新排序代理链"""
        self.rotate_proxy_chain()
        if self.proxy_chain:
            self.current_proxy_index = 0  # 重置到第一个代理
    
    def test_proxy(self, proxy: Dict[str, str]) -> bool:
        """测试代理是否有效"""
        try:
            if proxy.get('type') == 'http':
                proxy_url = f"http://{proxy.get('host')}:{proxy.get('port')}"
                if proxy.get('username') and proxy.get('password'):
                    proxy_url = f"http://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"
                
                with httpx.Client(proxies={'http://': proxy_url, 'https://': proxy_url}, timeout=10) as client:
                    response = client.get('http://httpbin.org/ip', timeout=10)
                    return response.status_code == 200
            
            elif proxy.get('type') == 'socks5':
                # 测试SOCKS5代理
                sock = socks.socksocket()
                sock.set_proxy(
                    proxy_type=socks.SOCKS5,
                    addr=proxy.get('host'),
                    port=proxy.get('port'),
                    username=proxy.get('username'),
                    password=proxy.get('password')
                )
                sock.settimeout(10)
                sock.connect(('httpbin.org', 80))
                sock.close()
                return True
            
        except Exception:
            pass
        
        return False