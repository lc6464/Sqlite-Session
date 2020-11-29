from pickle import loads, dumps
from uuid import uuid1

class ExecuteSql:
	def __init__(self, conn):
		self.conn = conn
		self.cur = conn.cursor()

	def execute(self, sql, parameters=(), cur=None):
		self.cur = cur if cur != None else self.cur
		return self.cur.execute(sql, parameters)

	def getResult(self, sql, parameters=(), cur=None):
		self.cur = cur if cur != None else self.cur
		return list(self.execute(sql, parameters))

	def getLength(self, sql, parameters=(), cur=None):
		self.cur = cur if cur != None else self.cur
		return len(self.getResult(sql, parameters))

	def commit(self, conn=None):
		self.conn = conn if conn != None else self.conn
		return self.conn.commit()


class Session(ExecuteSql):
	def Get(self, session):
		r = self.getResult('select * from Session where Session = ?', (session,))
		if len(r) > 0:
			r = list(r[0])
			r[2] = loads(r[2])
			return tuple(r)
		else:
			return ()

	def GetUser(self, user):
		r = self.getResult('select * from Session where User = ?', (user,))
		if len(r) > 0:
			r = list(r[0])
			r[2] = loads(r[2])
			return tuple(r)
		else:
			return ()

	def Remove(self, session):
		r = self.getResult('select * from Session where Session = ?', (session,))
		if len(r) > 0:
			r = list(r[0])
			r[2] = loads(r[2])
		else:
			return ()
		self.execute('delete from Session where Session = ?', (session,))
		self.commit()
		return tuple(r)

	def RemoveUser(self, user):
		r = self.getResult('select * from Session where User = ?', (user,))
		if len(r) > 0:
			r = list(r[0])
			r[2] = loads(r[2])
		else:
			return ()
		self.execute('delete from Session where User = ?', (user,))
		self.commit()
		return tuple(r)

	def Set(self, session, value):
		value = dumps(value)
		r = self.getResult('update Session set Value = ? where Session = ?', (value, session))
		self.commit()
		return r

	def SetUser(self, user, value):
		value = dumps(value)
		self.execute('update Session set Value = ? where User = ?', (value, user))
		self.commit()
		r = self.getResult('select * from Session where User = ?', (user,))
		if len(r) > 0:
			r = list(r[0])
			r[2] = loads(r[2])
			return tuple(r)
		else:
			return ()

	def Add(self, user):
		u = uuid1().urn[9:]
		while self.getLength('select * from Session where Session = ?', (u,)) > 0:
			u = uuid1().urn[9:]
		self.RemoveUser(user)
		self.execute('insert into Session (Session, User, Value) values (?, ?, ?)', (u, user, dumps({})))
		self.commit()
		r = self.getResult('select * from Session where Session = ?', (u,))
		if len(r) > 0:
			r = list(r[0])
			r[2] = loads(r[2])
			return tuple(r)
		else:
			return ()