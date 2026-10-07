import unittest
from transport import search

class TransportTests(unittest.TestCase):
    def test_direct_route_fare_and_time(self):
        route = search('Campus','Station')[0]
        self.assertEqual(route['route'],'Campus Shuttle')
        self.assertEqual(route['fare_demo_inr'],15)
        self.assertEqual(route['travel_minutes'],15)
        self.assertEqual(route['wait_minutes'],0)
    def test_case_and_whitespace(self):
        self.assertEqual(search(' campus ','STATION'),search('Campus','Station'))
    def test_wait_for_next_departure(self):
        row = next(r for r in search('Campus','Station',1) if r['route']=='Campus Shuttle')
        self.assertEqual(row['wait_minutes'],14)
    def test_intermediate_stop_offset(self):
        row = search('Library','Station',0)[0]
        self.assertEqual(row['wait_minutes'],5)
        self.assertEqual(row['travel_minutes'],10)
    def test_departure_boundary(self):
        self.assertEqual(search('Library','Station',5)[0]['wait_minutes'],0)
    def test_delay_simulation(self):
        self.assertEqual(search('Campus','Station',0,3)[0]['wait_minutes'],3)
    def test_reverse_route_not_available(self):
        self.assertEqual(search('Station','Campus'),[])
    def test_no_direct_connection(self):
        self.assertEqual(search('Library','Museum'),[])
    def test_invalid_inputs(self):
        for args in [('Nowhere','Station'),('Campus','Campus'),('Campus','Station',-1),('Campus','Station',0,-1),('Campus','Station',1.5),('Campus','Station',True)]:
            with self.assertRaises(ValueError): search(*args)
    def test_sorted_and_marked_simulated(self):
        rows=search('Campus','Station',4)
        self.assertEqual([r['arrival_in_minutes'] for r in rows],sorted(r['arrival_in_minutes'] for r in rows))
        self.assertTrue(all(r['simulated'] for r in rows))

if __name__ == '__main__': unittest.main()
