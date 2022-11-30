import json


class Shift:
    def __init__(self, _id=None, employee_id=None, date=None, in_timestamp=None, out_timestamp=None):
        self._id = _id
        self.employee_id = employee_id
        self.date = date
        self.in_timestamp = in_timestamp
        self.out_timestamp = out_timestamp

    def __iter__(self):
        yield from {
            "_id": self._id,
            "employee_id": self.employee_id,
            "date": self.date,
            "in_timestamp": self.in_timestamp,
            "out_timestamp": self.out_timestamp
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        json_dct = {"employee_id": self.employee_id, "date": self.date, "in_timestamp": self.in_timestamp,
                    "out_timestamp": self.out_timestamp}
        # only add _id if it exists in the object already
        if self._id:
            json_dct['_id'] = str(self._id)
        return json_dct

    @staticmethod
    def from_json_dict(json_dict):
        return Shift(json_dict.get('_id', None), json_dict['employee_id'], json_dict['date'], json_dict['in_timestamp'],
                     json_dict['out_timestamp'])

    @staticmethod
    def from_json_str(json_str):
        json_dict = json.loads(json_str)
        return Shift.from_json_dict(json_dict)

    def __hash__(self):
        return (self._id, self.employee_id, self.date, self.in_timestamp, self.out_timestamp).__hash__()

    def __eq__(self, other):
        if isinstance(other, Shift):
            return self._id == other._id and \
                   self.employee_id == other.employee_id and \
                   self.date == other.date and \
                   self.in_timestamp == other.in_timestamp and \
                   self.out_timestamp == other.out_timestamp
        return False
