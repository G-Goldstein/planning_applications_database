from migration_plan import MigrationPlan

applications_database_migration_plan = MigrationPlan()

applications_database_migration_plan.add_version(
	upgrades = [
		"""
			CREATE TABLE application (
				reference VARCHAR(50) PRIMARY KEY,
				title VARCHAR(5000),
				link VARCHAR(200),
				address VARCHAR(200),
				received_date DATE,
				validated_date DATE,
				status VARCHAR(50)
			)
		""",
		"""
			CREATE INDEX received_date_index
			ON application 
			(received_date, validated_date, reference)
		""",
		"""
			CREATE INDEX validated_date_index
			ON application 
			(validated_date, received_date, reference)
		""",
		"""
			CREATE INDEX indexed_title
			ON  application
			USING gin(title)
		"""
	],
	downgrades = [
		"""
			DROP TABLE application
		"""
	]
)