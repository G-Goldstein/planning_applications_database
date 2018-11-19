import psycopg2

class DatabaseManager():

	def __init__(self, dbname, user, host, password):
		conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(dbname, user, host, password))
		self.cursor = conn.cursor()

	def begin(self):
		self.cursor.execute("BEGIN")

	def commit(self):
		self.cursor.execute("COMMIT")

	def rollback(self):
		self.cursor.execute("ROLLBACK")

	def initialise_version_table(self):
		self.begin()
		self.cursor.execute("""
			CREATE TABLE version
			(version int,
			PRIMARY KEY(version)
			)
		""")

		self.cursor.execute("INSERT INTO version VALUES(0)")
		self.commit()

	def get_version(self):
		try:
			self.cursor.execute('SELECT MAX(version) FROM version')
		except:
			self.rollback()
			self.initialise_version_table()
			self.cursor.execute('SELECT MAX(version) FROM version')
		row = self.cursor.fetchone()
		return row[0]

	def migrate_database(self, migration_plan, to_version=None):
		if to_version is None:
			to_version = migration_plan.get_highest_version()
		self._migrate_database(migration_plan, self.get_version(), to_version)

	def _migrate_database(self, migration_plan, from_version, to_version):
		if from_version < to_version:
			self.apply_upgrades(migration_plan, range(from_version, to_version))
		elif from_version > to_version:
			self.apply_downgrades(migration_plan, reversed(range(to_version, from_version)))
		else:
			print("Database already at requested version {}".format(to_version))

	def apply_upgrades(self, migration_plan, versions):
		for version in versions:
			self.begin()
			self.apply_migrations(migration_plan.upgrades[version])
			self.cursor.execute('INSERT INTO version VALUES (%s)', [version + 1])
			self.commit()
			print("Upgraded from version {} to version {}".format(version, version + 1))

	def apply_downgrades(self, migration_plan, versions):
		for version in versions:
			self.begin()
			self.apply_migrations(migration_plan.downgrades[version])
			self.cursor.execute('DELETE FROM version WHERE version = %s', [version + 1])
			self.commit()
			print("Downgraded from version {} to version {}".format(version + 1, version))

	def apply_migrations(self, migrations):
		for migration in migrations:
			self.cursor.execute(migration)