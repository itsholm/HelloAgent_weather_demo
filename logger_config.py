"""
日志配置模块
统一管理整个项目的日志设置
"""
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

# 标记是否已经初始化过日志系统
_logging_initialized = False


def setup_logger(
    log_level: str = "INFO",
    log_to_file: bool = True,
    log_file: str = "helloagent.log",
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> None:
    """
    配置根 logger，这样所有模块的 logger 都会继承这个配置
    
    参数:
        log_level: 日志级别，可选: DEBUG, INFO, WARNING, ERROR, CRITICAL
        log_to_file: 是否将日志写入文件
        log_file: 日志文件路径
        max_bytes: 单个日志文件的最大大小（字节）
        backup_count: 保留的备份日志文件数量
    """
    global _logging_initialized
    
    # 避免重复初始化
    if _logging_initialized:
        return
    
    # 设置日志级别
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # 获取根 logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # 清除可能存在的旧 handlers（避免重复添加）
    root_logger.handlers.clear()
    
    # 创建格式化器
    # 格式: 时间 - 模块名 - 级别 - 消息
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 1. 控制台处理器（Console Handler）- 总是输出到终端
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 2. 文件处理器（File Handler）- 可选，将日志写入文件
    if log_to_file:
        try:
            # 使用 RotatingFileHandler 实现日志轮转（避免单个文件过大）
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        except Exception as e:
            # 如果文件写入失败（如权限问题），至少保证控制台输出正常
            print(f"警告: 无法创建日志文件 {log_file}: {e}")
    
    _logging_initialized = True
    root_logger.info(f"日志系统已初始化，级别: {log_level}, 文件输出: {log_to_file}")


# 默认配置：从环境变量读取日志级别，如果没有则使用 INFO
# 注意：这里不再自动初始化，需要在 main.py 中显式调用 setup_logger()

