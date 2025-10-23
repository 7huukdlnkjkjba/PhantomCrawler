# PhantomCrawler - HTML解析模块
import re
from urllib.parse import urlparse, urljoin
from typing import List, Dict, Optional

class HTMLParser:
    """HTML解析器，用于提取页面中的链接"""
    
    def __init__(self):
        # 常用的链接提取正则表达式
        self.link_pattern = re.compile(r'<a[^>]+href=["\'](.*?)["\'][^>]*>', re.IGNORECASE)
        
    def extract_links(self, html_content: str, base_url: str) -> List[str]:
        """
        从HTML内容中提取链接
        
        Args:
            html_content: HTML内容字符串
            base_url: 基础URL，用于解析相对路径
            
        Returns:
            提取的链接列表
        """
        if not html_content:
            return []
        
        # 提取所有链接
        raw_links = self.link_pattern.findall(html_content)
        
        # 清理和规范化链接
        normalized_links = []
        for link in raw_links:
            # 跳过JavaScript链接和锚点链接
            if link.startswith('javascript:') or link.startswith('#'):
                continue
            
            # 处理相对路径
            if not link.startswith(('http://', 'https://')):
                link = urljoin(base_url, link)
            
            # 规范化URL（移除片段部分）
            parsed = urlparse(link)
            normalized_link = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if parsed.query:
                normalized_link += f"?{parsed.query}"
            
            normalized_links.append(normalized_link)
        
        return list(set(normalized_links))  # 去重
    
    def filter_links_by_domain(self, links: List[str], target_domain: str) -> List[str]:
        """
        根据域名过滤链接
        
        Args:
            links: 链接列表
            target_domain: 目标域名
            
        Returns:
            过滤后的链接列表
        """
        filtered_links = []
        for link in links:
            parsed = urlparse(link)
            # 检查域名是否匹配（支持子域名）
            if parsed.netloc and (parsed.netloc == target_domain or parsed.netloc.endswith(f'.{target_domain}')):
                filtered_links.append(link)
        
        return filtered_links
    
    def filter_links_by_pattern(self, links: List[str], include_patterns: Optional[List[str]] = None, 
                              exclude_patterns: Optional[List[str]] = None) -> List[str]:
        """
        根据模式过滤链接
        
        Args:
            links: 链接列表
            include_patterns: 包含的模式列表
            exclude_patterns: 排除的模式列表
            
        Returns:
            过滤后的链接列表
        """
        filtered_links = links.copy()
        
        # 应用包含模式
        if include_patterns:
            filtered_links = [link for link in filtered_links 
                            if any(pattern in link for pattern in include_patterns)]
        
        # 应用排除模式
        if exclude_patterns:
            filtered_links = [link for link in filtered_links 
                            if not any(pattern in link for pattern in exclude_patterns)]
        
        return filtered_links