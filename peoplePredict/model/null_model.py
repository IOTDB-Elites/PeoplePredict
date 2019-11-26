# just a example of model
class NullModel:
    def __init__(self):
        self.res = 0
        self.name = 'null_model'

    def predict(self, x):
        return self.res

    def name(self):
        return self.name
