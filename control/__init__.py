"""
JetRacer Control Library

This package provides motor and steering control for the JetRacer platform
using PCA9685 PWM controllers.
"""

from .motors import JetRacer

__all__ = ['JetRacer']
__version__ = '0.1.0'
