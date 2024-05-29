# 日志
import logging

# 日志统一输出到uvicorn日志中
log = logging.getLogger("uvicorn") 
log.setLevel(logging.DEBUG)