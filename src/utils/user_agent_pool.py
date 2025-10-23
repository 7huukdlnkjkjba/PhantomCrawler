# PhantomCrawler - 用户代理池工具
import random
from typing import List

# 常用浏览器的User-Agent池
USER_AGENTS = [
    # Chrome浏览器
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    
    # Firefox浏览器
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:114.0) Gecko/20100101 Firefox/114.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.0; rv:115.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (X11; Linux i686; rv:115.0) Gecko/20100101 Firefox/115.0',
    
    # Safari浏览器
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    
    # Edge浏览器
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    
    # 移动设备
    'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; SM-A526B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
]

# 按照浏览器类型分类的User-Agent
UA_BY_BROWSER = {
    'chrome': [ua for ua in USER_AGENTS if 'Chrome' in ua and 'Edg' not in ua],
    'firefox': [ua for ua in USER_AGENTS if 'Firefox' in ua],
    'safari': [ua for ua in USER_AGENTS if 'Safari' in ua and 'Chrome' not in ua and 'Edg' not in ua],
    'edge': [ua for ua in USER_AGENTS if 'Edg' in ua],
    'mobile': [ua for ua in USER_AGENTS if 'Mobile' in ua],
}

def get_user_agent_pool() -> List[str]:
    """获取完整的User-Agent池"""
    return USER_AGENTS.copy()

def get_random_user_agent() -> str:
    """随机获取一个User-Agent"""
    return random.choice(USER_AGENTS)

def get_user_agent_by_browser(browser_type: str) -> str:
    """根据浏览器类型获取随机User-Agent"""
    browser_type = browser_type.lower()
    if browser_type in UA_BY_BROWSER and UA_BY_BROWSER[browser_type]:
        return random.choice(UA_BY_BROWSER[browser_type])
    return get_random_user_agent()

def add_custom_user_agent(ua: str) -> None:
    """添加自定义User-Agent到池中"""
    if ua not in USER_AGENTS:
        USER_AGENTS.append(ua)
        # 更新按浏览器分类的池
        _update_browser_categories(ua)

def _update_browser_categories(ua: str) -> None:
    """更新浏览器分类的User-Agent池"""
    if 'Chrome' in ua and 'Edg' not in ua:
        UA_BY_BROWSER['chrome'].append(ua)
    elif 'Firefox' in ua:
        UA_BY_BROWSER['firefox'].append(ua)
    elif 'Safari' in ua and 'Chrome' not in ua and 'Edg' not in ua:
        UA_BY_BROWSER['safari'].append(ua)
    elif 'Edg' in ua:
        UA_BY_BROWSER['edge'].append(ua)
    if 'Mobile' in ua:
        UA_BY_BROWSER['mobile'].append(ua)