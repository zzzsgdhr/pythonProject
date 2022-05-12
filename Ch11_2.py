class A():
  att1 = 'class_att1'
  att2 = 1
  def __init__(self):
    self.att1 = 'instance_att1'

a = A()
print(a.att1)
print(a.att2)
