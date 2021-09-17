# -*- encoding: utf-8 -*-
"""
@File       :   NBayesPredictor.py
@Contact    :   mcfly@mail.sdu.edu.cn
@github     :   https://github.com/McflyWZX

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/9/17 15:29   Mcfly      1.0         None
"""
from collections import Counter
import math


class MAP_Class:
    def __init__(self, name):
        self.name = name
        self.featureCount = 0
        self.featureListTable = []
        self.featureFrequency = {}

    def updateFeatureFrequency(self, expect=-1):
        self.featureCount = 0
        self.featureFrequency.clear()
        for i in range(len(self.featureListTable)):
            if i == expect:
                continue
            self.featureCount += len(self.featureListTable[i])
            frequency = Counter(self.featureListTable[i])
            for feature, num in frequency.items():
                if feature in self.featureFrequency.keys():
                    self.featureFrequency[feature] += num
                else:
                    self.featureFrequency[feature] = num

    # 向这个类别中添加一个该类别的特征列表
    def addDataList(self, featureList: list):
        self.featureListTable.append(featureList)

    def sortFrequencyDict(self):
        self.featureFrequency = {k: v for k, v in
                                 sorted(self.featureFrequency.items(), key=lambda item: item[1], reverse=True)}


class MAP_Predictor:
    def __init__(self):
        self.totalDataLen = 0
        self.classes: dict = {}

    def addClass(self, mapClass: MAP_Class):
        if mapClass.name in self.classes.keys():
            print('There are already have class: \'' + mapClass.name + '\'')
            return
        else:
            self.classes[mapClass.name] = mapClass
            self.totalDataLen += len(mapClass.featureListTable)

    def __pred(self, featureList):
        featureSet = set(featureList)
        probWiAfterC = {}
        for name, cls in self.classes.items():
            # 取出改类别的的特征列表，并与传入的特征拼装做拉普拉斯平滑
            totalLen = cls.featureCount
            totalFeature: dict = cls.featureFrequency.copy()
            # 先补全特征
            for feature in featureSet:
                if feature not in totalFeature.keys():
                    totalFeature[feature] = 0
            # 拉普拉斯平滑
            for feature in totalFeature.keys():
                totalFeature[feature] += 1
                totalLen += 1

            probWiAfterC[name] = 0
            for feature in featureSet:
                probWiAfterC[name] += math.log2(totalFeature[feature] / totalLen)
        probWiAfterC = {k: v for k, v in
                        sorted(probWiAfterC.items(), key=lambda item: item[1], reverse=True)}
        return probWiAfterC

    def validate(self, percentageValidation: float):
        err = 0.0
        total = 0.0
        for name, cls in self.classes.items():
            # 其它类别刷新特征频率
            for otherCls in self.classes.values():
                if not otherCls == cls:
                    otherCls.updateFeatureFrequency()
            for i in range(len(cls.featureListTable)):
                # 用于交叉验证抽样的类别抽出样本并刷新特征频率
                cls.updateFeatureFrequency(expect=i)
                result, *_ = self.__pred(cls.featureListTable[i])
                print(name + '%02d' % i + ' result: ' + result)
                if not result == name:
                    err += 1
                total += 1
        print('正确率: %f' % (1 - err / total))
        return 1 - err / total

    def predUnknow(self, featureList):
        for cls in self.classes.values():
            cls.updateFeatureFrequency()
        result, *_ = self.__pred(featureList)
        return result
