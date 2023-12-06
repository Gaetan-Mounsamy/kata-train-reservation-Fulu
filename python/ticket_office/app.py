import json
import requests
from flask import Flask, request

class Train:
    def __init__(self, train_id):
        self.id = train_id
        self.data = requests.get(f"http://localhost:8081/data_for_train/{self.id}").json()

    def check_available_seats(self):
        return filter(lambda s: s["coach"] == "A" and not s["booking_reference"], self.data["seats"].values())
    
class Reservation:
    def __init__(self, train: Train, booking_reference, to_reserve):
        self.train = train
        self.booking_reference = booking_reference
        self.seat_ids = [s["seat_number"] + s["coach"] for s in to_reserve]
    
    def get_payload(self):
        return {
            "train_id": self.train.id,
            "seats": self.seat_ids,
            "booking_reference": self.booking_reference
        }
    
def reserve_seats(available_seats, seat_count):
    return [next(available_seats) for _ in range(seat_count)]

def create_app():
    app = Flask("ticket_office")

    def send_reservation(reservation: Reservation):
        reservation_payload = reservation.get_payload()
        response = requests.post("http://localhost:8081/reserve", json=reservation_payload)
        return response

    @app.post("/reserve")
    def reserve():
        payload = request.json
        train = Train(payload["train_id"])
        seat_count = payload["count"]
        
        booking_reference = requests.get("http://localhost:8082/booking_reference").text

        available_seats = train.check_available_seats()
        to_reserve = reserve_seats(available_seats, seat_count)
        reservation = Reservation(train, booking_reference, to_reserve)

        response = send_reservation(reservation)
        assert response.status_code == 200, response.text

        return json.dumps(reservation.get_payload())

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8083)
