# just a example of model
class PoiModel:
    def __init__(self):
        self.res = 0
        self.name = 'poi_model'

    def predict(self, x):
        return self.res

    def name(self):
        return self.name
