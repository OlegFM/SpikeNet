class SpikeLayer():
    number = 0
    layer_id = 0
    neyrons = []
    inputs = 0
    killall = False
    outputs = []

    #Инициализация нового слоя
    def __init__(self, number, inputs):
        self.number = number
        self.inputs = inputs
        for i in range(int(number)):
            self.neyrons.append(SpikeNeyron(inputs=inputs))

    #Создание слоя из модели
    def __init__(self, model):
        self.LoadLayer(model)

    def LoadLayer(self, model):
        self.inputs = model[0]
        self.number = model[1]
        self.killall = model[2]
        for neyron in model[3]:
            self.neyrons.append(neyron)

    def SaveLayer(self):
        return [self.inputs, self.number, self.killall, self.neyrons]

    def tick(self, input, killall):
        self.outputs = []
        local_killall = False

        #Ввод данных в нейрон и получение состояния его выхода
        for neyron in self.neyrons:
            self.outputs += neyron.tick(input, killall)

        #Если хотя бы в одном нейроне поднят флаг killall, запрещаем работу всему слою
            if neyron.killall:
                local_killall = True
        self.killall = local_killall
        return self.outputs