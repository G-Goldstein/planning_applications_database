from database_manager import DatabaseManager
from applications_database import applications_database_migration_plan
import os

DATABASE_URL = os.environ['DATABASE_URL']

db = DatabaseManager(DATABASE_URL)

db.migrate_database(applications_database_migration_plan)