class Ovocie:
	def __init__(self):
		self.jablka = []
		for i in range(10):
			self.jablka.append(Jablko(i, self))




class Jablko:
	def __init__(self, a, ovocie):
		self.a = a
		self.ovocie = ovocie
		self.hrusky = []
		for i in range(10):
			self.hrusky.append(Hrusky(self.a, self))


class Hrusky:
	def __init__(self, a, jablko):
		self.jablko = jablko
		self.a = a

	def printt(self):
		for ovos in self.jablko.ovocie.jablka:
			print(ovos.hrusky)



ovocie = Ovocie()
for i in ovocie.jablka:
	for j in i.hrusky:
		j.printt()




