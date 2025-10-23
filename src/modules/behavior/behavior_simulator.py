"""行为模拟器模块 - 用于模拟真实用户的浏览行为"""
import random
import time
import math
import psutil
from typing import Dict, Any, Optional, List
from src.config import global_config
from src.modules.intelligence.metacognition_engine import MetacognitionEngine


class BehaviorSimulator:
    """行为模拟器类 - 模拟真实用户的各种浏览行为"""
    
    def __init__(self):
        """初始化行为模拟器"""
        # 配置参数
        self.mouse_movement_enabled = global_config.get('behavior_simulator.mouse_movement_enabled', True)
        self.scrolling_enabled = global_config.get('behavior_simulator.scrolling_enabled', True)
        self.clicking_enabled = global_config.get('behavior_simulator.clicking_enabled', True)
        self.typing_enabled = global_config.get('behavior_simulator.typing_enabled', True)
        self.delay_min = global_config.get('behavior_simulator.delay_min', 1.0)
        self.delay_max = global_config.get('behavior_simulator.delay_max', 3.0)
        
        # 人类行为模型参数
        self.mouse_movement_params = {
            'jitter_intensity': global_config.get('behavior_simulator.mouse.jitter_intensity', 0.5),
            'speed_variation': global_config.get('behavior_simulator.mouse.speed_variation', 0.3),
            'acceleration_factor': global_config.get('behavior_simulator.mouse.acceleration_factor', 0.2),
            'path_complexity': global_config.get('behavior_simulator.mouse.path_complexity', 0.4)
        }
        
        # 上次操作时间，用于计算合理的时间间隔
        self.last_action_time = time.time()
        
        # 元认知相关属性
        self.environment_awareness = {
            'pressure_level': 0.0,  # 0-1, 表示环境压力级别
            'current_efficiency': 0.0,  # 当前效率
            'detection_risk': 0.0  # 检测风险
        }
        
        # 行为模式 - 默认为普通浏览
        self.behavior_pattern = 'normal'  # normal, careful, hurried, stealth
        
        # 行为历史记录
        self.action_history = []
        self.last_pattern_change = time.time()
        
        # 加载行为模式参数
        self._load_behavior_patterns()
        
        # 元认知引擎集成
        self.metacognition = MetacognitionEngine()
        
        # 资源监控配置
        self.resource_monitor_interval = 10  # 秒
        
        # 启动资源监控
        self._start_resource_monitor()
        
        # 同步行为模式
        self.behavior_pattern = self.metacognition.current_behavior_pattern
    
    def human_delay(self, min_delay: Optional[float] = None, max_delay: Optional[float] = None, context: Optional[Dict[str, Any]] = None) -> None:
        """模拟人类操作的时间间隔
        
        Args:
            min_delay: 最小延迟时间（秒）
            max_delay: 最大延迟时间（秒）
            context: 上下文信息，用于元认知决策
        """
        # 根据上下文更新环境感知
        if context:
            self._update_environment_awareness(context)
        
        # 执行元认知优化的行为模式选择
        self._select_optimized_behavior_pattern()
        
        # 获取当前行为模式的参数
        pattern_params = self.pattern_parameters.get(self.behavior_pattern, self.pattern_parameters['normal'])
        
        # 基础延迟参数
        min_d = min_delay or self.delay_min
        max_d = max_delay or self.delay_max
        
        # 根据行为模式调整延迟
        min_d *= pattern_params['delay_multiplier']
        max_d *= pattern_params['delay_multiplier']
        
        # 根据环境风险调整延迟
        risk = self.environment_awareness['detection_risk']
        if risk > 0.7:
            min_d *= 1.5
            max_d *= 2.0
        elif risk > 0.4:
            min_d *= 1.2
            max_d *= 1.5
        
        # 计算自上次操作以来的时间
        current_time = time.time()
        elapsed = current_time - self.last_action_time
        
        # 如果时间间隔太短，添加适当的延迟
        if elapsed < min_d:
            delay = random.uniform(min_d - elapsed, max_d - elapsed)
            # 添加注意力变异性
            attention_factor = 1.0 + random.uniform(-pattern_params['attention_variability'], pattern_params['attention_variability'])
            delay = delay * attention_factor
            time.sleep(delay)
        elif elapsed < max_d:
            # 如果在合理范围内，可以选择不等待
            if random.random() < pattern_params['pattern_consistency']:
                pass
            else:
                delay = random.uniform(0, max_d - elapsed)
                time.sleep(delay)
        
        # 更新上次操作时间
        self.last_action_time = time.time()
        
        # 记录动作
        self._record_action('delay', time.time() - current_time)
    
    def generate_mouse_path(self, start_x: int, start_y: int, end_x: int, end_y: int, steps: int = 50) -> list:
        """生成更真实的鼠标移动路径
        
        使用贝塞尔曲线和噪声生成真实的人类鼠标移动路径
        
        Args:
            start_x: 起始X坐标
            start_y: 起始Y坐标
            end_x: 目标X坐标
            end_y: 目标Y坐标
            steps: 路径步数
            
        Returns:
            路径坐标列表 [(x1, y1), (x2, y2), ...]
        """
        # 获取当前行为模式的参数
        pattern_params = self.pattern_parameters.get(self.behavior_pattern, self.pattern_parameters['normal'])
        
        path = []
        
        # 计算距离和方向
        dx = end_x - start_x
        dy = end_y - start_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # 基于距离调整步数
        adjusted_steps = int(min(steps, max(10, distance / 5)))
        
        # 根据行为模式调整路径复杂度
        complexity_factor = pattern_params.get('path_complexity_multiplier', 1.0)
        jitter_factor = self.mouse_movement_params['jitter_intensity'] * complexity_factor
        
        # 生成控制点（使路径更自然）
        cp1_x = start_x + dx * random.uniform(0.2, 0.4) + random.uniform(-50 * complexity_factor, 50 * complexity_factor)
        cp1_y = start_y + dy * random.uniform(0.2, 0.4) + random.uniform(-50 * complexity_factor, 50 * complexity_factor)
        cp2_x = start_x + dx * random.uniform(0.6, 0.8) + random.uniform(-50 * complexity_factor, 50 * complexity_factor)
        cp2_y = start_y + dy * random.uniform(0.6, 0.8) + random.uniform(-50 * complexity_factor, 50 * complexity_factor)
        
        # 生成贝塞尔曲线点
        for i in range(adjusted_steps + 1):
            t = i / adjusted_steps
            
            # 贝塞尔曲线公式
            x = ((1-t)**3 * start_x) + (3*(1-t)**2 * t * cp1_x) + (3*(1-t)*t**2 * cp2_x) + (t**3 * end_x)
            y = ((1-t)**3 * start_y) + (3*(1-t)**2 * t * cp1_y) + (3*(1-t)*t**2 * cp2_y) + (t**3 * end_y)
            
            # 添加随机抖动（更真实的人类移动）
            jitter_x = random.gauss(0, jitter_factor * 10)
            jitter_y = random.gauss(0, jitter_factor * 10)
            
            # 根据移动阶段调整抖动
            if t < 0.2 or t > 0.8:
                # 开始和结束阶段抖动更大
                jitter_x *= 1.5
                jitter_y *= 1.5
            
            # 添加加速度和减速度效果
            speed_factor = 1.0
            if t < 0.3:
                # 加速阶段
                speed_factor = t / 0.3 * self.mouse_movement_params['acceleration_factor'] + 1.0
            elif t > 0.7:
                # 减速阶段
                speed_factor = (1.0 - t) / 0.3 * self.mouse_movement_params['acceleration_factor'] + 1.0
            
            # 应用速度变化
            speed_variation = random.gauss(1.0, self.mouse_movement_params['speed_variation'])
            final_x = x + jitter_x * speed_variation * speed_factor
            final_y = y + jitter_y * speed_variation * speed_factor
            
            # 确保坐标合理
            final_x = max(0, final_x)
            final_y = max(0, final_y)
            
            # 添加错误（根据行为模式）
            if random.random() < pattern_params['error_probability']:
                # 模拟错误移动（偏离目标）
                error_x = random.uniform(-10, 10)
                error_y = random.uniform(-10, 10)
                final_x += error_x
                final_y += error_y
            
            path.append((int(final_x), int(final_y)))
        
        # 添加一些随机的小停顿
        pause_count = min(2, max(0, len(path) // 5))
        # 根据行为模式调整停顿
        if self.behavior_pattern == 'careful' or self.behavior_pattern == 'stealth':
            pause_count = min(3, pause_count + 1)
        elif self.behavior_pattern == 'hurried':
            pause_count = max(0, pause_count - 1)
        
        if pause_count > 0:
            pause_points = random.sample(range(1, len(path)-1), pause_count)
            for point_idx in pause_points:
                # 在停顿点重复几次坐标，模拟短暂停留
                for _ in range(random.randint(2, 5)):
                    path.insert(point_idx, path[point_idx])
        
        return path
    
    def simulate_page_interaction(self, page, context: Optional[Dict[str, Any]] = None, detailed: bool = False, duration: Optional[float] = None) -> None:
        """模拟页面交互行为
        
        Args:
            page: Playwright页面对象或其他页面控制器
            context: 上下文信息，用于元认知决策
            detailed: 是否执行详细交互（更接近人类行为）
            duration: 交互持续时间（秒）
        """
        try:
            # 根据上下文更新环境感知
            if context:
                self._update_environment_awareness(context)
            
            # 随机选择交互类型
            interaction_types = []
            if self.mouse_movement_enabled:
                interaction_types.append('move')
            if self.scrolling_enabled:
                interaction_types.append('scroll')
            if self.clicking_enabled:
                interaction_types.append('click')
            if self.typing_enabled:
                interaction_types.append('type')
            
            if not interaction_types:
                return
            
            # 根据行为模式调整交互参数
            pattern_params = self.pattern_parameters.get(self.behavior_pattern, self.pattern_parameters['normal'])
            
            # 基础交互数量
            base_min, base_max = 1, 3
            
            # 详细模式下增加交互复杂度和数量
            if detailed:
                base_min, base_max = 3, 6
            
            # 调整交互数量
            if self.behavior_pattern == 'hurried':
                base_min, base_max = 1, 2
            elif self.behavior_pattern == 'careful' or self.behavior_pattern == 'stealth':
                base_min, base_max = 2, 4
            
            # 执行不同的交互行为
            num_interactions = random.randint(base_min, base_max)
            selected_interactions = random.sample(interaction_types, min(num_interactions, len(interaction_types)))
            
            # 对于高风险环境，增加移动和滚动，减少点击和输入
            risk = self.environment_awareness['detection_risk']
            if risk > 0.7:
                # 移除或减少可能引起注意的交互
                if 'click' in selected_interactions:
                    selected_interactions.remove('click')
                if 'type' in selected_interactions:
                    selected_interactions.remove('type')
                # 确保至少有一个交互
                if not selected_interactions and interaction_types:
                    selected_interactions = ['move']
            
            # 如果指定了持续时间，分配给每个交互
            total_duration = 0
            if duration is not None:
                # 计算每个交互的平均时间
                avg_duration = duration / len(selected_interactions)
            else:
                avg_duration = None
            
            for i, interaction in enumerate(selected_interactions):
                start_time = time.time()
                
                if interaction == 'move':
                    self._simulate_mouse_movement(page)
                elif interaction == 'scroll':
                    self._simulate_scrolling(page)
                elif interaction == 'click':
                    self._simulate_clicking(page)
                elif interaction == 'type':
                    self._simulate_typing(page)
                
                # 记录交互
                self._record_action('interaction', interaction)
                
                # 调整交互间隔，确保在指定时间内完成
                if avg_duration is not None:
                    elapsed = time.time() - start_time
                    if elapsed < avg_duration and i < len(selected_interactions) - 1:
                        # 在交互之间添加延迟
                        time.sleep(avg_duration - elapsed)
                        total_duration += avg_duration
                    else:
                        total_duration += elapsed
            
            # 详细模式下添加额外的随机小动作为人体验证
            if detailed and random.random() < 0.6:
                # 添加一些微小的鼠标移动和停顿
                for _ in range(random.randint(2, 5)):
                    self._simulate_mouse_movement(page)
                    self.human_delay(0.1, 0.3)
                    
                # 模拟短暂的视线停留（如阅读某处内容）
                if random.random() < 0.5:
                    self.human_delay(1.0, 3.0)
                
                # 交互之间的延迟（根据行为模式调整）
                delay_min = 0.5 * pattern_params['delay_multiplier']
                delay_max = 2.0 * pattern_params['delay_multiplier']
                self.human_delay(delay_min, delay_max, context)
                
        except Exception as e:
            # 交互模拟失败不应影响主要功能
            print(f"[PhantomCrawler] 行为模拟出错: {e}")
    
    def _simulate_mouse_movement(self, page) -> None:
        """模拟鼠标移动
        
        Args:
            page: Playwright页面对象
        """
        try:
            # 获取页面尺寸
            viewport = page.viewport_size
            if not viewport:
                viewport = {'width': 1920, 'height': 1080}
            
            # 生成随机起始和结束位置
            start_x = random.randint(viewport['width'] // 4, viewport['width'] * 3 // 4)
            start_y = random.randint(viewport['height'] // 4, viewport['height'] * 3 // 4)
            end_x = random.randint(viewport['width'] // 4, viewport['width'] * 3 // 4)
            end_y = random.randint(viewport['height'] // 4, viewport['height'] * 3 // 4)
            
            # 生成移动路径
            path = self.generate_mouse_path(start_x, start_y, end_x, end_y)
            
            # 执行移动
            page.mouse.move(start_x, start_y)
            
            # 按照路径移动鼠标
            pattern_params = self.pattern_parameters.get(self.behavior_pattern, self.pattern_parameters['normal'])
            base_delay = random.uniform(0.005, 0.02)
            
            # 根据行为模式调整移动速度
            speed_multiplier = 1.0
            if self.behavior_pattern == 'hurried':
                speed_multiplier = 1.5
            elif self.behavior_pattern == 'careful' or self.behavior_pattern == 'stealth':
                speed_multiplier = 0.8
            
            for x, y in path[1:]:
                # 根据模式调整延迟
                move_delay = base_delay / speed_multiplier
                # 添加注意力变异性
                move_delay *= 1.0 + random.uniform(-pattern_params['attention_variability'], pattern_params['attention_variability'])
                
                time.sleep(move_delay)
                page.mouse.move(x, y)
                
            # 可能的短暂停留
            if random.random() < 0.3:
                time.sleep(random.uniform(0.1, 0.5))
                
        except Exception:
            pass
    
    def _simulate_scrolling(self, page) -> None:
        """模拟页面滚动
        
        Args:
            page: Playwright页面对象
        """
        try:
            # 滚动模式：均匀滚动、快速滚动、慢速滚动、随机滚动
            scroll_mode = random.choice(['uniform', 'fast', 'slow', 'random'])
            
            # 获取页面总高度
            total_height = page.evaluate("() => document.body.scrollHeight || document.documentElement.scrollHeight")
            viewport_height = page.evaluate("() => window.innerHeight")
            
            if total_height <= viewport_height:
                return  # 页面太短，不需要滚动
            
            # 确定滚动范围（不滚动到页面底部）
            max_scroll = min(total_height - viewport_height, viewport_height * 3)
            
            if scroll_mode == 'uniform':
                # 均匀滚动
                steps = random.randint(3, 8)
                for i in range(steps):
                    scroll_position = int(max_scroll * (i / steps))
                    page.evaluate(f"window.scrollTo(0, {scroll_position})")
                    self.human_delay(0.3, 0.8)
                    
            elif scroll_mode == 'fast':
                # 快速滚动
                scroll_position = random.randint(int(max_scroll * 0.2), int(max_scroll * 0.8))
                page.evaluate(f"window.scrollTo(0, {scroll_position})")
                
            elif scroll_mode == 'slow':
                # 慢速滚动
                start_pos = random.randint(0, int(max_scroll * 0.3))
                end_pos = random.randint(int(max_scroll * 0.7), int(max_scroll))
                steps = random.randint(10, 20)
                
                for i in range(steps + 1):
                    t = i / steps
                    # 缓动函数使滚动更自然
                    eased_t = t * t * (3 - 2 * t)  # 缓入缓出
                    scroll_position = int(start_pos + (end_pos - start_pos) * eased_t)
                    page.evaluate(f"window.scrollTo(0, {scroll_position})")
                    time.sleep(random.uniform(0.1, 0.2))
                    
            elif scroll_mode == 'random':
                # 随机滚动 - 最接近真实用户
                scroll_sequence = []
                current_pos = 0
                
                # 生成随机滚动序列
                for _ in range(random.randint(5, 15)):
                    # 随机滚动量和方向
                    scroll_amount = random.randint(int(viewport_height * 0.1), int(viewport_height * 0.5))
                    if random.random() > 0.3 and current_pos > 0:  # 30%概率向上滚动
                        scroll_amount = -scroll_amount
                    
                    new_pos = max(0, min(max_scroll, current_pos + scroll_amount))
                    if new_pos != current_pos:  # 避免无效滚动
                        scroll_sequence.append(new_pos)
                        current_pos = new_pos
                
                # 执行滚动序列
                for pos in scroll_sequence:
                    page.evaluate(f"window.scrollTo(0, {pos})")
                    self.human_delay(0.2, 0.8)
            
            # 最终回到页面顶部的概率较低
            if random.random() < 0.2:
                page.evaluate("window.scrollTo(0, 0)")
                
        except Exception:
            pass
    
    def _simulate_clicking(self, page) -> None:
        """模拟鼠标点击
        
        Args:
            page: Playwright页面对象
        """
        try:
            # 寻找可点击的元素
            clickable_selector = random.choice([
                'button:not([disabled])',
                'a[href]:not([disabled])',
                'input[type="submit"]:not([disabled])',
                'input[type="button"]:not([disabled])',
                'div[role="button"]:not([disabled])',
                '.clickable:not([disabled])',
                '.button:not([disabled])',
                '[onclick]'
            ])
            
            # 评估是否有匹配的元素
            has_clickable = page.evaluate(f"() => document.querySelector('{clickable_selector}') !== null")
            
            if has_clickable:
                # 获取元素位置
                js_code = '''
                () => {
                    const el = document.querySelector('%s');
                    const rect = el.getBoundingClientRect();
                    return { x: rect.left + rect.width / 2, y: rect.top + rect.height / 2, width: rect.width, height: rect.height };
                }
                ''' % clickable_selector
                element_bounds = page.evaluate(js_code)
                
                # 稍微偏移点击位置，更真实
                click_x = element_bounds['x'] + random.randint(-int(element_bounds['width'] * 0.2), int(element_bounds['width'] * 0.2))
                click_y = element_bounds['y'] + random.randint(-int(element_bounds['height'] * 0.2), int(element_bounds['height'] * 0.2))
                
                # 移动到元素位置
                viewport = page.viewport_size
                if click_x > 0 and click_x < viewport['width'] and click_y > 0 and click_y < viewport['height']:
                    page.mouse.move(click_x, click_y)
                    
                    # 微小停顿
                    time.sleep(random.uniform(0.1, 0.3))
                    
                    # 模拟真实点击（按下和释放之间有微小延迟）
                    page.mouse.down()
                    time.sleep(random.uniform(0.05, 0.15))
                    page.mouse.up()
                    
        except Exception:
            # 如果找不到可点击元素或点击失败，随机点击页面某处
            try:
                viewport = page.viewport_size
                random_x = random.randint(viewport['width'] // 4, viewport['width'] * 3 // 4)
                random_y = random.randint(viewport['height'] // 4, viewport['height'] * 3 // 4)
                
                page.mouse.move(random_x, random_y)
                time.sleep(random.uniform(0.1, 0.3))
                page.mouse.click(random_x, random_y)
                
            except Exception:
                pass
    
    def _simulate_typing(self, page) -> None:
        """模拟键盘输入
        
        Args:
            page: Playwright页面对象
        """
        try:
            # 寻找可输入的元素
            input_selector = random.choice([
                'input[type="text"]:not([disabled])',
                'input[type="search"]:not([disabled])',
                'input[type="email"]:not([disabled])',
                'textarea:not([disabled])',
                '[contenteditable="true"]'
            ])
            
            # 检查是否有可输入元素
            has_input = page.evaluate(f"() => document.querySelector('{input_selector}') !== null")
            
            if has_input:
                # 生成随机文本（基于上下文）
                input_type = page.evaluate(f"() => document.querySelector('{input_selector}').type || 'text'")
                
                if input_type == 'search':
                    # 搜索框输入
                    search_queries = [
                        'how to use python',
                        'latest news',
                        'weather today',
                        'programming tips',
                        'best practices',
                        'what is AI',
                        'data science tutorials'
                    ]
                    text_to_type = random.choice(search_queries)
                    
                elif input_type == 'email':
                    # 邮箱输入
                    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'example.com']
                    username = 'user' + str(random.randint(1000, 9999))
                    text_to_type = f"{username}@{random.choice(domains)}"
                    
                else:
                    # 普通文本
                    text_samples = [
                        'Hello world',
                        'This is a test',
                        'Just exploring',
                        'Interesting content',
                        'Looking for information'
                    ]
                    text_to_type = random.choice(text_samples)
                
                # 聚焦到输入框
                page.evaluate(f"document.querySelector('{input_selector}').focus()")
                
                # 逐字输入，模拟真实打字速度
                for char in text_to_type:
                    page.keyboard.press(char)
                    
                    # 打字速度变化
                    base_delay = 0.05 + random.random() * 0.1  # 基础速度
                    
                    # 偶尔的打字错误和修正
                    if random.random() < 0.05:  # 5%概率打错
                        wrong_char = chr(ord(char) + random.randint(-3, 3))
                        page.keyboard.press(wrong_char)
                        time.sleep(base_delay * 0.5)
                        page.keyboard.press('Backspace')  # 删除错误字符
                    
                    # 添加延迟
                    time.sleep(base_delay)
                
                # 可能的提交操作
                if random.random() < 0.3 and input_type in ['search', 'text']:
                    time.sleep(random.uniform(0.3, 0.8))
                    page.keyboard.press('Enter')
                    
        except Exception:
            pass
    
    def simulate_reading_behavior(self, page, duration: Optional[float] = None) -> None:
        """模拟阅读行为
        
        Args:
            page: Playwright页面对象
            duration: 阅读持续时间（秒），如果不提供则根据内容动态计算
        """
        try:
            # 获取页面复杂度和内容丰富度
            content_metrics = page.evaluate('''() => {
                const paragraphs = Array.from(document.querySelectorAll('p')).filter(p => p.textContent.length > 20);
                const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'));
                const totalWords = document.body.textContent ? document.body.textContent.split(/\\s+/).length : 0;
                return {
                    paragraphs: paragraphs.length,
                    headings: headings.length,
                    wordCount: totalWords,
                    hasImages: document.querySelectorAll('img').length > 0
                };
            }''')
            
            # 初始滚动行为
            self._simulate_scrolling(page)
            
            # 根据指定的持续时间或内容复杂度计算阅读时间
            if duration is None:
                # 基于内容自动计算
                base_time = max(3.0, min(15.0, content_metrics['wordCount'] / 150))  # 假设平均阅读速度
                if content_metrics['hasImages']:
                    base_time *= 1.2  # 有图片时增加阅读时间
                duration = base_time
            
            # 阅读分阶段进行
            stages = random.randint(2, 4)
            stage_duration = duration / stages
            
            for stage in range(stages):
                # 阶段1：快速浏览
                if stage == 0:
                    # 滚动到页面25%的位置
                    page.evaluate('window.scrollTo(0, document.body.scrollHeight * 0.25)')
                    self.human_delay(stage_duration * 0.5)
                    
                    # 轻微的鼠标移动
                    if random.random() < 0.7:
                        self._simulate_mouse_movement(page)
                
                # 阶段2-3：深入阅读特定段落
                elif content_metrics['paragraphs'] > 0:
                    # 随机选择一个段落
                    para_index = random.randint(0, min(content_metrics['paragraphs'] - 1, 5))
                    
                    # 滚动到段落位置
                    js_code = '''
                    () => {
                        const paragraphs = Array.from(document.querySelectorAll('p')).filter(p => p.textContent.length > 20);
                        if (paragraphs[%d]) {
                            paragraphs[%d].scrollIntoView({ behavior: 'smooth', block: 'center' });
                        }
                    }
                    ''' % (para_index, para_index)
                    page.evaluate(js_code)
                    
                    # 停留阅读
                    self.human_delay(stage_duration * 0.7)
                    
                    # 模拟阅读时的鼠标悬停在重点内容上
                    if random.random() < 0.6:
                        self._simulate_mouse_movement(page)
                        
                        # 随机选择页面上的某个文本区域悬停
                        hover_js = '''
                        () => {
                            const elements = Array.from(document.querySelectorAll('p, h2, h3')).filter(el => el.textContent.length > 10);
                            if (elements.length > 0) {
                                const randomEl = elements[Math.floor(Math.random() * elements.length)];
                                const rect = randomEl.getBoundingClientRect();
                                return { x: rect.left + rect.width * 0.3, y: rect.top + rect.height * 0.5 };
                            }
                            return { x: window.innerWidth / 2, y: window.innerHeight / 2 };
                        }
                        '''
                        hover_pos = page.evaluate(hover_js)
                        page.mouse.move(hover_pos['x'], hover_pos['y'])
                        self.human_delay(0.5, 1.5)
                
                # 阶段4：浏览到底部或其他部分
                else:
                    # 滚动到页面随机位置
                    scroll_percent = random.uniform(0.5, 0.9)
                    page.evaluate(f'window.scrollTo(0, document.body.scrollHeight * {scroll_percent})')
                    self.human_delay(stage_duration)
            
            # 模拟用户可能的返回顶部行为
            if random.random() < 0.3:
                page.evaluate('window.scrollTo({ top: 0, behavior: "smooth" })')
                self.human_delay(0.5, 1.0)
                    
        except Exception:
            pass
    
    def get_behavior_statistics(self) -> Dict[str, Any]:
        """获取行为模拟的统计信息
        
        Returns:
            行为统计信息字典
        """
        # 计算平均延迟
        delays = [a['value'] for a in self.action_history if a['type'] == 'delay']
        avg_delay = sum(delays) / len(delays) if delays else (self.delay_min + self.delay_max) / 2
        
        # 计算交互次数统计
        interactions = [a['value'] for a in self.action_history if a['type'] == 'interaction']
        interaction_counts = {}
        for interaction in interactions:
            interaction_counts[interaction] = interaction_counts.get(interaction, 0) + 1
        
        # 获取元认知洞察
        metacognitive_insights = self.metacognition.get_metacognitive_insights()
        
        return {
            'mouse_movement_enabled': self.mouse_movement_enabled,
            'scrolling_enabled': self.scrolling_enabled,
            'clicking_enabled': self.clicking_enabled,
            'typing_enabled': self.typing_enabled,
            'average_delay': avg_delay,
            'mouse_parameters': self.mouse_movement_params,
            'current_pattern': self.behavior_pattern,
            'environment_awareness': metacognitive_insights['system_state'],
            'interaction_statistics': interaction_counts,
            'actions_performed': len(self.action_history),
            'last_pattern_change': time.time() - self.last_pattern_change,
            'recommendations': metacognitive_insights['recommendations'],
            'best_strategies': metacognitive_insights['best_strategies']
        }
        
    def shutdown(self):
        """关闭模拟器并清理资源"""
        print("[BehaviorSimulator] 正在关闭行为模拟器...")
        # 确保元认知引擎正确关闭并保存知识
        self.metacognition.shutdown()
        print("[BehaviorSimulator] 行为模拟器已关闭")
    
    def _load_behavior_patterns(self):
        """加载不同行为模式的参数"""
        self.pattern_parameters = {
            'normal': {
                'delay_multiplier': 1.0,
                'error_probability': 0.02,
                'attention_variability': 0.1,
                'pattern_consistency': 0.8,
                'path_complexity_multiplier': 1.0
            },
            'careful': {
                'delay_multiplier': 1.5,
                'error_probability': 0.01,
                'attention_variability': 0.05,
                'pattern_consistency': 0.95,
                'path_complexity_multiplier': 1.2
            },
            'hurried': {
                'delay_multiplier': 0.6,
                'error_probability': 0.05,
                'attention_variability': 0.2,
                'pattern_consistency': 0.6,
                'path_complexity_multiplier': 0.8
            },
            'stealth': {
                'delay_multiplier': 1.8,
                'error_probability': 0.005,
                'attention_variability': 0.25,
                'pattern_consistency': 0.3,
                'path_complexity_multiplier': 1.5,
                'human_likeness': 0.95
            }
        }
    
    def _update_environment_awareness(self, context: Dict[str, Any]):
        """根据上下文更新环境感知并同步到元认知引擎"""
        # 更新本地环境感知状态
        # 检测风险评估
        if context.get('blocked', False):
            self.environment_awareness['detection_risk'] = min(1.0, self.environment_awareness['detection_risk'] + 0.3)
        elif context.get('success', False):
            self.environment_awareness['detection_risk'] = max(0.0, self.environment_awareness['detection_risk'] - 0.1)
        
        # 环境压力评估
        recent_failures = context.get('recent_failures', 0)
        self.environment_awareness['pressure_level'] = min(1.0, recent_failures * 0.2)
        
        # 效率评估
        response_time = context.get('response_time', 3.0)
        if response_time < 1.0:
            self.environment_awareness['current_efficiency'] = 0.9
        elif response_time < 3.0:
            self.environment_awareness['current_efficiency'] = 0.7
        elif response_time < 5.0:
            self.environment_awareness['current_efficiency'] = 0.5
        else:
            self.environment_awareness['current_efficiency'] = 0.3
        
        # 同步到元认知引擎
        # 更新检测风险
        self.metacognition.environment_awareness['detection_risk'] = self.environment_awareness['detection_risk']
        
        # 更新系统性能指标
        self.metacognition.environment_awareness['system_performance']['avg_response_time'] = response_time
        
        # 如果有URL，分析爬取结果
        if 'url' in context and 'result' in context:
            # 准备策略信息
            strategies_used = context.get('strategies', {})
            
            # 调用元认知引擎分析结果
            self.metacognition.analyze_crawl_result(
                url=context['url'],
                result=context['result'],
                strategies_used=strategies_used
            )
        
        # 基于元认知引擎的洞察更新本地状态
        insights = self.metacognition.get_metacognitive_insights()
        
        # 更新本地行为模式
        if 'current_behavior_pattern' in insights['system_state']:
            new_pattern = insights['system_state']['current_behavior_pattern']
            if new_pattern != self.behavior_pattern:
                current_time = time.time()
                # 避免过于频繁的模式切换（至少间隔3分钟）
                if current_time - self.last_pattern_change > 180:
                    self.behavior_pattern = new_pattern
                    self.last_pattern_change = current_time
                    self.logger.info(f"基于元认知洞察自动切换行为模式至: {new_pattern}")
        
        # 更新本地检测风险（以元认知引擎的评估为准）
        if 'detection_risk' in insights['system_state']:
            self.environment_awareness['detection_risk'] = insights['system_state']['detection_risk']
    
    def _select_optimized_behavior_pattern(self):
        """基于元认知分析选择优化的行为模式"""
        # 使用元认知引擎进行决策
        insights = self.metacognition.get_metacognitive_insights()
        new_pattern = insights['system_state']['current_behavior_pattern']
        
        # 模式变更时间限制，避免频繁切换
        current_time = time.time()
        if current_time - self.last_pattern_change < 300:  # 5分钟内不频繁切换
            return
        
        # 只在必要时更改模式
        if new_pattern != self.behavior_pattern:
            self.behavior_pattern = new_pattern
            self.last_pattern_change = current_time
            print(f"[BehaviorSimulator] 基于元认知洞察切换行为模式至: {new_pattern}")
            
            # 检查是否有紧急建议
            for recommendation in insights['recommendations']:
                if recommendation['level'] == 'critical':
                    print(f"[BehaviorSimulator] 紧急建议: {recommendation['message']}")
                    print(f"[BehaviorSimulator] 建议行动: {recommendation['action']}")
    
    def _record_action(self, action_type: str, action_value: Any):
        """记录行为动作以便分析模式"""
        now = time.time()
        self.action_history.append({
            'type': action_type,
            'value': action_value,
            'timestamp': now,
            'pattern': self.behavior_pattern
        })
        
        # 保留最近100个动作
        if len(self.action_history) > 100:
            self.action_history = self.action_history[-100:]
    
    def shift_behavior_pattern(self):
        """切换到不同的行为模式，用于规避检测"""
        # 使用元认知引擎的行为模式切换功能
        self.metacognition.shift_behavior_pattern()
        new_pattern = self.metacognition.current_behavior_pattern
        
        # 同步本地模式
        self.behavior_pattern = new_pattern
        self.last_pattern_change = time.time()
        print(f"[BehaviorSimulator] 执行行为模式切换: {self.behavior_pattern}")
        
    def _start_resource_monitor(self):
        """启动资源监控线程"""
        import threading
        
        def monitor_resources():
            while True:
                try:
                    # 获取当前进程资源使用情况
                    process = psutil.Process()
                    with process.oneshot():
                        cpu_percent = process.cpu_percent(interval=0.1) / psutil.cpu_count()
                        memory_percent = process.memory_percent()
                    
                    # 获取网络IO（简化版）
                    net_io = psutil.net_io_counters()
                    network_usage = min(net_io.bytes_sent + net_io.bytes_recv, 1024*1024*100) / (1024*1024*100)  # 假设100MB/s为满负荷
                    
                    # 更新元认知引擎的资源压力
                    self.metacognition.update_resource_usage(
                        cpu=min(cpu_percent/100, 1.0),
                        memory=min(memory_percent/100, 1.0),
                        network=min(network_usage, 1.0)
                    )
                    
                    time.sleep(self.resource_monitor_interval)
                except Exception as e:
                    print(f"[BehaviorSimulator] 资源监控出错: {e}")
                    time.sleep(self.resource_monitor_interval)
        
        # 启动守护线程
        monitor_thread = threading.Thread(target=monitor_resources, daemon=True)
        monitor_thread.start()
        print("[BehaviorSimulator] 资源监控线程已启动")