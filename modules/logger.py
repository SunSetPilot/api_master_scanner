import os
import sys
import logging
import colorlog
import platform
import logging.handlers

import config.settings


class Logger(logging.Logger):

    def __init__(self, level) -> None:
        # 系统类型
        os_system = platform.system()
        # 是否在终端中使用带色日志
        use_color = True
        if os_system == "Darwin":
            logger_file = "/tmp/{project_name}/debug.log".format(
                project_name=config.settings.project_name
            )
        else:
            logger_file = "/tmp/logs/{project_name}.log".format(project_name=config.settings.project_name)

        # 创建日志文件
        logging.Logger.__init__(self, logger_file)
        try:
            os.makedirs(os.path.dirname(logger_file))
        except OSError:
            pass

        log_format = logging.Formatter(
            "[%(asctime)s] [" + config.settings.project_name + "] [%(levelname)s] %(filename)s [line:%(lineno)d] %(message)s")

        # 判断执行输出流是否是终端/MAC OS，是则直接显示日志
        if sys.stdout.isatty() or os_system == "Darwin":
            try:
                if use_color:
                    log_colors = {
                        'DEBUG': 'white',
                        'INFO': 'blue',
                        'WARNING': 'yellow',
                        'ERROR': 'red',
                        'CRITICAL': 'bold_red',
                    }

                    log_style = "%(log_color)s[%(asctime)s] [" \
                                + config.settings.project_name + \
                                "] [%(levelname)s] %(filename)s [line:%(lineno)d] %(message)s%(reset)s"
                    log_format = colorlog.ColoredFormatter(fmt=log_style, log_colors=log_colors, reset=True)
                    console_handler = logging.StreamHandler(sys.stdout)
                    console_handler.setLevel(level)
                    console_handler.setFormatter(log_format)
                    self.addHandler(console_handler)
                else:
                    console_handler = logging.StreamHandler(sys.stdout)
                    console_handler.setLevel(level)
                    console_handler.setFormatter(log_format)
                    self.addHandler(console_handler)
            except Exception as reason:
                self.error("%s" % reason)

        # 每个日志最大100M，最多备份1个日志
        try:
            handler = logging.handlers.RotatingFileHandler(
                filename=logger_file,
                mode="a",
                maxBytes=100 * 1024 * 1024,
                backupCount=1,
                encoding="UTF8" or None,
                delay=False
            )
            handler.setLevel(level)
            handler.setFormatter(log_format)
            self.addHandler(handler)
        except Exception as reason:
            self.error("%s" % reason)


logger = Logger(level=config.settings.log_level)
