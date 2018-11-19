from database_manager import DatabaseManager
from applications_database import applications_database_migration_plan

dbname = os.environ['DBM_DBNAME']
user = os.environ['DBM_USER']
host=os.environ['DBM_HOST']
password=os.environ['DBM_PASSWORD']

db = DatabaseManager(dbname, user, host, password)

db.migrate_database(applications_database_migration_plan)