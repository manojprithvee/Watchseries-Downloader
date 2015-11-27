import pickle
def test(a):
	pass
abc=[lambda:test("manoj")]
output = open('test.json', 'wb')
pickle.dump(abc, output)