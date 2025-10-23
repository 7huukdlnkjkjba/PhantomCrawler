# PhantomCrawler 核心配置文件
import os
from typing import Dict, List, Any, Optional
import yaml
import uuid

# 全局配置实例（延迟初始化）
global_config_instance = None

class Config:
    def __init__(self, config_file: str = None):
        # 默认配置
        self.default_config = {
            # 基础配置
            'user_agent_pool': [],
            'proxy_chain': [],
            'request_timeout': 30,
            'max_retries': 3,
            
            # 指纹伪装配置
            'fingerprint': {
                'enable_dynamic_ua': True,
                'enable_ja3_simulation': True,
                'enable_browser_fingerprint_spoofing': True,
                'accept_languages': ['en-US,en;q=0.9', 'zh-CN,zh;q=0.9', 'ja-JP,ja;q=0.8'],
                'accept_encodings': ['gzip', 'deflate', 'br'],
            },
            
            # 行为模拟配置
            'behavior_simulation': {
                'enable_human_delay': True,
                'min_delay': 1.0,
                'max_delay': 5.0,
                'use_gamma_distribution': True,
                'gamma_shape': 2.0,
                'gamma_scale': 1.0,
                'enable_session_roles': True,
                'enable_request_chain_pollution': True,
                'pollution_resources': [
                    'https://code.jquery.com/jquery-3.6.0.min.js',
                    'https://fonts.googleapis.com/css?family=Roboto',
                    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css'
                ]
            },
            
            # 元认知系统配置
            'metacognition': {
                'enabled': True,
                'learning_rate': 0.1,
                'discount_factor': 0.9,
                'exploration_rate': 0.2,
                'knowledge_storage': {
                    'enabled': True,
                    'path': os.path.join(os.path.dirname(__file__), 'data', 'knowledge_base.json'),
                    'save_interval': 60  # 秒
                },
                'strategy_optimization': {
                    'enabled': True,
                    'memory_retention': 1000,  # 保留的历史记录数量
                    'adaptive_threshold': 0.7  # 自适应调整阈值
                },
                'self_awareness': {
                    'enabled': True,
                    'resource_monitoring_interval': 5,  # 秒
                    'performance_metrics_window': 60,  # 秒
                    'alert_thresholds': {
                        'cpu_usage': 80,  # 百分比
                        'memory_usage': 85,  # 百分比
                        'error_rate': 0.3  # 错误率阈值
                    }
                }
            },
            
            # 反侦测配置
            'anti_detection': {
                'use_undetected_chromedriver': True,
                'use_stealth_plugins': True,
                'handle_captchas': True,
                'captcha_solver_type': 'tesseract',  # 'tesseract' or 'api'
                'captcha_api_key': '',
                'detect_honeypots': True,
            },
            
            # 解析引擎配置
            'parsing': {
                'enable_adaptive_parsing': True,
                'max_history_items': 50,
                'enable_js_execution': True,
            },
            
            # 持久化配置
            'persistence': {
                'storage_mode': 'encrypted_sqlite',  # 'encrypted_sqlite', 'hidden_cache', 'exif_embedded'
                'sqlite_db_path': 'data/phantom.db',
                'sqlite_encryption_key': '',  # 将在运行时设置
                'remote_push_enabled': False,
                'remote_push_url': '',
                'remote_push_encryption': True,
            },
            
            # 分布式配置
            'distributed': {
                'enabled': False,
                'node_type': 'master',  # 'master' or 'worker'
                'redis_url': 'redis://localhost:6379',
                'master_host': 'localhost',
                'master_port': 5555,
                'worker_id': f'worker-{uuid.uuid4()}',  # 工作节点ID，自动生成
            },
            
            # 情报收集配置
            'intelligence': {
                'subdomain_enum_enabled': True,
                'api_endpoint_fuzzing': False,
                'api_fuzzing_depth': 1,
            },
            
            # 日志和安全配置
            'security': {
                'clean_logs_after_run': False,
                'obfuscate_logs': True,
                'emergency_exit_on_detection': False,
                'heartbeat_interval': 300,  # 秒
            },
            
            # Playwright配置
            'playwright': {
                'headless': True,
                'slow_mo': 50,  # 慢动作，模拟真实用户操作
            }
        }
        
        # 加载自定义配置
        self.config = self.default_config.copy()
        if config_file and os.path.exists(config_file):
            self._load_from_file(config_file)
        
        # 初始化基本数据
        self._initialize_default_data()
        
        # 更新全局配置实例
        global global_config_instance
        global_config_instance = self
    
    def _load_from_file(self, config_file: str) -> None:
        """从文件加载配置"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                custom_config = yaml.safe_load(f)
                if custom_config:
                    self._update_config(custom_config)
        except Exception as e:
            print(f"警告: 无法加载配置文件 {config_file}: {str(e)}")
    
    def _initialize_default_data(self) -> None:
        """初始化默认数据，如User-Agent池"""
        # 默认User-Agent池
        if not self.config['user_agent_pool']:
            self.config['user_agent_pool'] = [
                # Chrome
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Mobile Safari/537.36',
                
                # Firefox
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/114.0',
                
                # Safari
                'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15',
            ]
        
    def _load_from_file(self, config_file: str) -> None:
        """从YAML文件加载配置"""
        with open(config_file, 'r', encoding='utf-8') as f:
            custom_config = yaml.safe_load(f)
            if custom_config:
                self._merge_configs(self.config, custom_config)
    
    def _update_config(self, user_config: Dict[str, Any]) -> None:
        """递归更新配置"""
        for key, value in user_config.items():
            if key in self.config and isinstance(self.config[key], dict) and isinstance(value, dict):
                # 递归更新嵌套配置
                self._update_config_nested(self.config[key], value)
            else:
                self.config[key] = value
    
    def _update_config_nested(self, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        """递归更新嵌套配置"""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._update_config_nested(target[key], value)
            else:
                target[key] = value
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """根据键路径获取配置值"""
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any) -> None:
        """根据键路径设置配置值"""
        keys = key_path.split('.')
        config = self.config
        
        # 导航到目标键的父级
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            elif not isinstance(config[key], dict):
                config[key] = {}
            config = config[key]
        
        # 设置最终的值
        config[keys[-1]] = value
        
        # 更新全局配置实例
        global global_config_instance
        if global_config_instance is self:
            global_config_instance.config = self.config.copy()
    
    def export(self) -> Dict[str, Any]:
        """导出配置为字典"""
        return self.config.copy()
    
    def save(self, file_path: str) -> None:
        """保存配置到文件"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
    
    def validate(self) -> List[str]:
        """验证配置的有效性"""
        errors = []
        
        # 验证必要的配置项
        if self.get('request_timeout', 0) <= 0:
            errors.append('请求超时必须大于0')
        
        if self.get('max_retries', -1) < 0:
            errors.append('最大重试次数必须大于等于0')
        
        # 验证代理链格式
        proxy_chain = self.get('proxy_chain', [])
        for i, proxy in enumerate(proxy_chain):
            if not isinstance(proxy, dict) or 'type' not in proxy or 'host' not in proxy or 'port' not in proxy:
                errors.append(f'代理链中的第{i+1}个代理格式无效')
        
        # 验证存储路径
        if self.get('persistence.storage_mode') == 'encrypted_sqlite':
            db_path = self.get('persistence.sqlite_db_path', '')
            if not db_path:
                errors.append('SQLite数据库路径不能为空')
        
        return errors

# 获取全局配置的工厂函数
def get_global_config():
    """获取全局配置实例"""
    global global_config_instance
    if global_config_instance is None:
        global_config_instance = Config()
    return global_config_instance

# 创建并导出默认全局配置实例
global_config = get_global_config()