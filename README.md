# Smart Transport Prototype

A Python command-line prototype for finding direct routes, estimating demo fares and simulating vehicle arrival times. Inspired by a Smart Transport project concept; this is a new implementation prepared with AI assistance.

All routes, fares and schedules are fictional. There is no live GPS tracking, real transit integration or ticket booking.

## Features

- Direct route search between named stops
- Case-insensitive input handling and validation
- Fare calculation based on travelled segments
- Arrival estimates using repeating departure intervals
- Adjustable elapsed time and simulated departure delays
- Results sorted by arrival time
- Ten automated tests covering route logic and edge cases

## Run

Requires Python 3.10 or newer. No external packages are needed.

```sh
python transport.py --stops
python transport.py Campus Station
python transport.py Library Station --elapsed 4
python transport.py Campus "City Centre" --elapsed 10 --delay 3
python -m unittest -v
```

Results are printed as JSON. An empty route list means no direct one-way service exists in the demo. Transfers and reverse services are not implemented.

## Simulation model

Routes are ordered sequences of stops. Travel time and fare use fixed costs per segment. Vehicles depart the first stop every `headway` minutes from simulation minute zero. A downstream stop has an offset based on its position. The optional delay shifts departures uniformly; it does not change travel speed.

The wait calculation is `(stop offset + delay - elapsed time) % headway`. Arrival time is the wait plus journey duration. A zero wait means a vehicle is departing at that simulation minute. These estimates are deterministic, not predictions from real measurements.

## Files

- `transport.py`: route data, search logic and CLI
- `test_transport.py`: isolated tests with expected results

## Limitations and extensions

The prototype has no UI, database, authentication or geographic calculations. Future work could add a web interface, transfer search and a real transit feed after validating data access and reliability. Review the simulation assumptions before explaining the project in interviews.
