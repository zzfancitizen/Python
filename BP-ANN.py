#---Author：伍思磊---
#---Mail:wusilei@1006.tv---
#---2015/7/27---
 
import random
import math
 
#---神经网络Model---
class Ann:
    #构造函数 初始化模型参数
    def __init__(self, i_num, h_num, o_num):
        #可调参数
        self.learn_rate = 0.1    #学习率
        self.num_long = 2        #输出结果位数
        self.random_long = 10    #随机种子位数
 
        #输入参数
        self.input_num = i_num   #输入层 数量
        self.hidden_num = h_num  #隐层 数量
        self.output_num = o_num  #输出层 数量
 
        #模型参数
        self.input = []          #输入层
        self.hidden = []         #隐层
        self.output = []         #输出层
        self.error = []          #误差
        self.expectation = []    #期望
        self.weight_ih = self.__ini_weight(self.input_num, self.hidden_num)   #输入层->隐层 连接权
        self.weight_ho = self.__ini_weight(self.hidden_num, self.output_num)  #隐层->输出层 连接权
        self.threshold_h = self.__ini_threshold(self.hidden_num)              #隐层 阈值
        self.threshold_o = self.__ini_threshold(self.output_num)              #输出层 阈值
         
 
    #初始连接权生成器
    def __ini_weight(self, x, y):
        result = []
        long = math.pow(10, self.random_long)
        for i in range(0, x, 1):
            res = []
            for j in range(0, y, 1):
                num = round(random.randint(-1*long,long)/long, self.random_long)
                res.insert(j, num)
            result.insert(i, res)
        return result
 
    #初始阈值生成器
    def __ini_threshold(self, n):
        result = []
        long = pow(10, self.random_long)
        for i in range(0, n, 1):
            num = round(random.randint(-1*long,long)/long, self.random_long)
            result.insert(i, num)
        return result
 
    #激励函数 sigma
    def excitation(self, value):
        sigma = 1/(1+(math.exp(-1*value)))
        return sigma
 
    #输入数据
    def input_param(self, data, expectation = []):
        self.input = []
        for value in data:
            self.input.append(value)
        if(expectation):
            self.expectation = []
            for value in expectation:
                self.expectation.append(value)
 
    #隐层计算
    def count_hidden(self):
        self.hidden = []
        for h in range(0, self.hidden_num, 1):
            Hval = 0
            for i in range(len(self.input)):
                Hval += self.input[i] * self.weight_ih[i][h]
            Hval = self.excitation(Hval+self.threshold_h[h])
            self.hidden.insert(h, Hval)
 
    #输出层计算
    def count_output(self):
        self.output = []
        for o in range(0, self.output_num, 1):
            Oval = 0
            for h in range(len(self.hidden)):
                Oval += self.hidden[h] * self.weight_ho[h][o]
            Oval += self.threshold_o[o]
            Oval = round(Oval, self.num_long)
            self.output.insert(o, Oval)
 
    #误差计算
    def count_error(self):
        self.error = []
        for key in range(len(self.output)):
            self.error.insert(key, self.expectation[key] - self.output[key])
 
    #连接权反馈训练 输入层->隐层
    def train_weight_ih(self):
        for i in range(len(self.weight_ih)):
            for h in range(len(self.weight_ih[i])):
                tmp = 0
                for o in range(0, self.output_num, 1):
                    tmp += self.weight_ho[h][o] * self.error[o]
                self.weight_ih[i][h] = self.weight_ih[i][h] + self.learn_rate * self.hidden[h] * (1 - self.hidden[h]) * self.input[i] * tmp
             
 
    #连接权反馈训练 隐层->输出层
    def train_weight_ho(self):
        for h in range(len(self.weight_ho)):
            for o in range(len(self.weight_ho[h])):
                self.weight_ho[h][o] = self.weight_ho[h][o] + self.learn_rate * self.hidden[h] * self.error[o]
                 
    #阈值反馈训练 隐层
    def train_threshold_h(self):
        for h in range(len(self.threshold_h)):
            tmp = 0
            for o in range(0, self.output_num, 1):
                tmp += self.weight_ho[h][o] * self.error[o]
            self.threshold_h[h] = self.threshold_h[h] + self.learn_rate * self.hidden[h] * (1 - self.hidden[h]) * tmp
             
 
    #阈值反馈训练 输出层
    def train_threshold_o(self):
        for o in range(len(self.threshold_o)):
            self.threshold_o[o] = self.threshold_o[o] + self.error[o]
 
    #反馈训练
    def train(self):
        self.train_weight_ih()
        self.train_weight_ho()
        self.train_threshold_h()
        self.train_threshold_o()
 
    #归一化函数
    def normal_num(self, max, min, data):
        data = (data - min)/(max - min)
        return data
 
    #寻找集合的最大值和最小值
 
#---业务部分(示例)---
 
#要训练的规则，输入两个值，如果两值相等返回[1,0]，反之返回[0,1]
def testFunc(val):
    if(val[0] == val[1]):
        return [1,0]
    else:
        return [0,1]
 
#构造神经网络模型
ann = Ann(2,3,2)
 
#生成训练数据，随机生成5000组[0,1][1,0][1,1][0,0]随机数组
data = []
for i in range(0, 10000, 1):
    x = random.randint(0,1)
    y = random.randint(0,1)
    data.append([x,y])
 
#取得训练数据中的最大值和最小值
for i in range(len(data)):
    for j in range(len(data[i])):
        if(i == 0 and j == 0):
            max = min = data[i][j]
        elif(data[i][j] > max):
            max = data[i][j]
        elif(data[i][j] < min):
            min = data[i][j]
 
#训练数据归一化
dataNormal = []
for i in range(len(data)):
    dataNormal.insert(i, [])
    for j in range(len(data[i])):
        dataNormal[i].append(ann.normal_num(max, min, data[i][j]))
 
#计算训练数据期望值，并进行反馈训练
for i in range(len(data)):
    #计算期望值
    exp = testFunc(data[i])
    #输入训练数据与期望
    ann.input_param(dataNormal[i], exp)
    #计算隐层
    ann.count_hidden()
    #计算输出层
    ann.count_output()
    #计算误差
    ann.count_error()
    #反馈训练
    ann.train()
 
#生成测试数据，随机生成20组
testdata = []
for i in range(0, 20, 1):
    x = random.randint(0,1)
    y = random.randint(0,1)
    testdata.append([x,y])
 
#进行测试，同时输出神经网络预测值与实际期望值
for i in range(len(testdata)):
    exp = testFunc(testdata[i])
    ann.input_param(testdata[i])
    ann.count_hidden()
    ann.count_output()
    print("Ann:")
    print(ann.output)
    print("Exp:")
    print(exp)
    print("\r")