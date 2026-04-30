class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, stops):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops

def find_cheapest_flight(data):
    if data is None or not data["data"]:
        print("There is no flight data.")
        return FlightData(price="N/A",
                          origin_airport="N/A",
                          destination_airport="N/A",
                          out_date="N/A",
                          return_date="N/A",
                          stops="N/A")

    # Get data from the first flight in the json
    first_flight = data["data"][0]
    lowest_price = float(first_flight["price"]["grandTotal"])
    number_of_stops = len(first_flight["itineraries"][0]["segments"]) - 1      # a flight with 2 segments will have 1 stop
    origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    destination = first_flight["itineraries"][0]["segments"][number_of_stops]["arrival"]["iataCode"]
    out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

    cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, number_of_stops)

    for flight in data["data"]:
        new_price = float(flight["price"]["grandTotal"])
        if new_price < lowest_price:
            lowest_price = new_price
            origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            destination = flight["itineraries"][0]["segments"][number_of_stops]["arrival"]["iataCode"]
            out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

            cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)

            print(f"Lowest price to {destination} is £{lowest_price}")

    return cheapest_flight


