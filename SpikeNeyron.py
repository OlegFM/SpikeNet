class SpikeNeyron():
    import numpy as np
    weights = []
    tikalive = 0
    TLTP_weights = []
    u = []
    tlast = []
    tleak = 0
    polarity = 0
    inputs = 0
    tiks = 0
    killall = False

    #Начальная инициализация
    def __init__(self, tikalive=2000, weight_init="classic", inputs=1, tspike=0, tlast=0, tleak=5000):
        self.tikalive = tikalive
        if weight_init == "classic":
            for i in range(inputs):
                self.weights.append(np.random(0.001, 1))
        else:
            for i in range(inputs):
                self.weights.append(np.random(0.8, 1200))
        self.u = np.zeros(inputs)
        self.tlast = tlast
        self.tleak = tleak
        self.tspike = tspike
        self.inputs = inputs
        self.tlast = np.zeros(inputs)

    #Инициализация существующей моделью
    def __init__(self, model):
        self.LoadParameters(model)

    #Суммирование входящих сигналов по формуле
    def sigIntegrity(self, input):
        TLTP = []
        num = 0
        for i in input:
            if i == 1 or i==-1:
                self.u[i] = self.u[i] * self.exp_sig(input)[i] + self.weights[i]
                self.tlast[i] = 0
                num += 1
                TLTP.append(num)
        self.TLTP_weights.append(TLTP)

    def exp_sig(self, input):
        exp_arr = []
        for i in input:
            if i == 1:
                exp_arr.append(np.exp(-self.tlast[i] / self.tleak))
        return exp_arr

    def exp_weights(self, inc=False, prespike=False):
        weights = []

        #Выбор бета для инеркмента или декремента
        beta = beta_inc
        if (not inc):
            beta = beta_dec

        #Составление массива весов, увеличиваемых активационной функцией
        for item in self.TLTP_weights:
            weights += item
        weights = set(weights).sort()

        #Соствление массива весов, уменьшаемых активационной функцией
        if (not prespike):
            for i in range(int(len(self.weights))):
                if (i in weights):
                    weights.remove(i)
                else:
                    weights.append(i)
        exp_arr = []

        #Составление массива экспонент для формулы расчёта веса
        for i in weights:
            if(not prespike):
                exp_arr.append(np.exp(-beta*(w_max - self.weights[i])/(w_max - w_min)))
            else:
                exp_arr.append(np.exp(-beta * (self.weights[i] - w_min) / (w_max - w_min)))
        return exp_arr

    def activation(self):

        #обновление весовых коэффициентов связей, учавствовавших в накоплении сигнала за время TLTP
        prespike_weights = self.exp_weights(True, prespike=True)
        for i in prespike_weights:
           self.weights[i] = self.weights[i]-alpha_inc*i

        #обновление весовых коэффициентов оставшихся связей
        other_weights = self.exp_weights()
        for i in other_weights:
           self.weights[i] = self.weights[i]-alpha_dec*i
        self.tlast = np.zeros(self.inputs)

    def tick(self, input, killall=False):
        output = 0
        #кол-во тиков после последней активации
        self.tiks += 1

        #Разрешить суммирование сигналов по истечении времени работы и рефрактерного периода
        #и после разрешения на работу
        if(self.tiks > (self.tikalive + TRef) and not killall):
            self.sigIntegrity(input)

        #Разрешить работу сети по истечении времени работы
        if(self.tiks > self.tikalive):
            self.killall = True

        #Инкремент времени с момента поступления последнего сигнала или активации нейрона
        self.tlast = list(np.asarray(self.tlast) + 1)
        sig = np.array(self.u)

        #Условие активации нейрона
        if(sig.sum() >= Tresh):
            self.activation()
            output = 1
        return output

    def SaveParameters(self):
        return [self.weights, self.TLTP_weights, self.u, self.tikalive, self.killall, self.tiks, self.tlast,
                self.tspike, self.tleak, self.polarity]

    def LoadParameters(self, params):
        self.weights = params[0]
        self.TLTP_weights = params[1]
        self.u = params[2]
        self.tikalive = params[3]
        self.killall = params[4]
        self.tiks = params[5]
        self.tlast = params[6]
        self.tspike = params[7]
        self.tleak = params[8]
        self.polarity = params[9]