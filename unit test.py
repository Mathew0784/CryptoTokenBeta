import unittest

class TestCryptoApp(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_fetch_crypto_data(self):
        data = app.fetch_crypto_data()
        self.assertTrue(isinstance(data, list))
        for crypto in data:
            self.assertTrue("name" in crypto)
            self.assertTrue("price" in crypto)

    def test_insert_crypto_data(self):
        data = [
            {"name": "TEST1", "price": "100"},
            {"name": "TEST2", "price": "200"}
        ]
        app.insert_crypto_data(data)

        with app.sqlite3.connect("crypto_data.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT symbol, price FROM crypto WHERE symbol IN ('TEST1', 'TEST2')")
            fetched_data = cursor.fetchall()

        self.assertEqual(len(fetched_data), 2)
        self.assertEqual(fetched_data[0], ("TEST1", "100"))
        self.assertEqual(fetched_data[1], ("TEST2", "200"))

        if __name__ == "__main__":
            unittest.main()
            app.run(debug=True)