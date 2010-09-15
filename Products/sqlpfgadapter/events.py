
def addTable(object, event):
  """ Add an SQL table to database when a new action adapter is created 
  """
  object.createOrUpdateTable()
