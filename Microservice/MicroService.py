class MicroService(object):
	"""docstring for MicroService"""
	def __init__(self, hosts, app):
		from kazoo.client import KazooClient

		self.zk = KazooClient(hosts=hosts)
		self.app = "/" + app

	def zkStart(self):
		self.zk.start()

	def zkStop(self):
		self.zk.stop()
		
	def registerService(self, service, url):
		if self.zk.exists(self.app + "/" + service):
			self.zk.delete(self.app + "/" + service, recursive=True)
			self.zk.delete(self.app, recursive=True)
		self.zk.ensure_path(self.app + "/" + service)
		self.zk.set(self.app + "/" + service, bytes(url, encoding="utf-8"))

		self.__watchServiceChanged(service)

		return 'Service registed'

	def unregisterService(self, service):
		self.zk.delete(self.app + "/" + service, recursive=True)
		return "Service deleted"

	def findService(self, service):
		data, stat = self.zk.get(self.app + "/" + service)
		return data.decode("utf-8")

	def __watchServiceChanged(self, service):

		@self.zk.DataWatch(self.app + "/" + service)
		def changed(data, stat):
			print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
