import os
import logging
from time import time, sleep
#import psycopg2
import MySQLdb

check_timeout = os.getenv("MYSQL_CHECK_TIMEOUT", 30)
check_interval = os.getenv("MYSQL_CHECK_INTERVAL", 1)
interval_unit = "second" if check_interval == 1 else "seconds"

config = {
	"dbname": os.getenv("MYSQL_DATABASE", "mysql_data"),
	"user": os.getenv("MYSQL_USER", "sa"),
	"password": os.getenv("MYSQL_PASSWORD", "***REMOVED***"),
	"host": os.getenv("DATABASE_URL", "mysql")
}

start_time = time()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def mysql_isready(host, user, password, dbname):
	while time() - start_time < check_timeout:
		try:

			conn = MySQLdb.connect(host=host, user=user, passwd=password, db=dbname)
			#conn = psycopg2.connect(**vars())
			logger.info("MySql is ready! ✨ 💅")
			conn.close()
			return True
		except MySQLdb.OperationalError:
			logger.info(f"MySql isn't ready. Waiting for {check_interval} {interval_unit}...")
			sleep(check_interval)

	logger.error(f"We could not connect to MySql within {check_timeout} seconds.")
	return False


mysql_isready(**config)
