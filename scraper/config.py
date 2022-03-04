import os
import logging
from datetime import datetime
import sys

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Setup logger
a_logger = logging.getLogger()
a_logger.setLevel(logging.INFO)

output_file_handler = logging.FileHandler(
    '%s/logs/%s.log' % (path, str(datetime.now().strftime("%d-%b-%Y (%H-%M-%S.%f)"))))
stdout_handler = logging.StreamHandler(sys.stdout)

a_logger.addHandler(output_file_handler)
a_logger.addHandler(stdout_handler)
