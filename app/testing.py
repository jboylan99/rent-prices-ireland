import unittest
from app import app

# Basic tests to see if the pages are there or not.
class FlaskTests(unittest.TestCase):

	def setUp(self):
		app.config['TESTING'] = True
		app.config['DEBUG'] = False
		self.app = app.test_client()

	def tearDown(self):
		pass

	# Test if these pages exist
	def test_index(self):
		response = self.app.get('/', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_countystats(self):
		response = self.app.get('/countystatistics', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_nationalstats(self):
		response = self.app.get('/nationalstatistics', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	# Test that this page does not exist.
	def test_wrong_page(self):
		response = self.app.get('/login', follow_redirects=True)
		self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
	unittest.main()