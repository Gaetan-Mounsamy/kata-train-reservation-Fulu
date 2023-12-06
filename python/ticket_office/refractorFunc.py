def check_available_seats(train_data):
    return filter(lambda s: s["coach"] == "A" and not s["booking_reference"], train_data["seats"].values())

def reserve_seats(available_seats, seat_count):
    return [next(available_seats) for _ in range(seat_count)]

def create_reservation(to_reserve, train_id, booking_reference):
    seat_ids = [s["seat_number"] + s["coach"] for s in to_reserve]
    return {
        "train_id": train_id,
        "booking_reference": booking_reference,
        "seats": seat_ids
    }
