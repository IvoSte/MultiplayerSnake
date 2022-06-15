if __name__ == "__main__":
    import sys

    sys.path.append("..")

from dataclasses import asdict
import json
import dacite


class NetworkData:
    def to_json(self):
        """Return JSON object of this data object, used when sending data."""
        jsonified_send_object = asdict(self)
        jsonified_send_object["class_type"] = type(self).__name__
        return json.dumps(jsonified_send_object)

    @classmethod
    def from_json(cls, json_string, type_def=None):
        """Return data object of input JSON object, used when receiving data."""
        data = json.loads(json_string)
        if type_def is None:
            type_def = cls.deduce_class_type(data["class_type"])

        type_hooks = {Controls: int}
        type_hooks = {int: Controls}
        return dacite.from_dict(data_class=type_def, data=data, config=dacite.Config(type_hooks=type_hooks))

    def to_packet(self):
        """Encode data object to packet to send, first packing to JSON, then to binary"""
        return str.encode(self.to_json(), encoding="utf8")

    @classmethod
    def from_packet(cls, packet, type_def=None):
        """Decode data object from received packet, first decoding from binary, then to data object from JSON"""
        return cls.from_json(packet.decode(), type_def=type_def)

    @classmethod
    def deduce_class_type(cls, type_name):
        """When recieving a bytes object and translating it back to NetworkData object,
        we need to know what subtype of NetworkData we need to translate it to."""
        return [
            stp
            for stp in cls.__subclasses__()  # look through all subclasses...
            if stp.__name__ == type_name  # ...and select by type name
        ][0]


from networking.network_commands import *
from networking.network_data import *
