# -*- coding: utf-8 -*-
# @Author: TD21forever
# @Date:   2018-10-30 20:54:30
# @Last Modified by:   TD21forever
# @Last Modified time: 2018-10-30 21:30:27
# coding=gbk
import time
import torch
import torch.utils.data as Data
import torchvision
import os
import torch.nn as nn
import torch.optim as optim
from torch.autograd import  Variable
from torchvision.transforms import transforms
exit()
DOWNLOAD_DATA = True
BATH_SIZE = 4
transform = None
LR = 0.001
EPOCH = 1
experimentSuffix = "CIFAR10"
dir = "C:\\Users\\TD21forever\\Desktop\\model.pth"
saveModelName = EPOCH



transform = transforms.Compose([
    transforms.Resize((227,227), 3),                           #对图像大小统一
    transforms.RandomHorizontalFlip(),                        #图像翻转
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[    #图像归一化
                             0.229, 0.224, 0.225])
])
#预处理

train_data = torchvision.datasets.CIFAR10(     #建立数据库
    root = './data',
    train=True,
    download= DOWNLOAD_DATA,
    transform = transform,                  #数据预处理

)
train_loader = Data.DataLoader(
    dataset = train_data,                  #数据库来源
    batch_size = BATH_SIZE,                #每一次传入多少图片
    shuffle = True,                        #为True时表示每个epoch都会打乱数据顺序
    num_workers = 0                        #加载数据时使用多少子进程。默认值为0，表示在主进程中加载数据
)
test_data = torchvision.datasets.CIFAR10( 
    root='./data',
    train=False,
    download=DOWNLOAD_DATA,
    transform=transform,
)
test_loader = Data.DataLoader(
    dataset = test_data,
    batch_size = BATH_SIZE,
    shuffle = True,
    num_workers = 0
)



classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')



#Alexnet
class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = torch.nn.Sequential(
            torch.nn.Conv2d(3, 96, 11, 4, 0),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(3, 2)
        )
        self.conv2 = torch.nn.Sequential(
            torch.nn.Conv2d(96, 256, 5, 1, 2),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(3, 2)
        )
        self.conv3 = torch.nn.Sequential(
            torch.nn.Conv2d(256, 384, 3, 1, 1),
            torch.nn.ReLU(),
        )
        self.conv4 = torch.nn.Sequential(
            torch.nn.Conv2d(384, 384, 3, 1, 1),
            torch.nn.ReLU(),
        )
        self.conv5 = torch.nn.Sequential(
            torch.nn.Conv2d(384, 256, 3, 1, 1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(3, 2)
        )
        self.dense = torch.nn.Sequential(
            torch.nn.Linear(9216, 4096),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.5),
            torch.nn.Linear(4096, 4096),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.5),
            torch.nn.Linear(4096, 10)
        )

    def forward(self, x):
        conv1_out = self.conv1(x)
        conv2_out = self.conv2(conv1_out)
        conv3_out = self.conv3(conv2_out)
        conv4_out = self.conv4(conv3_out)
        conv5_out = self.conv5(conv4_out)
        res = conv5_out.view(conv5_out.size(0), -1)
        out = self.dense(res)
        return out

net = Net()
net.cuda() #使用GPU加速
loss_function = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(),lr = LR, momentum = 0.9)


for epoch in range(EPOCH):
    batch_size_start = time.time()
    classes_list = [0,0,0,0,0,0,0,0,0,0]
    running_loss = 0.0
    for i, (x,y) in enumerate(train_loader,0):
        inputs = x.cuda()#使用GPU加速
        labels = y.cuda()#使用GPU加速
        output = net(inputs)
        loss = loss_function(output, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if (i + 1) % 500 == 0:
            print('Epoch [%d/%d], Iter [%d/%d] Loss: %.4f,need time %.4f'
                  % (epoch + 1, EPOCH, i + 1, (len(train_data) // BATH_SIZE), loss.data.item(),time.time() - batch_size_start))

    correct = 0
    total = 0
    net.eval()# 改成测试形态, 应用场景如: dropout
    batch_size_start = time.time()
    for (images, labels) in test_loader:
        image = images.cuda()
        label = labels.cuda()
        outputs = net(image)
        data = outputs.data
        # print(data)#一个4*10的矩阵，4代表batch_size 10代表10类
        value, predicted = torch.max(data, 1)#返回每一行中最大值的那个元素，且返回其索引
        print(classes[0],"%.4f"%float(data[0][0]),"\n",
            classes[1],"%.4f"%float(data[0][1]),"\n",
            classes[2],"%.4f"%float(data[0][2]),"\n",
            classes[3],"%.4f"%float(data[0][3]),"\n",
            classes[4],"%.4f"%float(data[0][4]),"\n",
            classes[5],"%.4f"%float(data[0][5]),"\n",
            classes[6],"%.4f"%float(data[0][6]),"\n",
            classes[7],"%.4f"%float(data[0][7]),"\n",
            classes[8],"%.4f"%float(data[0][8]),"\n",
            classes[9],"%.4f"%float(data[0][9]))
        print('这张图片实际上是',classes[label[0]],'预测是',classes[predicted[0]])
        print("------------------------------------------------------------------------")
        total += labels.size(0)
        correct += (predicted == label).sum()
    print(" Val BatchSize cost time :%.4f s" % (time.time() - batch_size_start))
    print('Test Accuracy of the model on the %d Val images: %.4f' % (total, float(correct) / total))
    if (float(correct) / total) >= 0.99:
        print('the Accuracy>=0.98 the num_epochs:%d' % epoch)
        break
    if (epoch + 1) % saveModelName != 0:#如果到了最后一轮，就保存训练好的模型，可有可无
        continue
    try:
        state = {'net':net.state_dict(), 'optimizer':optimizer.state_dict(), 'epoch':epoch}
        torch.save(state, dir)
    except Exception as e:
        print("保存模型失败")
        raise e
    
