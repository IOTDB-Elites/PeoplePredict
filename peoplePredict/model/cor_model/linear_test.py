import numpy as np
import  matplotlib.pyplot as plt
from sklearn import  linear_model

if __name__ == '__main__':
    a = [5,6,7,8]
    b = [10, 12, 14, 16]
    a  =np.array(a).reshape((-1, 1))
    b = np.array(b)
    linear = linear_model.LinearRegression()
    linear.fit(a, b)
    print('Cofficients:', linear.coef_)
    print('intercept', linear.intercept_)

    minX =min(a)
    maxX =max(b)
    #以数据datasets_X的最大值和最小值为范围，建立等差数列，方便后续画图。
    X=np.arange(minX,maxX).reshape([-1,1])

    plt.scatter(a,b,color='red')
    #plot函数用来绘制直线，这 里表示用蓝色绘制回归线；
    #xlabel和ylabel用来指定横纵坐标的名称
    plt.plot(X,linear.predict(X),color='blue')
    plt.xlabel('Area')
    plt.ylabel('Price')
    plt.show()
