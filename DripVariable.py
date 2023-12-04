class DripVariable:
    def __init__(self, name, value, drip_type):
        self.name = name
        self.value = value
        self.type = drip_type

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def __str__(self):
        return self.name + ": " + str(self.value)