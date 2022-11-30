import json


class Employee:
    def __init__(self, _id=None, rfid=None, name=None, wallet_address=None, pay_rate=None):
        self._id = _id
        self.rfid = rfid
        self.name = name
        self.wallet_address = wallet_address
        self.pay_rate = pay_rate

    def __iter__(self):
        yield from {
            "_id": self._id,
            "rfid": self.rfid,
            "name": self.name,
            "wallet_address": self.wallet_address,
            "pay_rate": self.pay_rate
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        json_dct = {"rfid": self.rfid, "name": self.name, "wallet_address": self.wallet_address,
                    "pay_rate": self.pay_rate}
        # only add _id if it exists in the object already
        if self._id:
            json_dct['_id'] = str(self._id)
        return json_dct

    @staticmethod
    def from_json_dict(json_dict):
        return Employee(json_dict.get('_id', None), json_dict['rfid'], json_dict['name'], json_dict['wallet_address'],
                        json_dict['pay_rate'])

    @staticmethod
    def from_json_str(json_str):
        json_dict = json.loads(json_str)
        return Employee.from_json_dict(json_dict)

    def __hash__(self):
        return (self._id, self.rfid, self.name, self.wallet_address, self.pay_rate).__hash__()

    def __eq__(self, other):
        if isinstance(other, Employee):
            return self._id == other._id and \
                   self.rfid == other.rfid and \
                   self.name == other.name and \
                   self.wallet_address == other.wallet_address and \
                   self.pay_rate == other.pay_rate
        return False
