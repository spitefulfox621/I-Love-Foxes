"""
spᴉteƒox preloader
"""
import subprocess, sys

# Check if running in a virtual environment
def in_virtualenv():
    return (
        hasattr(sys, 'real_prefix') or (
            hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
            )

def install_dependencies(dependencies:list):
    print (f"installing dependencies {', '.join(dependencies)}...")
    for dependency in dependencies:
        try:
            __import__(dependency)
        except ImportError:
            subprocess.check_call([sys.executable   , "-m", "pip", "install", dependency])