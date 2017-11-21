from config import CONFIG

# keyboard field
# describes how keyboard field is partitioned to 10 areas
class Field:
    def __init__(self):
        self.width = CONFIG['keyboard_width']
        self.height = CONFIG['keyboard_height']

    # ...