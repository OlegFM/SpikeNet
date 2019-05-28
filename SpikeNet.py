class SpikeNet():

    layers_num = 0
    layers = []
    killall = False
    outputs = []

    def __init__(self, layers):
        id = 0
        for layer in layers:
            layer.LoadLayer(layer)
            layer.id = id
            id += id

    def tick(self, input):
        self.outputs = []
        self.killall = False
        for i in range(int(self.layers)):
            if self.layers[i].id == 0:
               self.outputs += self.layers[i].tick(input, self.killall)
            else:
               self.outputs += self.layers[i].tick(self.layers[i-1].output, self.killall)
            if self.layers[i].killall:
                self.killall = True
        return self.outputs

    def Save(self):
        return [self.layers_num, self.killall, self.outputs, self.layers]

    def Load(self, net):

        self.layers_num = net[0]
        self.killall = net[1]
        self.layers = net[2]
        self.outputs = net[3]