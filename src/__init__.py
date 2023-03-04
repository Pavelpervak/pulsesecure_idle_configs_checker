"""
ICS Idle Config using XML Backup
"""
import logging
from .iconfig.config import ICSIdleConfig
from .iconfig.rspolicy import ICSRSPolicy
from .iconfig.rsprofile import ICSRSProfile
from .idelete.xcoperation import ICSXCOperation

logging.getLogger(__name__).addHandler(logging.NullHandler())
