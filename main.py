# -*- encoding: utf-8 -*-
"""
@File       :   main.py    
@Contact    :   mcfly@mail.sdu.edu.cn
@github     :   https://github.com/McflyWZX

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/9/17 15:31   Mcfly      1.0         None
"""
from ArticleReptile import *
from NBayesPredictor import *
from matplotlib import pyplot as plt

if __name__ == '__main__':
    # 下载文章数据
    # getAllArticle()
    # 加载下载好的两个作者的文章
    articlesByMadison = loadArticles('MADISON')
    articlesByHamilton = loadArticles('HAMILTON')
    articlesUnknow = loadArticles('HAMILTON OR MADISON')

    Madison = MAP_Class('MADISON')
    for article in articlesByMadison:
        Madison.addDataList(article.getWords())

    x = []
    y = []
    mapPre = None
    for numHamilton in range(21, 22):

        Hamilton = MAP_Class('HAMILTON')
        for i in range(numHamilton):  # len(articlesByMadison)):
            Hamilton.addDataList(articlesByHamilton[i].getWords())

        mapPre = MAP_Predictor()
        mapPre.addClass(Madison)
        mapPre.addClass(Hamilton)
        accuracy = mapPre.validate(1)

        x.append(numHamilton)
        y.append(accuracy)

    for article in articlesUnknow:
        print(mapPre.predUnknow(articlesUnknow))

    plt.plot(x, y, color='r', marker='o', markersize=0.5)
    plt.show()
