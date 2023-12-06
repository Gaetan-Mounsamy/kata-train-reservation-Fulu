import json
import requests
from flask import Flask, request
from refractorFunc import check_available_seats, reserve_seats, create_reservation

def create_app():
    app = Flask("ticket_office")

    def send_reservation(reservation):
        reservation_payload = {
            "train_id": reservation["train_id"],
            "seats": reservation["seats"],
            "booking_reference": reservation["booking_reference"]
        }
        response = requests.post("http://localhost:8081/reserve", json=reservation_payload)
        return response

    @app.post("/reserve")
    def reserve():
        payload = request.json
        seat_count, train_id = payload["count"], payload["train_id"]
        
        booking_reference = requests.get("http://localhost:8082/booking_reference").text
        train_data = requests.get(f"http://localhost:8081/data_for_train/{train_id}").json()

        available_seats = check_available_seats(train_data)
        to_reserve = reserve_seats(available_seats, seat_count)
        reservation = create_reservation(to_reserve, train_id, booking_reference)

        response = send_reservation(reservation)
        assert response.status_code == 200, response.text

        return json.dumps(reservation)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8083)
