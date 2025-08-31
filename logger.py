import logging
import sys
from typing import Optional


def setup_logger(name: str = "mcps", level: Optional[str] = None) -> logging.Logger:
    """设置并返回配置好的日志记录器
    
    Args:
        name: 日志记录器名称
        level: 日志级别，默认为 INFO
        
    Returns:
        配置好的日志记录器实例
    """
    # 创建日志记录器
    logger = logging.getLogger(name)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 设置日志级别
    log_level = getattr(logging, level.upper()) if level else logging.INFO
    logger.setLevel(log_level)
    
    # 创建控制台处理器（输出到 stdout，Docker 可以捕获）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # 添加处理器到日志记录器
    logger.addHandler(console_handler)
    
    # 防止日志向上传播到根记录器
    logger.propagate = False
    
    return logger


# 创建默认的日志记录器实例
default_logger = setup_logger("mcps")


def get_logger(name: str = None) -> logging.Logger:
    """获取日志记录器实例
    
    Args:
        name: 日志记录器名称，如果为 None 则返回默认记录器
        
    Returns:
        日志记录器实例
    """
    if name is None:
        return default_logger
    return setup_logger(name) 