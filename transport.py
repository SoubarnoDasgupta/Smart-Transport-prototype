"""Deterministic transport simulation. No real transit or GPS data."""
from dataclasses import dataclass
import argparse
import json

@dataclass(frozen=True)
class Route:
    name: str
    stops: tuple[str, ...]
    minutes_per_segment: int
    fare_per_segment: int
    headway: int

ROUTES = (
    Route('Campus Shuttle', ('Campus','Library','Market','Station'), 5, 5, 15),
    Route('City Connector', ('Campus','Hospital','Station','City Centre'), 8, 7, 20),
    Route('Market Express', ('Market','Museum','City Centre'), 6, 6, 12),
)
STOPS = sorted({stop for route in ROUTES for stop in route.stops})

def normalize_stop(value):
    if not isinstance(value, str):
        raise ValueError('Stop must be text.')
    for stop in STOPS:
        if stop.casefold() == value.strip().casefold():
            return stop
    raise ValueError('Unknown stop. Choose from: ' + ', '.join(STOPS))

def search(origin, destination, elapsed_minutes=0, delay_minutes=0):
    origin, destination = normalize_stop(origin), normalize_stop(destination)
    if origin == destination:
        raise ValueError('Choose different origin and destination stops.')
    for value in (elapsed_minutes, delay_minutes):
        if type(value) is not int or value < 0:
            raise ValueError('Elapsed time and delay must be non-negative integers.')
    results = []
    for route in ROUTES:
        if origin not in route.stops or destination not in route.stops:
            continue
        start, end = route.stops.index(origin), route.stops.index(destination)
        if start >= end:
            continue  # One-way demo routes.
        departure_offset = start * route.minutes_per_segment + delay_minutes
        wait = (departure_offset - elapsed_minutes) % route.headway
        segments = end - start
        results.append({
            'route': route.name,
            'stops': list(route.stops[start:end+1]),
            'wait_minutes': wait,
            'travel_minutes': segments * route.minutes_per_segment,
            'arrival_in_minutes': wait + segments * route.minutes_per_segment,
            'fare_demo_inr': segments * route.fare_per_segment,
            'simulated': True,
        })
    return sorted(results, key=lambda row: (row['arrival_in_minutes'], row['fare_demo_inr']))

def main():
    parser = argparse.ArgumentParser(description='Search fictional, one-way transport routes.')
    parser.add_argument('origin', nargs='?')
    parser.add_argument('destination', nargs='?')
    parser.add_argument('--stops', action='store_true')
    parser.add_argument('--elapsed', type=int, default=0, help='Minutes since simulation started')
    parser.add_argument('--delay', type=int, default=0, help='Uniform departure delay in minutes')
    args = parser.parse_args()
    if args.stops:
        print('\n'.join(STOPS)); return
    if not args.origin or not args.destination:
        parser.error('Provide origin and destination, or use --stops.')
    try:
        results = search(args.origin,args.destination,args.elapsed,args.delay)
    except ValueError as error:
        parser.exit(1, f'Error: {error}\n')
    print(json.dumps({'notice':'Simulated data only; not real transit information.', 'routes':results}, indent=2))

if __name__ == '__main__':
    main()
