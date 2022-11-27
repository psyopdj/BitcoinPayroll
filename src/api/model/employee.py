import json


class Employee:
    def __init__(self, _id=None, clock=None, address=None):
        self._id = _id
        self.clock = clock
        self.address = address

    def __iter__(self):
        yield from {
            "_id": self._id,
            "clock": self.clock,
            "address": self.address,
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        json_dct = {"clock": self.clock, "address": self.address}
        # only add _id if it exists in the object already
        if self._id:
            json_dct['_id'] = str(self._id)
        return json_dct

    @staticmethod
    def from_json_dict(json_dict):
        return Employee(json_dict.get('_id', None), json_dict['clock'], json_dict['address'])

    @staticmethod
    def from_json_str(json_str):
        json_dict = json.loads(json_str)
        return Employee.from_json_dict(json_dict)

    def __hash__(self):
        return (self._id, self.clock, self.address).__hash__()

    def __eq__(self, other):
        if isinstance(other, Employee):
            return self._id == other._id and \
                   self.clock == other.clock and \
                   self.address == other.address
        return False
