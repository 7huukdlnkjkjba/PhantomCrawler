# PhantomCrawler - 行为模拟模块
import random
import time
import numpy as np
import math
from typing import Dict, List, Tuple, Optional, Any
from src.configs.config import global_config

class BehaviorSimulator:
    """模拟人类浏览行为的核心类"""
    
    def __init__(self):
        # 人类行为参数
        self.min_delay = global_config.get('behavior_simulation.min_delay', 1.0)
        self.max_delay = global_config.get('behavior_simulation.max_delay', 5.0)
        self.use_gamma_distribution = global_config.get('behavior_simulation.use_gamma_distribution', True)
        self.gamma_shape = global_config.get('behavior_simulation.gamma_shape', 2.0)
        self.gamma_scale = global_config.get('behavior_simulation.gamma_scale', 1.0)
        
        # 会话角色状态
        self.session_roles = {
            'casual_browser': {
                'click_probability': 0.3,
                'view_duration': (1, 5),
                'depth': (1, 3),
            },
            'researcher': {
                'click_probability': 0.7,
                'view_duration': (5, 15),
                'depth': (3, 8),
            },
            'product_shopper': {
                'click_probability': 0.5,
                'view_duration': (3, 10),
                'depth': (2, 6),
            },
            'information_seeker': {
                'click_probability': 0.8,
                'view_duration': (2, 8),
                'depth': (4, 10),
            }
        }
        
        # 当前会话状态
        self.current_role = None
        self.session_history = []
        self.current_depth = 0
    
    def human_delay(self) -> None:
        """执行符合人类行为的延时"""
        if global_config.get('behavior_simulation.enable_human_delay', True):
            if self.use_gamma_distribution:
                # 使用伽马分布生成更符合人类行为的延时
                delay = np.random.gamma(self.gamma_shape, self.gamma_scale)
                # 确保在配置范围内
                delay = max(self.min_delay, min(self.max_delay, delay))
            else:
                # 简单的均匀分布
                delay = random.uniform(self.min_delay, self.max_delay)
            
            time.sleep(delay)
    
    def init_session_role(self) -> Dict:
        """初始化会话角色"""
        if global_config.get('behavior_simulation.enable_session_roles', True):
            self.current_role = random.choice(list(self.session_roles.keys()))
            return self.session_roles[self.current_role]
        return self.session_roles['casual_browser']  # 默认角色
    
    def should_click(self) -> bool:
        """根据当前角色决定是否点击链接"""
        if not self.current_role:
            self.init_session_role()
        
        role_config = self.session_roles[self.current_role]
        return random.random() < role_config['click_probability']
    
    def get_view_duration(self) -> float:
        """获取当前页面的浏览时间"""
        if not self.current_role:
            self.init_session_role()
        
        role_config = self.session_roles[self.current_role]
        duration_range = role_config['view_duration']
        return random.uniform(duration_range[0], duration_range[1])
    
    def is_session_complete(self) -> bool:
        """判断会话是否应该结束"""
        if not self.current_role:
            return True
        
        role_config = self.session_roles[self.current_role]
        max_depth = role_config['depth'][1]
        return self.current_depth >= max_depth
    
    def record_page_view(self, url: str, referrer: Optional[str] = None) -> None:
        """记录页面访问"""
        timestamp = time.time()
        self.session_history.append({
            'url': url,
            'referrer': referrer,
            'timestamp': timestamp,
            'depth': self.current_depth
        })
        self.current_depth += 1
    
    def simulate_reading_behavior(self) -> None:
        """模拟阅读行为"""
        # 模拟用户在页面上的停留和阅读行为
        view_duration = self.get_view_duration()
        
        # 将总时间分成多个小段，模拟注意力分散和重新聚焦
        segments = random.randint(1, 4)
        segment_duration = view_duration / segments
        
        for i in range(segments):
            # 主阅读时间
            time.sleep(segment_duration * 0.8)
            
            # 注意力分散（如查看其他标签页）
            if i < segments - 1 and random.random() < 0.3:
                distraction_time = random.uniform(0.5, 2.0)
                time.sleep(distraction_time)
    
    def generate_click_path(self, available_links: List[str], current_url: str) -> List[str]:
        """生成模拟人类的点击路径"""
        if not self.current_role:
            self.init_session_role()
        
        role_config = self.session_roles[self.current_role]
        max_depth = random.randint(role_config['depth'][0], role_config['depth'][1])
        
        click_path = [current_url]
        remaining_depth = max_depth - 1  # 减去当前页面
        
        while remaining_depth > 0 and available_links:
            if self.should_click():
                # 选择一个链接
                next_link = random.choice(available_links)
                click_path.append(next_link)
                # 移除已选择的链接以避免循环
                available_links = [link for link in available_links if link != next_link]
                remaining_depth -= 1
                
                # 模拟页面间的导航时间
                self.human_delay()
            else:
                break
        
        return click_path
    
    def simulate_mouse_movement(self, page: Any = None) -> List[Tuple[int, int]]:
        """模拟真实的鼠标移动路径
        
        Args:
            page: Playwright或其他浏览器自动化页面对象
            
        Returns:
            鼠标移动路径点列表
        """
        # 生成一个不完全直线的鼠标移动路径
        start_x = random.randint(0, 100)
        start_y = random.randint(0, 100)
        end_x = random.randint(800, 1000)
        end_y = random.randint(400, 600)
        
        # 使用Bézier曲线生成更自然的路径
        control_points = random.randint(1, 3)
        points = [(start_x, start_y)]
        
        # 生成中间控制点
        for i in range(control_points):
            factor = (i + 1) / (control_points + 1)
            mid_x = int(start_x + (end_x - start_x) * factor)
            mid_y = int(start_y + (end_y - start_y) * factor)
            
            # 添加随机偏移
            offset_x = random.randint(-100, 100)
            offset_y = random.randint(-100, 100)
            
            points.append((mid_x + offset_x, mid_y + offset_y))
        
        points.append((end_x, end_y))
        
        # 计算完整路径
        steps = random.randint(20, 50)
        path = self._calculate_bezier_curve(points, steps)
        
        # 如果提供了页面对象，则执行实际移动
        if page:
            try:
                # 移动到起点
                page.mouse.move(start_x, start_y)
                
                # 执行多次随机移动
                num_movements = random.randint(3, 8)
                current_x, current_y = start_x, start_y
                
                for _ in range(num_movements):
                    # 随机目标点
                    target_x = random.randint(0, 1920)
                    target_y = random.randint(0, 1080)
                    
                    # 生成Bézier路径
                    move_path = self._calculate_bezier_curve([(current_x, current_y), 
                                                             (target_x, target_y)], steps)
                    
                    # 移动鼠标
                    for x, y in move_path:
                        page.mouse.move(x, y)
                        time.sleep(random.uniform(0.01, 0.03))
                    
                    current_x, current_y = target_x, target_y
                    time.sleep(random.uniform(0.2, 1.0))
                
                # 随机点击
                if random.random() < 0.3:
                    page.mouse.click(current_x, current_y)
                    time.sleep(random.uniform(0.1, 0.3))
                    
            except Exception as e:
                print(f"[BehaviorSimulator] 鼠标移动模拟失败: {str(e)}")
        
        return path
    
    def _calculate_bezier_curve(self, points: List[Tuple[int, int]], steps: int) -> List[Tuple[int, int]]:
        """计算Bézier曲线上的点
        
        Args:
            points: 控制点列表
            steps: 步数
        
        Returns:
            路径点列表
        """
        n = len(points) - 1
        result = []
        
        for t in np.linspace(0, 1, steps):
            x, y = 0, 0
            
            for i in range(n + 1):
                # 计算Bézier基函数
                binomial = math.comb(n, i)
                term = binomial * (t ** i) * ((1 - t) ** (n - i))
                
                x += term * points[i][0]
                y += term * points[i][1]
            
            result.append((int(x), int(y)))
        
        return result
    
    def simulate_scroll(self, page: Any) -> None:
        """模拟真实的滚动行为
        
        Args:
            page: Playwright或其他浏览器自动化页面对象
        """
        try:
            # 获取页面高度
            page_height = page.evaluate('() => document.body.scrollHeight')
            
            # 滚动模式
            scroll_modes = ['smooth', 'intermittent', 'fast', 'slow']
            mode = random.choice(scroll_modes)
            
            if mode == 'smooth':
                # 平滑滚动
                total_scroll = min(page_height - 800, 2000)
                step_count = random.randint(20, 40)
                step_size = total_scroll / step_count
                
                for i in range(step_count):
                    y = i * step_size
                    page.evaluate(f'window.scrollTo({{top: {y}, behavior: "smooth"}})')
                    time.sleep(random.uniform(0.05, 0.15))
                    
            elif mode == 'intermittent':
                # 间歇性滚动
                current_pos = 0
                while current_pos < min(page_height - 800, 1500):
                    scroll_amount = random.randint(50, 300)
                    current_pos += scroll_amount
                    page.evaluate(f'window.scrollTo(0, {current_pos})')
                    time.sleep(random.uniform(0.3, 1.5))
                    
            elif mode == 'fast':
                # 快速滚动
                page.evaluate('window.scrollTo(0, Math.min(document.body.scrollHeight - 800, 1000))')
                time.sleep(random.uniform(0.5, 1.0))
                
            elif mode == 'slow':
                # 慢速滚动
                total_scroll = min(page_height - 800, 1200)
                step_count = random.randint(30, 50)
                step_size = total_scroll / step_count
                
                for i in range(step_count):
                    y = i * step_size
                    page.evaluate(f'window.scrollTo(0, {y})')
                    time.sleep(random.uniform(0.1, 0.3))
                    
            # 随机回滚一点
            if random.random() < 0.4:
                page.evaluate('window.scrollBy(0, -50)')
                time.sleep(random.uniform(0.5, 1.0))
                
        except Exception as e:
            print(f"[BehaviorSimulator] 滚动模拟失败: {str(e)}")
    
    def simulate_page_interaction(self, page: Any) -> bool:
        """模拟真实的页面交互行为
        
        Args:
            page: Playwright或其他浏览器自动化页面对象
            
        Returns:
            是否成功点击了链接
        """
        # 模拟鼠标移动
        self.simulate_mouse_movement(page)
        
        # 随机决定是否滚动
        if random.random() < 0.8:  # 80%概率滚动
            self.simulate_scroll(page)
        
        # 随机决定是否点击链接
        if self.should_click():
            try:
                # 尝试找到可点击的元素
                links = page.query_selector_all('a')
                if links and len(links) > 5:
                    # 选择一个随机链接但不是第一个或最后一个
                    link_index = random.randint(1, min(len(links) - 2, 10))
                    link = links[link_index]
                    
                    # 检查元素是否可见
                    if link.is_visible():
                        # 移动到链接
                        rect = link.bounding_box()
                        if rect:
                            center_x = rect['x'] + rect['width'] / 2
                            center_y = rect['y'] + rect['height'] / 2
                            
                            # 生成到链接的路径
                            path = self._calculate_bezier_curve(
                                [(page.mouse.position()['x'], page.mouse.position()['y']),
                                 (center_x, center_y)], 
                                10
                            )
                            
                            # 沿着路径移动
                            for x, y in path:
                                page.mouse.move(x, y)
                                time.sleep(random.uniform(0.01, 0.03))
                            
                            # 轻微晃动
                            page.mouse.move(center_x + random.randint(-3, 3), 
                                          center_y + random.randint(-3, 3))
                            time.sleep(random.uniform(0.05, 0.15))
                            
                            # 这里可以选择只悬停而不实际点击
                            if random.random() < 0.5:
                                page.mouse.click(center_x, center_y)
                                return True
            except Exception as e:
                print(f"[BehaviorSimulator] 链接点击模拟失败: {str(e)}")
        
        return False
    
    def reset_session(self) -> None:
        """重置会话状态"""
        self.current_role = None
        self.session_history = []
        self.current_depth = 0
    
    def get_viewport_size(self, page: Any) -> Dict[str, int]:
        """获取视口尺寸
        
        Args:
            page: 页面对象
            
        Returns:
            包含width和height的字典
        """
        try:
            size = page.viewport_size()
            if size:
                return size
        except Exception:
            pass
        # 默认尺寸
        return {'width': 1920, 'height': 1080}