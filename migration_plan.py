class MigrationPlan():
	def __init__(self):
		self.upgrades = []
		self.downgrades = []

	def get_highest_version(self):
		return len(self.upgrades)

	def add_version(self, *, upgrades, downgrades):
		self.upgrades.append(upgrades)
		self.downgrades.append(downgrades)