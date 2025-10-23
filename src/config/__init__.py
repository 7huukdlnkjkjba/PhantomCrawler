"""PhantomCrawler 配置模块"""
import os
import json
import yaml
from typing import Any, Dict, Optional


class ConfigManager:
    """配置管理器类，用于加载和访问配置项"""
    
    def __init__(self, config_file: Optional[str] = None):
        # 默认配置
        self._default_config = {
            # 爬虫核心配置
            'request_timeout': 30,
            'max_retries': 3,
            
            # 用户代理池
            'user_agent_pool': [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Mobile Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/114.0',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1',
                'Mozilla/5.0 (iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/114.0.1823.67 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Edge/114.0.1823.67 Safari/537.36'
            ],
            
            # 指纹欺骗配置
            'fingerprint': {
                'enable_browser_fingerprint_spoofing': True,
                'canvas_noise_level': 0.5,
                'webgl_noise_level': 0.3,
                'font_list_spoofing': True,
                'audio_fingerprint_spoofing': True
            },
            
            # 行为模拟器配置
            'behavior_simulator': {
                'mouse_movement_enabled': True,
                'scrolling_enabled': True,
                'clicking_enabled': True,
                'typing_enabled': True,
                'delay_min': 1.0,
                'delay_max': 3.0,
                'mouse': {
                    'jitter_intensity': 0.5,
                    'speed_variation': 0.3,
                    'acceleration_factor': 0.2,
                    'path_complexity': 0.4
                }
            },
            
            # Playwright配置
            'playwright': {
                'headless': True,
                'timeout': 30000,
                'skip_resource_types': ['image', 'media', 'font', 'stylesheet'],
                'viewport_width': 1920,
                'viewport_height': 1080
            },
            
            # 代理配置
            'proxy_chain': [],
            'proxy_rotation_interval': 300,  # 秒
            
            # 验证码检测配置
            'captcha_detection': {
                'enabled': True,
                'keywords': ['captcha', '验证码', 'robot', 'automated', 'blocked', 'security check', '人机验证'],
                'url_patterns': ['captcha', 'verify', 'security', 'auth', 'challenge'],
                'html_patterns': ['g-recaptcha', 'hcaptcha', 'recaptcha', 'captcha-image'],
                'js_functions': ['grecaptcha.execute', 'hcaptcha.execute', 'loadCaptcha']
            },
            
            # 请求签名配置
            'request_signature': {
                'enabled': True,
                'signature_alg': 'md5',
                'timestamp_format': 'millisecond'
            },
            
            # TLS指纹配置
            'tls_fingerprint': {
                'enabled': True,
                'browser_mimic': 'chrome',  # chrome, firefox, safari
                'custom_cipher_suites': []
            }
        }
        
        # 实际配置字典
        self._config = self._default_config.copy()
        
        # 加载配置文件
        if config_file:
            self.load_config(config_file)
    
    def load_config(self, config_file: str) -> None:
        """从文件加载配置
        
        Args:
            config_file: 配置文件路径
        """
        if not os.path.exists(config_file):
            print(f"[PhantomCrawler] 警告: 配置文件 {config_file} 不存在，使用默认配置")
            return
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                if config_file.endswith('.json'):
                    user_config = json.load(f)
                elif config_file.endswith('.yaml') or config_file.endswith('.yml'):
                    user_config = yaml.safe_load(f)
                else:
                    print(f"[PhantomCrawler] 警告: 不支持的配置文件格式: {config_file}")
                    return
                
                # 深度合并配置
                self._merge_configs(self._config, user_config)
                print(f"[PhantomCrawler] 配置文件 {config_file} 加载成功")
                
        except Exception as e:
            print(f"[PhantomCrawler] 加载配置文件失败: {str(e)}")
    
    def _merge_configs(self, base: Dict[str, Any], update: Dict[str, Any]) -> None:
        """深度合并配置字典
        
        Args:
            base: 基础配置
            update: 要合并的配置
        """
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_configs(base[key], value)
            else:
                base[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项
        
        Args:
            key: 配置键，支持点号分隔的嵌套路径
            default: 默认值
            
        Returns:
            配置值或默认值
        """
        parts = key.split('.')
        value = self._config
        
        try:
            for part in parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    return default
            return value
        except Exception:
            return default
    
    def set(self, key: str, value: Any) -> None:
        """设置配置项
        
        Args:
            key: 配置键，支持点号分隔的嵌套路径
            value: 配置值
        """
        parts = key.split('.')
        config = self._config
        
        for part in parts[:-1]:
            if part not in config or not isinstance(config[part], dict):
                config[part] = {}
            config = config[part]
        
        config[parts[-1]] = value
    
    def get_all(self) -> Dict[str, Any]:
        """获取所有配置
        
        Returns:
            完整配置字典
        """
        return self._config.copy()


# 创建全局配置实例
global_config = ConfigManager()

# 导出配置类和全局实例
__all__ = ['ConfigManager', 'global_config']