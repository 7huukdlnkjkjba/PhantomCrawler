# PhantomCrawler - 七宗欲核心引擎 | 实战突破版
import asyncio
import random
import time
from typing import Dict, List, Optional, Any, Callable
import httpx
from src.modules.evasion.fingerprint_spoofer import FingerprintSpoofer
from src.modules.behavior.behavior_simulator import BehaviorSimulator
from src.modules.evasion.protocol_obfuscator import ProtocolObfuscator
from src.config import global_config

class PhantomCrawler:
    """PhantomCrawler核心引擎类，整合所有功能模块"""
    
    def __init__(self, config_file: Optional[str] = None):
        # 初始化配置
        if config_file:
            from src.configs.config import Config
            Config(config_file)  # 这将更新全局配置
        
        # 初始化核心模块
        self.fingerprint_spoofer = FingerprintSpoofer()
        self.behavior_simulator = BehaviorSimulator()
        self.protocol_obfuscator = ProtocolObfuscator()
        
        # 七宗欲引擎实例
        self.seven_desires = self.behavior_simulator.seven_desires
        
        # 爬虫状态
        self.is_running = False
        self.session_id = self._generate_session_id()
        self.crawl_history = []
        self.success_streak = 0
        self.total_attempts = 0
        self.consecutive_failures = 0
        
        # 当前策略（实战版）
        self.current_strategies = {
            'fingerprint': {'advanced': False, 'rotation_interval': 0},
            'delay': 2.0,
            'request_chain': [],
            'playwright_strategy': 'normal',  # normal, stealth, aggressive
            'evasion_level': 0,  # 0-3，反检测等级
            'risk_adjusted': False
        }
        
        print(f"[七宗欲爬虫] 初始化完成，当前主导欲望: {self.seven_desires.dominant_desire}")
        
        # 客户端实例
        self.http_client = None
        self.playwright_browser = None
        
        # 学习状态
        self.previous_state = None
        self.previous_action = None
    
    def _generate_session_id(self) -> str:
        """生成唯一的会话ID"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def initialize(self) -> bool:
        """初始化爬虫"""
        try:
            # 初始化HTTP客户端
            self.http_client = self._create_http_client()
            
            self.is_running = True
            print(f"[PhantomCrawler] 初始化成功，会话ID: {self.session_id}")
            return True
        except Exception as e:
            print(f"[PhantomCrawler] 初始化失败: {str(e)}")
            return False
    
    def _create_http_client(self) -> httpx.Client:
        """创建配置好的HTTP客户端"""
        # 生成浏览器指纹
        headers = self.fingerprint_spoofer.generate_fingerprint()
        
        # 创建代理客户端
        client = self.protocol_obfuscator.create_proxied_httpx_client()
        
        # 应用指纹
        client = self.fingerprint_spoofer.configure_httpx_client(client)
        client.headers.update(headers)
        
        return client
    
    def crawl(self, url: str, callback: Optional[Callable] = None, _playwright_attempted: bool = False) -> Dict[str, Any]:
        """执行智能爬取任务，集成七宗欲引擎优化"""
        if not self.is_running:
            self.initialize()
        
        # 记录开始时间
        start_time = time.time()
        self.total_attempts += 1
        
        try:
            # 获取目标风险评估
            risk_level = self.seven_desires.desire_perception['detection_danger']
            dominant_desire = self.seven_desires.dominant_desire
            
            print(f"[七宗欲爬虫] 开始爬取 {url} - 风险等级: {risk_level:.2f} - 主导欲望: {dominant_desire}")
            
            # 基于七宗欲生成实战策略
            self._generate_desire_based_strategy(url)
            
            # 应用策略
            self._apply_strategies(self.current_strategies)
            
            # 根据风险等级决定是否直接使用playwright
            if risk_level > 0.6:
                print(f"[七宗欲爬虫] 风险过高，直接启动高级浏览器模拟")
                return self._crawl_with_playwright(url, callback)
            
            # 生成经过优化的请求链
            request_chain = self._generate_optimized_request_chain(url)
            
            # 执行请求链中的每个请求
            for i, chain_url in enumerate(request_chain):
                print(f"[七宗欲爬虫] 执行请求链 {i+1}/{len(request_chain)}: {chain_url} - 欲望模式: {dominant_desire}")
                
                # 非目标URL的请求（污染资源）
                if chain_url != url:
                    try:
                        # 根据当前欲望调整延迟
                        desire_delay = self._get_desire_adjusted_delay()
                        time.sleep(desire_delay)
                        
                        # 根据风险等级调整请求头
                        headers = self._get_risk_adjusted_headers()
                        self.http_client.get(chain_url, timeout=5, follow_redirects=True, headers=headers)
                    except Exception as e:
                        print(f"[七宗欲爬虫] 污染资源请求失败: {str(e)} - 继续执行")
                else:
                    # 目标URL请求
                    try:
                        # 应用七宗欲优化的请求执行
                        response = self._execute_main_request_with_desire(chain_url)
                        
                        # 计算响应时间
                        response_time = time.time() - start_time
                        
                        # 准备结果数据
                        result = {
                            'url': url,
                            'status_code': response.status_code,
                            'content': response.text,
                            'headers': dict(response.headers),
                            'cookies': dict(response.cookies),
                            'response_time': response_time,
                            'blocked': self._is_blocked(response)
                        }
                        
                        # 调用回调函数
                        if callback:
                            callback(response)
                        
                        # 记录历史
                        self.crawl_history.append({
                            'url': url,
                            'status_code': response.status_code,
                            'timestamp': time.time(),
                            'session_id': self.session_id,
                            'blocked': result['blocked'],
                            'response_time': response_time
                        })
                        
                        # 执行七宗欲分析
                        self._seven_desires_analysis(url, result, response_time, success=True)
                        
                        # 更新环境感知
                        self.behavior_simulator._update_environment_awareness(result)
                        
                        # 更新连续成功记录
                        self.success_streak += 1
                        self.consecutive_failures = 0
                        
                        if self.success_streak >= 3:
                            print(f"[七宗欲爬虫] 连续成功{self.success_streak}次！{dominant_desire}欲望强化中...")
                        
                        return result
                        
                    except Exception as e:
                        error_msg = str(e)
                        print(f"[七宗欲爬虫] 主请求失败: {error_msg}")
                        # 记录失败并执行欲望分析
                        self.consecutive_failures += 1
                        self.success_streak = 0
                        
                        # 执行七宗欲失败分析
                        self._seven_desires_analysis(url, {'error': error_msg}, time.time() - start_time, success=False)
                        
                        # 根据连续失败次数调整策略
                        error_str = str(error_msg).lower() if error_msg else ''
                        if self.consecutive_failures >= 2 or any(kw in error_str for kw in ['blocked', 'captcha', '403', '429']):
                            print(f"[七宗欲爬虫] 触发备用策略 - 连续失败{self.consecutive_failures}次")
                            if not _playwright_attempted:
                                return self._crawl_with_playwright(url, callback)
                            else:
                                print("[七宗欲爬虫] Playwright已尝试过，不再重试以避免递归")
                        raise
        
        except Exception as e:
            print(f"[七宗欲爬虫] 爬取失败: {str(e)}")
            # 记录失败并执行欲望分析
            self.consecutive_failures += 1
            self.success_streak = 0
            self._seven_desires_analysis(url, {'error': str(e)}, time.time() - start_time, success=False)
            
            # 尝试使用Playwright作为备用方案
            strategy = 'aggressive' if hasattr(self.seven_desires, 'dominant_desire') and self.seven_desires.dominant_desire == '愤怒' else 'stealth'
            if not _playwright_attempted:
                return self._crawl_with_playwright(url, callback)
            else:
                print("[七宗欲爬虫] Playwright已尝试过，不再重试以避免递归")
                raise
    
    def _execute_main_request(self, url: str) -> httpx.Response:
        """执行智能主请求，集成元认知系统的风险评估和策略调整"""
        max_retries = global_config.get('max_retries', 3)
        retry_count = 0
        last_referrer = None
        
        # 获取当前风险评估
        risk_level = self.seven_desires.environment_awareness.get('detection_risk', 0)
        
        # 根据风险级别调整重试策略
        if risk_level > 0.7:
            # 高风险时增加重试间隔
            max_retries = min(5, max_retries + 2)
            print(f"[PhantomCrawler] 检测到高风险环境，增加重试次数至 {max_retries}")
        
        while retry_count < max_retries:
            try:
                # 根据当前行为模式调整请求参数
                pattern = self.behavior_simulator.behavior_pattern
                pattern_params = self.behavior_simulator.pattern_parameters.get(pattern, {})
                
                # 生成动态头部和请求签名
                headers = self.fingerprint_spoofer.generate_dynamic_headers(url, last_referrer)
                
                # 在高风险模式下使用更高级的指纹
                if risk_level > 0.5 or pattern == 'stealth':
                    headers = self.fingerprint_spoofer.generate_advanced_fingerprint(headers)
                
                request_signature = self.fingerprint_spoofer.generate_request_signature()
                
                # 动态调整URL参数的添加概率，基于当前模式
                add_param_probability = 0.6
                if pattern == 'careful' or pattern == 'stealth':
                    add_param_probability = 0.8  # 更频繁地添加参数以模拟真实用户
                elif pattern == 'hurried':
                    add_param_probability = 0.4  # 更少添加参数以加快速度
                
                # 将签名添加到查询参数
                import urllib.parse
                parsed_url = urllib.parse.urlparse(url)
                query_params = urllib.parse.parse_qs(parsed_url.query)
                
                # 随机添加签名参数
                if random.random() < add_param_probability:
                    # 随机选择参数名，避免固定模式
                    param_names = ['_', 't', 'v', 'uid', 'r', 's']
                    param_name = random.choice(param_names)
                    query_params[param_name] = [request_signature['nonce']]
                    
                # 重新构建URL
                new_query = urllib.parse.urlencode(query_params, doseq=True)
                new_url = urllib.parse.urlunparse(
                    (parsed_url.scheme, parsed_url.netloc, parsed_url.path, 
                     parsed_url.params, new_query, parsed_url.fragment)
                )
                
                # 根据模式调整超时时间
                base_timeout = global_config.get('request_timeout', 30)
                timeout_multiplier = 1.0
                if pattern == 'careful' or pattern == 'stealth':
                    timeout_multiplier = 1.5  # 更耐心等待
                elif pattern == 'hurried':
                    timeout_multiplier = 0.8  # 更急于获得响应
                
                adjusted_timeout = base_timeout * timeout_multiplier
                
                # 执行请求前的延迟，基于行为模式
                if retry_count > 0:
                    self.behavior_simulator.human_delay()
                
                # 执行请求
                response = self.http_client.get(
                    new_url,
                    headers=headers,
                    timeout=adjusted_timeout,
                    follow_redirects=True
                )
                
                # 检查是否被阻止
                if self._is_blocked(response):
                    print(f"[PhantomCrawler] 检测到可能被阻止，尝试更换策略...")
                    
                    # 记录阻止事件到元认知系统
                    detection_info = {
                        'blocked': True,
                        'status_code': response.status_code,
                        'url': url,
                        'retry_count': retry_count
                    }
                    
                    # 执行元认知自适应调整
                    self._metacognitive_adaptation(url, detection_info)
                    
                    # 根据风险级别调整等待时间
                    wait_time = random.uniform(5, 15)
                    if risk_level > 0.8:
                        wait_time = wait_time * 2  # 高风险时等待更久
                    
                    print(f"[PhantomCrawler] 休眠 {wait_time:.2f} 秒后重试...")
                    time.sleep(wait_time)
                    
                    retry_count += 1
                    last_referrer = None  # 重置referrer
                    continue
                
                # 记录最后一个有效的referrer
                last_referrer = url
                
                # 更新成功连续次数
                self.success_streak += 1
                
                # 低风险且多次成功后，可以适当加快速度
                if risk_level < 0.3 and self.success_streak > 5 and pattern == 'careful':
                    if random.random() < 0.3:  # 30%概率切换到更快的模式
                        print(f"[PhantomCrawler] 连续成功，考虑加快爬取速度")
                        self.behavior_simulator.shift_behavior_pattern()
                
                return response
                
            except Exception as e:
                error_msg = str(e)
                print(f"[PhantomCrawler] 请求失败: {error_msg}")
                
                # 根据错误类型调整策略
                error_str = str(error_msg).lower() if error_msg else ''
                if 'timeout' in error_str:
                    self._adjust_strategy_based_on_error('timeout')
                elif 'connection' in error_str:
                    self._adjust_strategy_based_on_error('connection_error')
                
                retry_count += 1
                if retry_count < max_retries:
                    # 重试前更换代理和指纹
                    self._refresh_identity()
                    
                    # 根据风险级别调整等待时间
                    wait_time = random.uniform(2, 5) * retry_count
                    if risk_level > 0.7:
                        wait_time *= 2  # 高风险时等待更久
                    
                    print(f"[PhantomCrawler] 等待 {wait_time:.2f} 秒后重试...")
                    time.sleep(wait_time)
                    
                    last_referrer = None  # 重置referrer
        
        # 达到最大重试次数，记录到元认知系统
        self.seven_desires.record_failure(url, 'max_retries_reached', self.current_strategies)
        raise Exception(f"达到最大重试次数 {max_retries}")
    
    def _is_blocked(self, response: httpx.Response) -> bool:
        """检测是否被目标网站阻止，增强版检测"""
        # 检查状态码
        if response.status_code in [403, 429, 503]:
            return True
        
        # 检查响应内容中的阻止关键词
        blocked_keywords = [
            'captcha', '验证码', 'robot', 'automated', 'blocked', 
            'suspicious', 'unusual activity', 'access denied',
            'security check', '验证', '人机验证', '请证明您不是机器人',
            'recaptcha', 'hcaptcha', 'distil', 'bot detected', 'automation'
        ]
        
        content_lower = response.text.lower()
        
        # 检查关键词
        for keyword in blocked_keywords:
            if keyword in content_lower:
                return True
        
        # 检查响应内容长度（可能返回空页面或极小页面）
        if len(response.text) < 500 and response.status_code == 200:
            # 但要排除API返回
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' not in content_type and 'image/' not in content_type:
                return True
        
        return False
    
    def _handle_blocked(self) -> None:
        """处理被阻止的情况"""
        # 更换代理
        self.protocol_obfuscator.rotate_proxy_chain()
        
        # 刷新指纹
        self._refresh_identity()
        
        # 休眠一段时间
        sleep_time = random.uniform(5, 15)
        print(f"[PhantomCrawler] 休眠 {sleep_time:.2f} 秒后重试...")
        time.sleep(sleep_time)
    
    def _refresh_identity(self):
        """刷新爬虫身份，包括更换指纹和代理"""
        # 更换指纹
        self.fingerprint_spoofer.refresh_fingerprint()
        
        # 更换代理
        self.protocol_obfuscator.rotate_proxy()
        
        # 重新创建HTTP客户端
        self.http_client = self._create_http_client()
        
        print(f"[PhantomCrawler] 身份已刷新")
    
    def _apply_strategies(self, strategies: Dict[str, Any]):
        """应用元认知系统推荐的策略"""
        # 应用指纹策略
        fingerprint_strategy = strategies.get('fingerprint', {})
        if fingerprint_strategy.get('advanced', False):
            global_config.set('fingerprint.enable_advanced_spoofing', True)
        else:
            global_config.set('fingerprint.enable_advanced_spoofing', False)
        
        # 应用延迟策略
        delay_value = strategies.get('delay', 2.0)
        global_config.set('behavior_simulation.min_delay', delay_value * 0.8)
        global_config.set('behavior_simulation.max_delay', delay_value * 1.2)
        
        # 应用代理策略
        proxy_strategy = strategies.get('proxy')
        if proxy_strategy:
            if isinstance(proxy_strategy, list):
                global_config.set('proxy_chain', proxy_strategy)
            else:
                global_config.set('proxy_chain', [proxy_strategy] if proxy_strategy else [])
    
    def _generate_optimized_request_chain(self, url: str) -> List[str]:
        """生成经过元认知优化的请求链"""
        # 获取策略中的请求链
        base_resources = self.current_strategies.get('request_chain', [])
        
        # 结合默认的请求链生成算法
        request_chain = []
        
        # 添加基础资源
        request_chain.extend(base_resources)
        
        # 确保目标URL在最后
        if url not in request_chain:
            request_chain.append(url)
        elif request_chain[-1] != url:
            # 将目标URL移到最后
            request_chain.remove(url)
            request_chain.append(url)
        
        return request_chain
    
    def _generate_desire_based_strategy(self, url: str):
        """基于七宗欲生成实战策略"""
        dominant = self.seven_desires.dominant_desire if hasattr(self.seven_desires, 'dominant_desire') else '贪婪'
        risk = self.seven_desires.desire_perception.get('detection_danger', 0) if hasattr(self.seven_desires, 'desire_perception') else 0
        
        # 根据主导欲望调整策略
        strategies = {
            '傲慢': {
                'fingerprint': {'advanced': True, 'rotation_interval': 0},
                'delay': random.uniform(1.0, 2.0),
                'playwright_strategy': 'normal',
                'evasion_level': 1
            },
            '嫉妒': {
                'fingerprint': {'advanced': True, 'rotation_interval': 5},
                'delay': random.uniform(2.0, 3.5),
                'playwright_strategy': 'stealth',
                'evasion_level': 2
            },
            '愤怒': {
                'fingerprint': {'advanced': True, 'rotation_interval': 2},
                'delay': random.uniform(0.5, 1.5),
                'playwright_strategy': 'aggressive',
                'evasion_level': 3
            },
            '懒惰': {
                'fingerprint': {'advanced': False, 'rotation_interval': 10},
                'delay': random.uniform(3.0, 5.0),
                'playwright_strategy': 'stealth',
                'evasion_level': 1
            },
            '贪婪': {
                'fingerprint': {'advanced': True, 'rotation_interval': 3},
                'delay': random.uniform(1.5, 2.5),
                'playwright_strategy': 'normal',
                'evasion_level': 2
            },
            '暴食': {
                'fingerprint': {'advanced': True, 'rotation_interval': 1},
                'delay': random.uniform(0.8, 1.8),
                'playwright_strategy': 'aggressive',
                'evasion_level': 2
            },
            '色欲': {
                'fingerprint': {'advanced': True, 'rotation_interval': 4},
                'delay': random.uniform(2.5, 4.0),
                'playwright_strategy': 'stealth',
                'evasion_level': 3
            }
        }
        
        # 获取欲望对应的策略
        base_strategy = strategies.get(dominant, strategies['贪婪'])
        
        # 根据风险级别调整
        if risk > 0.7:
            base_strategy['evasion_level'] = 3
            base_strategy['fingerprint']['advanced'] = True
            base_strategy['delay'] = base_strategy['delay'] * 1.5
        elif risk > 0.4:
            base_strategy['evasion_level'] = max(1, base_strategy['evasion_level'])
            base_strategy['delay'] = base_strategy['delay'] * 1.2
        
        # 更新当前策略
        for k, v in base_strategy.items():
            self.current_strategies[k] = v
        
        # 生成请求链
        if hasattr(self, '_generate_optimal_request_chain'):
            self.current_strategies['request_chain'] = self._generate_optimal_request_chain(url)
        self.current_strategies['risk_adjusted'] = True
        
        print(f"[七宗欲爬虫] 已生成{dominant}驱动策略 - 风险等级: {risk:.2f}")
    
    def _get_desire_adjusted_delay(self):
        """根据七宗欲获取调整后的延迟"""
        dominant = self.seven_desires.dominant_desire if hasattr(self.seven_desires, 'dominant_desire') else '贪婪'
        risk = self.seven_desires.desire_perception.get('detection_danger', 0) if hasattr(self.seven_desires, 'desire_perception') else 0
        
        # 基础延迟
        base_delay = self.current_strategies['delay']
        
        # 欲望调整系数
        desire_factors = {
            '傲慢': 0.8,
            '嫉妒': 1.2,
            '愤怒': 0.5,
            '懒惰': 1.5,
            '贪婪': 1.0,
            '暴食': 0.6,
            '色欲': 2.0
        }
        
        factor = desire_factors.get(dominant, 1.0)
        
        # 风险调整
        if risk > 0.7:
            factor *= 1.8
        elif risk > 0.4:
            factor *= 1.3
        
        # 随机波动
        jitter = random.uniform(0.8, 1.2)
        
        return max(0.2, base_delay * factor * jitter)
    
    def _get_risk_adjusted_headers(self):
        """获取基于风险等级调整的请求头"""
        risk = self.seven_desires.desire_perception.get('detection_danger', 0) if hasattr(self.seven_desires, 'desire_perception') else 0
        
        if risk > 0.5:
            # 高风险时生成全新指纹
            return self.fingerprint_spoofer.generate_fingerprint(advanced=True)
        return self.fingerprint_spoofer.generate_fingerprint()
    
    def _execute_main_request_with_desire(self, url: str):
        """执行七宗欲优化的主请求"""
        # 这里复用现有的_execute_main_request方法
        # 但会根据七宗欲进行参数调整
        return self._execute_main_request(url)
    
    def _seven_desires_analysis(self, url: str, result: Dict[str, Any], response_time: float, success: bool):
        """执行七宗欲分析，更新欲望强度和策略"""
        # 使用简单的递归防护 - 跟踪是否正在进行分析
        if hasattr(self, '_analysis_in_progress') and self._analysis_in_progress:
            print(f"[七宗欲爬虫] 递归防护: 分析已在进行中，跳过当前调用")
            return
        
        # 设置分析中标志
        self._analysis_in_progress = True
        
        try:
            # 简化的分析版本，避免复杂的递归调用
            # 只执行最基本的记录操作，避免触发可能导致递归的方法
            
            # 确保result是安全的格式
            safe_result = {}
            if isinstance(result, dict):
                safe_result['error'] = str(result.get('error', 'Unknown error'))
                safe_result['status_code'] = result.get('status_code', 500)
                safe_result['blocked'] = result.get('blocked', False)
            else:
                safe_result['error'] = str(result)
                safe_result['status_code'] = 500
                safe_result['blocked'] = False
            
            # 只记录成功或失败，不执行可能导致递归的其他方法
            if success:
                if hasattr(self.seven_desires, 'record_success'):
                    try:
                        self.seven_desires.record_success(url, safe_result)
                        print(f"[七宗欲爬虫] {url} 爬取成功")
                    except Exception as e:
                        print(f"[七宗欲爬虫] 记录成功时出错: {str(e)}")
            else:
                if hasattr(self.seven_desires, 'record_failure'):
                    try:
                        self.seven_desires.record_failure(url, safe_result)
                        print(f"[七宗欲爬虫] {url} 爬取失败 - 记录已保存")
                    except Exception as e:
                        print(f"[七宗欲爬虫] 记录失败时出错: {str(e)}")
            
            # 避免调用可能导致递归的其他方法
            # 暂时注释掉这些可能导致递归的调用
            # 将来可以逐步添加回来，但需要确保不会递归
            # if hasattr(self.seven_desires, '_sense_danger'):
            #     self.seven_desires._sense_danger(success, safe_result)
            # if hasattr(self.seven_desires, '_awaken_dominant_desire'):
            #     self.seven_desires._awaken_dominant_desire()
            # if hasattr(self.behavior_simulator, '_select_optimized_behavior_pattern'):
            #     self.behavior_simulator._select_optimized_behavior_pattern()
            # if hasattr(self.seven_desires, '_balance_desire_forces'):
            #     self.seven_desires._balance_desire_forces()
                
        except Exception as e:
            print(f"[七宗欲爬虫] 七宗欲分析出错: {str(e)}")
            # 避免在分析错误时再次触发分析，防止递归
        finally:
            # 重置分析中标志，确保方法结束后总是重置
            self._analysis_in_progress = False
    
    def _metacognitive_analysis(self, url: str, result: Dict[str, Any], response_time: float):
        """保持向后兼容的元认知分析方法"""
        # 调用七宗欲分析
        success = result.get('status_code', 0) < 400 and not self._is_blocked_content(result.get('content', ''))
        self._seven_desires_analysis(url, result, response_time, success)
        
        # 更新成功连续次数
        if result['status_code'] == 200 and not self._is_blocked_content(result.get('content', '')):
            self.success_streak += 1
        else:
            self.success_streak = 0
        
        # 获取当前性能指标
        performance_metrics = self.self_awareness.get_performance_metrics()
        
        # 编码当前状态
        current_state = self.learning_optimizer.encode_state({
            'success_rate': performance_metrics['success_rate'],
            'avg_response_time': performance_metrics['avg_response_time'],
            'error_rate': sum(self.self_awareness.error_counts.values()) / max(1, len(self.crawl_history)),
            'resource_pressure': self.self_awareness.get_resource_metrics()['cpu_usage']['average'] / 100
        })
        
        # 计算奖励
        reward = self.learning_optimizer.calculate_reward(
            result['status_code'] == 200 and not self._is_blocked_content(result.get('content', '')),
            {
                'response_time': response_time,
                'resource_usage': self.self_awareness.get_resource_metrics()['cpu_usage']['average'] / 100,
                'success_streak': self.success_streak
            }
        )
        
        # 更新学习
        if hasattr(self, 'previous_state') and hasattr(self, 'previous_action'):
            self.learning_optimizer.learn(self.previous_state, self.previous_action, reward, current_state)
            self.learning_optimizer.store_experience(self.previous_state, self.previous_action, reward, current_state)
        
        # 选择下一个动作
        action = self.learning_optimizer.select_action(current_state)
        
        # 更新状态
        self.previous_state = current_state
        self.previous_action = action
        
        # 定期从经验中学习
        if len(self.crawl_history) % 10 == 0:
            self.learning_optimizer.replay_experiences()
    
    def _record_failure(self, url: str, error_message: str):
        """记录失败并执行学习"""
        try:
            # 重置成功连续次数
            self.success_streak = 0
            
            # 分析失败原因
            # 使用安全的结果对象，避免传递可能导致递归的数据
            safe_result = {
                'status_code': 500,
                'error': str(error_message),
                'url': url,
                'timestamp': time.time()
            }
            
            # 安全调用record_failure方法而不是analyze_crawl_result
            if hasattr(self.seven_desires, 'record_failure'):
                # 只传递必要的信息，避免复杂对象
                self.seven_desires.record_failure(url, safe_result)
            
            # 检测模式变化 - 但限制调用深度，避免递归
            recent_results = self.crawl_history[-5:] if len(self.crawl_history) >= 5 else self.crawl_history
            if recent_results and hasattr(self.seven_desires, 'detect_pattern_changes'):
                # 简化传递的参数
                try:
                    if self.seven_desires.detect_pattern_changes(url, recent_results):
                        # 生成自适应响应
                        if hasattr(self.seven_desires, 'generate_adaptive_response'):
                            adaptive_response = self.seven_desires.generate_adaptive_response(url, True)
                            if adaptive_response:
                                self._apply_adaptive_response(adaptive_response)
                except Exception as e:
                    print(f"[PhantomCrawler] 模式检测出错: {str(e)}")
        except Exception as e:
            print(f"[PhantomCrawler] 记录失败时出错: {str(e)}")
            # 避免在记录失败时再次触发记录失败的递归
    
    def _is_blocked_content(self, content: str) -> bool:
        """检查内容是否被阻止"""
        blocked_keywords = [
            'captcha', '验证码', 'robot', 'automated', 'blocked', 
            'suspicious', 'unusual activity', 'access denied'
        ]
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in blocked_keywords)
    
    def _adjust_strategy_based_on_error(self, error_type: str):
        """根据错误类型调整策略"""
        if error_type == 'timeout':
            # 超时错误，增加延迟和超时时间
            current_timeout = global_config.get('request_timeout', 30)
            global_config.set('request_timeout', min(60, current_timeout + 5))
            print(f"[七宗欲引擎] 检测到超时，增加超时时间至 {global_config.get('request_timeout')}")
        elif error_type == 'connection_error':
            # 连接错误，更换代理
            self.protocol_obfuscator.rotate_proxy()
            print(f"[七宗欲引擎] 检测到连接错误，已更换代理")
    
    def _metacognitive_adaptation(self, url: str, detection_info: Dict[str, Any]):
        """执行元认知自适应调整"""
        # 检测模式变化
        recent_results = self.crawl_history[-5:] if len(self.crawl_history) >= 5 else self.crawl_history
        pattern_changed = self.seven_desires.detect_pattern_changes(url, recent_results)
        
        # 生成自适应响应
        adaptive_response = self.seven_desires.generate_adaptive_response(url, pattern_changed or detection_info.get('blocked', False))
        
        # 应用自适应响应
        self._apply_adaptive_response(adaptive_response)
        
        # 获取学习优化建议
        performance_metrics = self.self_awareness.get_performance_metrics()
        adaptation_suggestion = self.learning_optimizer.suggest_adaptation({
            'success_rate': performance_metrics['success_rate'],
            'avg_response_time': performance_metrics['avg_response_time'],
            'error_rate': sum(self.self_awareness.error_counts.values()) / max(1, len(self.crawl_history)),
            'current_pattern': performance_metrics['current_pattern']
        })
        
        # 应用优化建议
        self._apply_optimization_suggestions(adaptation_suggestion)
    
    def _apply_adaptive_response(self, response: Dict[str, Any]):
        """应用自适应响应策略"""
        if response.get('fingerprint_reset', False):
            self.fingerprint_spoofer.reset_fingerprint()
            print(f"[七宗欲引擎] 重置指纹")
        
        if response.get('delay_increase_factor', 1.0) > 1.0:
            current_min = global_config.get('behavior_simulation.min_delay', 1.0)
            current_max = global_config.get('behavior_simulation.max_delay', 3.0)
            factor = response['delay_increase_factor']
            global_config.set('behavior_simulation.min_delay', current_min * factor)
            global_config.set('behavior_simulation.max_delay', current_max * factor)
            print(f"[七宗欲引擎] 增加延迟因子: {factor}")
        
        if response.get('force_proxy_change', False):
            self.protocol_obfuscator.force_proxy_change()
            print(f"[七宗欲引擎] 强制更换代理")
        
        if response.get('behavior_shift', False):
            self.behavior_simulator.shift_behavior_pattern()
            print(f"[七宗欲引擎] 切换欲望模式")
    
    def _apply_optimization_suggestions(self, suggestions: Dict[str, Any]):
        """应用学习优化器的建议"""
        adaptations = suggestions.get('suggested_adaptations', [])
        
        for adaptation in adaptations:
            if adaptation['priority'] in ['critical', 'high']:
                actions = adaptation['actions']
                
                for action in actions:
                    if action == 'change_fingerprint':
                        self.fingerprint_spoofer.refresh_fingerprint()
                    elif action == 'switch_proxy':
                        self.protocol_obfuscator.rotate_proxy()
                    elif action == 'increase_delay':
                        current_min = global_config.get('behavior_simulation.min_delay', 1.0)
                        current_max = global_config.get('behavior_simulation.max_delay', 3.0)
                        global_config.set('behavior_simulation.min_delay', current_min * 1.5)
                        global_config.set('behavior_simulation.max_delay', current_max * 1.5)
                    elif action == 'enhance_fingerprint':
                        global_config.set('fingerprint.enable_advanced_spoofing', True)
                    elif action == 'reset_all':
                        self._refresh_identity()
                        self.success_streak = 0
        
        # 更新策略性能统计
        if adaptations:
            strategy_type = adaptations[0].get('type', 'general')
            self.learning_optimizer.update_strategy_performance(
                strategy_type,
                suggestions.get('confidence', 0.5) > 0.7,  # 基于置信度判断成功
                suggestions.get('confidence', 0.5) * 10  # 奖励与置信度相关
            )
    
    def get_metacognitive_insights(self) -> Dict[str, Any]:
        """
        获取元认知系统的洞察和统计信息
        
        Returns:
            包含元认知洞察的字典
        """
        return {
            'self_awareness': {
                'performance': self.self_awareness.get_performance_metrics(),
                'resources': self.self_awareness.get_resource_metrics(),
                'environment': self.self_awareness.get_environment_assessment()
            },
            'learning': self.learning_optimizer.get_learning_summary(),
            'current_strategies': self.current_strategies,
            'success_streak': self.success_streak
        }
    
    def close(self):
        """关闭爬虫并释放所有资源"""
        # 关闭自我感知监控器
        if hasattr(self, 'self_awareness'):
            self.self_awareness.shutdown()
        
        # 保存元认知知识
        if hasattr(self, 'seven_desires'):
            self.seven_desires._save_desire_knowledge()
        
        # 关闭HTTP客户端
        if self.http_client:
            self.http_client.close()
        
        # 关闭Playwright浏览器
        if self.playwright_browser:
            self.playwright_browser.close()
        
        self.is_running = False
        print(f"[PhantomCrawler] 已关闭，会话ID: {self.session_id}")
    
    def _crawl_with_playwright(self, url: str, callback: Optional[Callable] = None, force_strategy: Optional[str] = None) -> Dict[str, Any]:
        """使用Playwright进行智能爬取，集成七宗欲引擎的环境感知和风险评估（实战版）"""
        try:
            from playwright.sync_api import sync_playwright
            
            # 从七宗欲引擎获取风险评估
            risk_level = self.seven_desires.desire_perception['detection_danger'] if hasattr(self.seven_desires, 'desire_perception') else 0
            dominant_desire = self.seven_desires.dominant_desire if hasattr(self.seven_desires, 'dominant_desire') else '贪婪'
            
            print(f"[七宗欲爬虫] Playwright模式 - {dominant_desire}驱动 - 风险等级: {risk_level:.2f}")
            
            # 记录开始时间
            start_time = time.time()
            
            with sync_playwright() as p:
                # 根据风险级别调整浏览器启动参数
                browser_args = [
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                ]
                
                # 高风险时添加更多的反检测参数
                if risk_level > 0.7:
                    browser_args.extend([
                        '--disable-gpu',
                        '--window-size=1920,1080',
                        '--disable-features=site-per-process',
                        '--disable-blink-features=ScriptStreaming',
                        '--start-maximized',
                        '--disable-infobars',
                        '--ignore-certificate-errors',
                        '--disable-software-rasterizer',
                        '--no-first-run',
                        '--no-default-browser-check',
                        '--disable-extensions',
                    ])
                
                # 根据风险级别调整slow_mo参数
                slow_mo_value = random.randint(50, 150)
                if risk_level > 0.5:
                    slow_mo_value = random.randint(100, 200)  # 更高风险时更慢
                elif risk_level < 0.3:
                    slow_mo_value = random.randint(30, 80)  # 低风险时可以更快
                
                # 启动浏览器
                browser = p.chromium.launch(
                    headless=global_config.get('playwright.headless', risk_level < 0.6),  # 高风险时使用有头模式
                    args=browser_args,
                    slow_mo=slow_mo_value
                )
                
                # 获取当前行为模式
                pattern = self.behavior_simulator.behavior_pattern
                
                # 高风险模式或stealth模式下使用高级指纹
                if risk_level > 0.5 or pattern == 'stealth':
                    fingerprint_headers = self.fingerprint_spoofer.generate_advanced_fingerprint()
                else:
                    fingerprint_headers = self.fingerprint_spoofer.generate_fingerprint()
                
                # 根据行为模式选择屏幕尺寸分布
                if pattern == 'careful' or pattern == 'stealth':
                    # 更常见的桌面分辨率
                    width = random.choice([1366, 1440, 1920])
                    height = random.choice([768, 900, 1080])
                elif pattern == 'hurried':
                    # 可能使用笔记本或移动设备
                    width = random.choice([1366, 1440, 1024, 375, 414])
                    height = random.choice([768, 900, 768, 667, 896])
                else:
                    # 默认更广泛的选择
                    width = random.choice([1366, 1440, 1536, 1920, 2560])
                    height = random.choice([768, 900, 1080, 1440])
                
                # 创建上下文并配置指纹
                context = browser.new_context(
                    user_agent=fingerprint_headers['User-Agent'],
                    locale=random.choice(['en-US', 'zh-CN', 'ja-JP']),
                    timezone_id=random.choice(['America/New_York', 'Europe/London', 'Asia/Shanghai']),
                    screen={
                        'width': width,
                        'height': height
                    },
                    viewport={'width': width, 'height': height},
                    user_data_dir=None  # 避免使用持久化用户数据
                )
                
                # 配置额外的指纹混淆
                context.set_extra_http_headers({
                    'Accept-Language': fingerprint_headers.get('Accept-Language', 'en-US,en;q=0.9'),
                    'Accept-Encoding': fingerprint_headers.get('Accept-Encoding', 'gzip, deflate, br'),
                })
                
                # 禁用自动化特征
                page = context.new_page()
                
                # 根据七宗欲和风险级别选择反检测脚本强度
                anti_detection_level = 'basic'
                
                # 欲望驱动的反检测策略
                desire_anti_detection = {
                    '傲慢': 'advanced',    # 适度保护
                    '嫉妒': 'maximum',     # 全面保护
                    '愤怒': 'advanced',    # 平衡速度和保护
                    '懒惰': 'basic',       # 最小保护
                    '贪婪': 'advanced',    # 平衡保护
                    '暴食': 'maximum',     # 快速但高强度
                    '色欲': 'maximum'      # 极致保护
                }
                
                # 先应用欲望驱动的反检测级别
                anti_detection_level = desire_anti_detection.get(dominant_desire, 'basic')
                
                # 再根据风险级别进行调整
                if risk_level > 0.5:
                    anti_detection_level = 'advanced'
                if risk_level > 0.8 or pattern == 'stealth':
                    anti_detection_level = 'maximum'
                
                print(f"[七宗欲爬虫] {dominant_desire}模式 - 反检测级别: {anti_detection_level}")
                
                # 获取并执行相应级别的反检测脚本
                anti_detection_script = self.fingerprint_spoofer.get_anti_detection_script(level=anti_detection_level)
                page.evaluate_on_new_document(anti_detection_script)
                
                # 根据风险级别决定是否添加Canvas指纹混淆
                if risk_level > 0.3:
                    page.evaluate_on_new_document(self.fingerprint_spoofer.get_canvas_fingerprint_confusion_script())
                
                # 根据风险级别决定是否添加WebGL指纹混淆
                if risk_level > 0.4:
                    page.evaluate_on_new_document(self.fingerprint_spoofer.get_webgl_fingerprint_confusion_script())
                
                # 设置请求拦截器
                page.route("**/*", lambda route, request: self._playwright_request_handler(route, request))
                
                # 记录网络请求以便分析
                all_responses = []
                blocked_requests = []
                
                def response_handler(response):
                    all_responses.append(response)
                    # 记录被阻止的请求
                    if response.status in [403, 429, 503]:
                        blocked_requests.append({
                            'url': response.url,
                            'status': response.status,
                            'headers': dict(response.headers)
                        })
                
                page.on('response', response_handler)
                
                # 使用优化的请求链
                request_chain = self._generate_optimized_request_chain(url)
                referrer = None
                
                # 计算请求链长度 - 基于风险级别
                chain_length = len(request_chain) - 1  # 不包括目标URL
                if risk_level > 0.7:
                    # 高风险时增加预热页面数量
                    chain_length = min(chain_length + 2, len(request_chain) - 1)
                elif risk_level < 0.3:
                    # 低风险时可以减少预热页面
                    chain_length = max(1, chain_length - 1)
                
                # 执行请求链中的污染资源请求
                for chain_url in request_chain[:chain_length]:
                    try:
                        # 设置请求头，包括动态生成的referrer
                        page.set_extra_http_headers(
                            self.fingerprint_spoofer.generate_dynamic_headers(chain_url, referrer)
                        )
                        
                        # 根据行为模式决定等待策略
                        wait_until = 'domcontentloaded'  # 默认
                        if pattern == 'careful' or pattern == 'stealth':
                            wait_until = 'networkidle'  # 更彻底等待
                        elif pattern == 'hurried':
                            wait_until = 'commit'  # 更快导航
                        
                        page.goto(chain_url, wait_until=wait_until, timeout=5000)
                        
                        # 基于元认知决策和环境风险动态调整交互强度
                        context_for_decision = {
                            'url': chain_url,
                            'risk_level': risk_level,
                            'behavior_pattern': pattern,
                            'content_type': page.evaluate('() => document.contentType'),
                            'element_count': page.evaluate('() => document.querySelectorAll("*").length')
                        }
                        
                        # 基于七宗欲和风险级别决定交互详细程度
                        detailed_interaction = False
                        
                        # 欲望驱动的交互详细度
                        desire_interaction_detail = {
                            '傲慢': False,      # 高效，无需详细交互
                            '嫉妒': True,       # 仔细模仿，详细交互
                            '愤怒': False,      # 急躁，减少交互
                            '懒惰': False,      # 最小化交互
                            '贪婪': True,       # 平衡交互
                            '暴食': False,      # 快速交互
                            '色欲': True        # 专注，详细交互
                        }
                        
                        # 先应用欲望驱动的交互详细度
                        detailed_interaction = desire_interaction_detail.get(dominant_desire, False)
                        
                        # 再根据风险级别和模式进行调整
                        if risk_level > 0.6 or pattern in ['careful', 'stealth']:
                            detailed_interaction = True
                        elif risk_level > 0.3 and context_for_decision['element_count'] > 500:
                            detailed_interaction = True
                        
                        # 根据内容复杂度估算合适的交互持续时间
                        content_complexity = min(context_for_decision['element_count'] / 1000, 1.0)
                        base_duration = 1.0 + content_complexity * 4.0
                        
                        # 应用元认知决策的交互
                        self.behavior_simulator.simulate_page_interaction(
                            page, 
                            context=context_for_decision,
                            detailed=detailed_interaction,
                            duration=base_duration if detailed_interaction else None
                        )
                        
                        referrer = chain_url
                    except Exception as e:
                        print(f"[PhantomCrawler] 请求链中资源失败: {str(e)}")
                    
                    # 基于七宗欲和风险级别调整等待时间
                    desire_delays = {
                        '傲慢': (0.8, 1.5),      # 短延迟
                        '嫉妒': (2.0, 3.5),      # 长延迟
                        '愤怒': (0.3, 0.8),      # 极短延迟
                        '懒惰': (3.0, 5.0),      # 最长延迟
                        '贪婪': (1.0, 2.0),      # 中等延迟
                        '暴食': (0.5, 1.2),      # 短延迟
                        '色欲': (2.5, 4.0)       # 较长延迟
                    }
                    
                    # 获取欲望对应的延迟范围
                    min_delay, max_delay = desire_delays.get(dominant_desire, (0.5, 1.5))
                    
                    # 根据风险级别调整
                    if risk_level > 0.6:
                        min_delay = max(min_delay, 1.5)
                        max_delay = max(max_delay, 3.0)
                    
                    # 应用延迟
                    self.behavior_simulator.human_delay(min_delay=min_delay, max_delay=max_delay)
                
                # 访问目标URL
                target_headers = self.fingerprint_spoofer.generate_dynamic_headers(url, referrer)
                page.set_extra_http_headers(target_headers)
                
                # 根据行为模式和风险级别调整等待策略和超时时间
                wait_strategy = 'networkidle'  # 默认更保守
                timeout_value = global_config.get('playwright.timeout', 30000)
                
                if pattern == 'hurried' and risk_level < 0.4:
                    wait_strategy = 'domcontentloaded'  # 快速浏览模式
                    timeout_value = 20000
                elif (pattern == 'careful' or pattern == 'stealth') or risk_level > 0.6:
                    wait_strategy = 'networkidle'  # 彻底等待
                    timeout_value = 45000  # 更长的超时时间
                
                page.goto(url, wait_until=wait_strategy, timeout=timeout_value)
                
                # 获取页面内容
                content = page.content()
                status_code = page.status
                
                # 检测是否存在验证码
                is_captcha = self.fingerprint_spoofer.is_captcha_page(content)
                is_blocked = self._is_blocked_content(content)
                
                # 基于检测结果更新元认知系统
                detection_info = {
                    'blocked': is_blocked or is_captcha,
                    'captcha_detected': is_captcha,
                    'status_code': status_code,
                    'url': url,
                    'blocked_requests_count': len(blocked_requests)
                }
                
                # 如果检测到阻止，执行元认知自适应
                if is_blocked or is_captcha:
                    print(f"[PhantomCrawler] {is_captcha and '检测到验证码页面' or '检测到被阻止内容'}")
                    
                    # 记录到元认知系统
                    detection_type = 'captcha_detected' if is_captcha else 'content_blocked'
                    self.seven_desires.record_detection_attempt(url, detection_type)
                    
                    # 更新风险级别
                    risk_increase = 0.3 if is_captcha else 0.2
                    self.seven_desires.update_risk_level(url, risk_increase)
                    
                    # 执行元认知自适应
                    self._metacognitive_adaptation(url, detection_info)
                    
                    # 根据风险级别决定冷却时间
                    base_cooldown = 10 if is_captcha else 5
                    cooldown_multiplier = 1 + risk_level  # 风险越高，冷却时间越长
                    cooldown_time = random.uniform(base_cooldown, base_cooldown + 10) * cooldown_multiplier
                    
                    print(f"[PhantomCrawler] 冷却时间: {cooldown_time:.2f}秒")
                    time.sleep(cooldown_time)
                
                # 应用元认知反检测策略
                # 注入反检测脚本
                if hasattr(self.fingerprint_spoofer, 'get_anti_detection_script'):
                    script_level = 'basic'
                    if risk_level > 0.7:
                        script_level = 'maximum'
                    elif risk_level > 0.4:
                        script_level = 'advanced'
                    
                    anti_detection_script = self.fingerprint_spoofer.get_anti_detection_script(level=script_level)
                    if anti_detection_script:
                        page.evaluate(anti_detection_script)
                        print(f"[PhantomCrawler] 注入{script_level}级反检测脚本")
                
                # 根据元认知分析调整交互策略
                interaction_probability = 0.8  # 默认80%概率执行完整交互
                if risk_level > 0.7:
                    interaction_probability = 1.0  # 高风险时总是执行交互
                elif pattern == 'hurried' and risk_level < 0.3:
                    interaction_probability = 0.5  # 低风险快速模式减少交互
                
                if random.random() < interaction_probability:
                    # 根据风险级别决定交互细节
                    if risk_level > 0.5 or pattern == 'careful' or pattern == 'stealth':
                        # 高风险或谨慎模式下执行详细交互
                        self.behavior_simulator.simulate_page_interaction(page, detailed=True)
                        
                        # 基于元认知分析的阅读行为
                        content_metrics = page.evaluate('''() => {
                            const paragraphs = document.querySelectorAll('p').length;
                            const textLength = document.body.textContent ? document.body.textContent.length : 0;
                            const isArticle = document.querySelector('article, .article, .content, .main-content') !== null;
                            return {
                                paragraphs: paragraphs,
                                textLength: textLength,
                                isArticle: isArticle
                            };
                        }''')
                        
                        # 计算阅读时间
                        base_reading_time = 2.0
                        if content_metrics['textLength'] > 10000:
                            base_reading_time = 10.0
                        elif content_metrics['textLength'] > 5000:
                            base_reading_time = 7.0
                        elif content_metrics['textLength'] > 2000:
                            base_reading_time = 5.0
                        elif content_metrics['textLength'] > 1000:
                            base_reading_time = 3.0
                        
                        # 根据风险级别调整
                        if risk_level > 0.7:
                            base_reading_time *= 1.5
                        elif pattern == 'hurried':
                            base_reading_time *= 0.7
                        
                        self.behavior_simulator.simulate_reading_behavior(page, duration=base_reading_time)
                    else:
                        # 基本交互
                        self.behavior_simulator.simulate_page_interaction(page)
                        
                        # 基本模式下也根据内容调整阅读时间
                        text_length = page.evaluate('() => document.body.textContent ? document.body.textContent.length : 0')
                        base_duration = max(1.0, min(3.0, text_length / 1000))
                        self.behavior_simulator.simulate_reading_behavior(page, duration=base_duration)
                else:
                    # 最小化交互模式
                    self.behavior_simulator._simulate_mouse_movement(page)
                    self.behavior_simulator._simulate_scrolling(page)
                
                # 随机额外等待，基于风险级别
                if random.random() < 0.3 + (risk_level * 0.4):  # 风险越高，等待概率越大
                    extra_wait = random.uniform(1, 3)
                    if risk_level > 0.6:
                        extra_wait *= 2  # 高风险时等待更久
                    time.sleep(extra_wait)
                
                # 获取最终内容
                final_content = page.content()
                final_status = page.status
                
                # 获取cookies和响应信息
                cookies = page.context.cookies()
                cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
                
                # 处理响应头和状态码
                headers = {}
                response_status = None
                
                # 查找目标URL的响应
                for response in all_responses:
                    if response.url == url or url in response.url:
                        headers = dict(response.headers)
                        response_status = response.status
                        break
                
                if response_status is None:
                    response_status = final_status
                
                # 调用回调
                if callback:
                    callback(page)
                
                # 随机关闭方式，基于风险级别
                if random.random() < 0.7:
                    page.close()
                    context.close()
                browser.close()
                
                # 计算响应时间
                response_time = time.time() - start_time
                
                # 准备结果
                result = {
                    'url': url,
                    'status_code': response_status or final_status,
                    'content': final_content,
                    'headers': headers,
                    'cookies': cookies_dict,
                    'playwright_used': True,
                    'user_agent': fingerprint_headers['User-Agent'],
                    'fingerprint_details': {
                        'viewport': {'width': width, 'height': height},
                        'user_agent': fingerprint_headers['User-Agent']
                    },
                    'response_time': response_time,
                    'blocked': is_blocked or is_captcha,
                    'captcha_detected': is_captcha,
                    'risk_level': risk_level
                }
                
                # 记录历史
                self.crawl_history.append({
                    'url': url,
                    'status_code': response_status or final_status,
                    'timestamp': time.time(),
                    'session_id': self.session_id,
                    'blocked': is_blocked or is_captcha,
                    'response_time': response_time,
                    'playwright_used': True,
                    'risk_level': risk_level
                })
                
                # 执行元认知分析
                self._metacognitive_analysis(url, result, response_time)
                
                # 更新环境感知
                self.behavior_simulator._update_environment_awareness(result)
                
                # 如果未被阻止且连续成功，考虑降低风险评估
                if not result['blocked'] and hasattr(self, 'success_streak') and self.success_streak > 3:
                    self.seven_desires.update_risk_level(url, -0.1)  # 略微降低风险评估
                
                return result
                
        except Exception as e:
            error_msg = str(e)
            print(f"[PhantomCrawler] Playwright备用爬取失败: {error_msg}")
            
            # 分析错误类型
            error_type = 'unknown_error'
            error_str = str(error_msg).lower() if error_msg else ''
            if 'timeout' in error_str:
                error_type = 'timeout_error'
            elif 'connection' in error_str:
                error_type = 'connection_error'
            elif 'network' in error_str:
                error_type = 'network_error'
            elif 'browser' in error_str:
                error_type = 'browser_error'
            elif 'captcha' in error_str or 'block' in error_str:
                error_type = 'detection_error'
            
            # 根据错误类型调整策略
            self._adjust_strategy_based_on_error(error_type)
            
            # 记录失败到元认知系统
            self._record_failure(url, error_msg)
            
            # 更新风险级别 - 基于错误类型
            if error_type == 'detection_error':
                self.seven_desires.update_risk_level(url, 0.3)  # 显著增加风险
            elif error_type in ['browser_error', 'network_error']:
                self.seven_desires.update_risk_level(url, 0.1)  # 轻微增加风险
            
            # 尝试切换行为模式
            if error_type == 'detection_error' and hasattr(self, 'behavior_simulator'):
                self.behavior_simulator.shift_behavior_pattern()
            
            # 抛出异常以便上层捕获处理，但标记已经尝试过playwright
            raise Exception(f"Playwright爬取失败: {error_msg}") from e
    
    def crawl_batch(self, urls: List[str], max_concurrent: int = 3) -> List[Dict[str, Any]]:
        """批量爬取多个URL"""
        results = []
        
        # 将URL分成批次
        for i in range(0, len(urls), max_concurrent):
            batch = urls[i:i+max_concurrent]
            batch_results = []
            
            for url in batch:
                result = self.crawl(url)
                batch_results.append(result)
                
                # 批次内的URL之间添加延时
                if url != batch[-1]:
                    self.behavior_simulator.human_delay()
            
            results.extend(batch_results)
            
            # 批次之间添加更长的延时
            if i + max_concurrent < len(urls):
                time.sleep(random.uniform(5, 10))
        
        return results
    
    def _playwright_request_handler(self, route, request):
        """Playwright请求处理函数，用于拦截和修改请求"""
        # 跳过某些资源类型以提高性能
        skip_resource_types = global_config.get('playwright.skip_resource_types', ['image', 'media', 'font'])
        
        # 智能跳过资源 - 基于URL模式
        if request.resource_type in skip_resource_types:
            # 但允许一些重要的图片资源通过（如验证码）
            url = request.url
            important_image_patterns = ['captcha', 'verify', 'security', 'auth']
            if not any(pattern in url.lower() for pattern in important_image_patterns):
                route.abort()
                return
        
        # 生成动态请求头
        headers = dict(request.headers)
        
        # 移除可能暴露自动化的头部
        headers_to_remove = ['X-Powered-By', 'Server', 'X-AspNet-Version']
        for header in headers_to_remove:
            if header in headers:
                del headers[header]
        
        # 智能修改头部 - 基于请求类型
        if request.resource_type == 'document':
            # 为主要文档请求添加更完整的头部
            headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            headers['Accept-Language'] = random.choice(['en-US,en;q=0.9', 'zh-CN,zh;q=0.9', 'ja-JP,ja;q=0.9'])
            headers['Cache-Control'] = random.choice(['max-age=0', 'no-cache'])
            
            # 只对非HTTPS请求添加这个头部
            if not request.url.startswith('https'):
                headers['Upgrade-Insecure-Requests'] = '1'
        
        elif request.resource_type == 'script':
            # 为脚本请求添加合适的头部
            headers['Accept'] = '*/*'
            headers['Accept-Encoding'] = 'gzip, deflate, br'
        
        elif request.resource_type == 'xhr' or request.resource_type == 'fetch':
            # 为API请求添加适当的头部
            headers['X-Requested-With'] = 'XMLHttpRequest'
            headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        
        # 随机添加或修改一些其他头部
        if random.random() < 0.3:
            headers['DNT'] = '1'
        
        # 添加请求签名参数
        if random.random() < 0.4 and request.resource_type == 'xhr':
            from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
            
            parsed_url = urlparse(request.url)
            query_params = parse_qs(parsed_url.query)
            
            # 生成请求签名
            signature = self.fingerprint_spoofer.generate_request_signature()
            
            # 随机选择参数名
            param_names = ['_', 't', 'v', 'uid', 'r', 's']
            param_name = random.choice(param_names)
            query_params[param_name] = [signature['nonce']]
            
            # 重新构建URL
            new_query = urlencode(query_params, doseq=True)
            new_url = urlunparse(
                (parsed_url.scheme, parsed_url.netloc, parsed_url.path, 
                parsed_url.params, new_query, parsed_url.fragment)
            )
            
            route.continue_(url=new_url, headers=headers)
        else:
            route.continue_(headers=headers)
            
    def close(self) -> None:
        """关闭爬虫，清理资源"""
        if self.http_client:
            self.http_client.close()
        
        if self.playwright_browser:
            # 关闭Playwright浏览器
            pass
        
        self.is_running = False
        print(f"[PhantomCrawler] 已关闭，会话ID: {self.session_id}")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取爬虫统计信息"""
        return {
            'session_id': self.session_id,
            'crawl_count': len(self.crawl_history),
            'is_running': self.is_running,
            'behavior_stats': self.behavior_simulator.get_behavior_statistics(),
            'proxy_count': len(self.protocol_obfuscator.proxy_chain)
        }