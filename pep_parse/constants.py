import datetime as dt
from pathlib import Path


DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
BASE_DIR = Path(__file__).parent.parent
FILE_NAME = f'status_summary_{dt.datetime.now().strftime(DATETIME_FORMAT)}.csv'
