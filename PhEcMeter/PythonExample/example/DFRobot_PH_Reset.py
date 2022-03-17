import sys
sys.path.append('../')
import time

from modules.DFRobot_PH import DFRobot_PH
ph = DFRobot_PH()

ph.reset()
time.sleep(0.5)
sys.exit(1)