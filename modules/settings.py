import sys
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from base_utils import BaseUtils

base_utils = BaseUtils(0)

tg_token = os.getenv('BOT_TOKEN')

CurrentSafe = {}
CurrentAction = {}