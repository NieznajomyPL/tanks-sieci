class Event:
    def __init__(self):
        self.listeners = []

    def register(self, listener):
        self.listeners.append(listener)

    def unregister(self, listener):
        self.listeners.remove(listener)

    def trigger(self, *args, **kwargs):
        for listener in self.listeners:
            listener(*args, **kwargs)

class EventManager:
    def __init__(self):
        self.events = {}

    def create_event(self, name):
        self.events[name] = Event()

    def get_event(self, name):
        return self.events.get(name)