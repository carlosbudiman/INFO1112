import os
import sys
import json
import datetime 
import re
import typing

today = datetime.date.today().strftime("%d/%m/%y")
three_days_later = today + datetime.timedelta(days=3)
        
print(today)
print(three_days_later)