class BookingReference:
    def __init__(self, initial_count=123456789):
        self._count = initial_count

    def increment(self):
        self._count += 1

    def value(self):
        return hex(self._count)[2:]

    def get_booking_reference(self):
        self.increment()
        return self.value()