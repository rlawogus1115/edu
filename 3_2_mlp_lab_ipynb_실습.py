# -*- coding: utf-8 -*-
"""3.2.MLP_lab.ipynb 실습

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1umAO-HO32-hz4lJm7MUXhpnCS41cwM3-

<h1>MLP</h1>

# import
"""

import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras

"""# Sigmoid 함수"""

X = np.arange(-10, 10, 0.1)

plt.figure(figsize=(12,4))

plt.subplot(1,2,1)
plt.plot(X, 1/(1+np.exp(-X)))
plt.grid()

plt.subplot(1,2,2)
plt.plot(X, tf.sigmoid(X))
plt.grid()

"""# 상수 값으로 풀어보는 XOR  예제

![xor_nn_1](https://user-images.githubusercontent.com/661959/54298177-9e82f080-45fb-11e9-8bdd-1f86718c6f5d.png)

* 행렬식으로 간소화
 * $\begin{bmatrix}L_1 & L_2 \end{bmatrix} = sig(\begin{bmatrix} x_1 & x_2 \end{bmatrix} \cdot \begin{bmatrix} 5 & -7 \\ 5 & -7\end{bmatrix} + \begin{bmatrix} -8 & 3\end{bmatrix})$
 * $output = sig(\begin{bmatrix} L_1 & L_2 \end{bmatrix} \cdot 
\begin{bmatrix} -11 \\ -11\end{bmatrix} + 
\begin{bmatrix} 6\end{bmatrix})$
    
"""

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=np.float32)
y = np.array([[0], [1], [1], [0]], dtype=np.float32)

W1 = tf.Variable([[5,-7],[5,-7]],dtype =  tf.float32)
b = tf.Variable([[-8,3]],dtype=tf.float32)

layer1 = tf.sigmoid(tf.matmul(X,W1) + b)

W2 = tf.Variable([[-11],[-11]],dtype=np.float32)
b = tf.Variable([6],dtype='float32')

h = tf.sigmoid(tf.matmul(layer1,W2)+b)

y_pred = tf.cast(h>=0.5,dtype=tf.float32)
acc = tf.reduce_mean(tf.cast(y_pred == y,tf.float32))

print(f"\nHypothesis:\n{h} \nPredicted:\n{y_pred} \nAccuracy:\n{acc}")

"""# Backpropagation
*  딥러닝 불가론
  * Perceptron(1969) by Marvin Minsky(마빈 민스키), MIT AI Lab
    * ![image.png](https://i.imgur.com/w3R847C.png)
    > "No one on earth had found a viable way to train MLPs"
    ("지구에서는 아무도 MLP를 훈련할 실행 가능한 방법을 찾지 못했다".)

* 역 전파 알고리즘 등장
    * 1974, 1982 by Paul Werbos
    * 1986 Jeffry Hinton, 재발견
* 출력층의 결과 오차를 입력층 까지 거슬러 전파하면서 계산

### Backpropagation - Feed Forward
![](https://i.imgur.com/VteL102.png)
* $z_1, z_2 $
  * $z_1 = w_1x_1 + w_2x_2 = 0.3\times0.1 + 0.25\times0.2 = 0.08$
  * $z_2 = w_3x_1 + w_4x_2 = 0.4\times0.1 + 0.35\times0.2 = 0.11$
* $h_1, h_2$
  * $h_1 = sig(z_1) = 0.5199893$
  * $h_2 = sig(z_2) = 0.5274723$
* $z_3, z_4$
  * $z_3 = w_5h_1 + w_6h_2 = 0.45\times h1 + 0.4 \times h_2 = 0.4449841$
  * $z_4 = w_7h_1 + w_8h_2 = 0.7\times h1 + 0.6 \times h2 = 0.68047595$
* $o_1, o_2$
  * $o_1 = sig(z_3) = 0.609446$
  * $o_2 = sig(z_4) = 0.66384494$
* cost
  * $ cost_1 = \frac{1}{2}(y_1 - o_1)^2 = 0.02193381 $
  * $ cost_2 = \frac{1}{2}(y_2 - o_2)^2 = 0.0020380868 $
  * $ cost_{tot} = cost_1 + cost_2  = 0.023971897$
"""

x1, x2 = 0.1, 0.2
w1, w2, w3, w4, w5, w6, w7, w8 = 0.3, 0.25, 0.4, 0.35, 0.45, 0.4, 0.7, 0.6
y1, y2 = 0.4, 0.6
h1 = tf.sigmoid(w1*x1+w2*x2)
h2 = tf.sigmoid(w3*x1+w4*x2)

z3 = w5*h1+w6*h2
z4 = w7*h1 + w8*h2
print(f'z3:{z3}, z4:{z4}')
o1 = tf.sigmoid(z3)
o2 = tf.sigmoid(z4)
print(f'o1:{o1}, o2:{o2}')
c1 = 1/2*(y1 - o1)**2
c2 = 1/2*(y2 - o2)**2
cost = c1 + c2
print(f'c1:{c1}, c2:{c2}, cost:{cost}')

"""## Backpropagation step-1

![](https://i.imgur.com/dI0T2B7.png)

* $w_5, w_6,w_7,w_8$의 미분값 계산

  * $\displaystyle \frac{\partial Cost_{tot}}{\partial w_5} = \frac{\partial Cost_{tot}}{\partial o_1} \times \frac{\partial o_1}{\partial z_3} \times \frac{\partial z_3}{\partial w_5}$
    * $\displaystyle \frac{\partial Cost_{tot}}{\partial o_1}  = \frac{\partial Cost_1}{\partial o1} + \require{cancel} \cancelto{0}{\frac{\partial Cost_2}{\partial o1}} \\ =   2 \frac{1}{2}(y_1 - o_1)^{2-1} \times(-1) + 0 \\ = -(y_1 - o_1) =  -(0.4 - 0.609446) = 0.20944598 $

    * $\displaystyle \frac{\partial o_1}{\partial z_3} = o_1(1-o_1) = 0.609446(1 - 0.609446) = 0.23802158$
      * $sigmoid$ 함수의 미분 :  https://en.wikipedia.org/wiki/Logistic_function#Derivative
      * $\displaystyle \frac{\mathrm d }{\mathrm d x}f(x) = f(x)(1- f(x))$
    * $\displaystyle \frac{\partial z_3}{\partial w_5} = \frac{\partial }{\partial w_5}({w_5h_1 + w_6h_2}) = h_1 = 0.5199893$
  * $\displaystyle \frac{\partial Cost_{tot}}{\partial w_5} =  0.20944598 \times 0.23802158 \times 0.5199893 = 0.025922852$

  * $\displaystyle \frac{\partial Cost_{tot}}{\partial w_6} = 0.026295898 $
  * $\displaystyle \frac{\partial Cost_{tot}}{\partial w_7} = 0.0074084452$
  * $\displaystyle \frac{\partial Cost_{tot}}{\partial w_8} = 0.007515058$
* 각 Weight 업데이트($\alpha = 0.5$로 가정)
  * $w_5^+ =w_5 - \alpha\frac{\partial Cost_{tot}}{\partial w_5} = 0.45 - 0.5 \times 0.025922852 = 0.43703857 $
  * $w_6^+ =w_6 - \alpha\frac{\partial Cost_{tot}}{\partial w_6} = 0.4 - 0.5 \times 0.026295898 = 0.38685206 $
  * $w_7^+ =w_7 - \alpha\frac{\partial Cost_{tot}}{\partial w_7} = 0.7 - 0.5 \times 0.0074084452 = 0.69629574 $
  * $w_8^+ =w_8 - \alpha\frac{\partial Cost_{tot}}{\partial w_8} = 0.6 - 0.5 \times 0.007515058 = 0.5962425 $


"""

dw5 = -(y1-o1) * o1*(1-o1) * h1
dw6 = -(y1-o1) * o1*(1-o1) * h2
dw7 = -(y2-o2) * o2*(1-o2) * h1
dw8 = -(y2-o2) * o2*(1-o2) * h2
print(f'dw5:{dw5}, dw6:{dw6}, dw7:{dw7}, dw8:{dw8}')

lr = 0.5
w5_ = w5 - dw5 * lr
w6_ = w6 - dw6 * lr
w7_ = w7 - dw7 * lr
w8_ = w8 - dw8 * lr
print(f'w5+:{w5_}, w6+:{w6_}, w7+:{w7_}, w8+:{w8_}')

"""## Backpropagation Step-2

![](https://i.imgur.com/tukVuAB.png)

* $w_1, w_2, w_3, w_4$의 미분값 계산
  * $\displaystyle \frac{\partial Cost_{tot}}{\partial w_1} = \frac{\partial Cost_{tot}}{\partial h_1} \times \frac{\partial h_1}{\partial z_1} \times \frac{\partial z_1}{\partial w_1}$
    * $\displaystyle \frac{\partial Cost_{tot}}{\partial h_1} = \frac{\partial Cost_1}{\partial h_1}  +  \frac{\partial Cost_2}{\partial h_1} $
      * $\\displaystyle \frac{\partial Cost_1}{\partial h_1} = \frac{\partial Cost_1}{\partial o_1}  \times  \frac{\partial o_1}{\partial z_3} \times \frac{\partial z_3}{\partial h1} 
         = -(y_1 - o_1) o_1(1-o_1)w_5 
          = 0.022433696$
      * $\displaystyle \frac{\partial Cost_2}{\partial h_1} = \frac{\partial Cost_2}{\partial o_2}  \times  \frac{\partial o_2}{\partial z_4} \times \frac{\partial z_4}{\partial h1}
        = -(y_2-o_2)o_2(1-o_2)w_7 \\
        =  0.009973112$
      * $\displaystyle \frac{\partial Cost_{tot}}{\partial h_1} = 0.022433696 + 0.009973112 = 0.032406807 $
    * $\displaystyle \frac{\partial h_1}{\partial z_1} = h_1(1-h_1)  =  0.24960042536258698$
    * $\displaystyle \frac{\partial z_1}{\partial w_1} = x_1 = 0.1$
  * $\displaystyle \frac{\partial Cost_{tot}}{\partial w_1} = 0.032406807 \times 0.24960042536258698 \times 0.1  = 0.000808875251095742 $
  * $\displaystyle \frac{\partial Cost_{tot}}{\partial w_2} = 0.001617750502191484 $
  * $\displaystyle \frac{\partial Cost_{tot}}{\partial w_3} = 0.0007100860239006579 $
  * $\displaystyle \frac{\partial Cost_{tot}}{\partial w_4} = 0.0014201720478013158 $

* $w1, w2, w3, w4$ 업데이트
  * $w_1^+ = w_1- \alpha \frac{\partial Cost_{tot}}{\partial w_1} = 0.3 - 0.5\times 0.000808875251095742 = 0.29959556460380554$
  * $w_2^+ = w_2- \alpha \frac{\partial Cost_{tot}}{\partial w_2} = 0.25 - 0.5\times 0.001617750502191484 = 0.24919112026691437$
  * $w_3^+ = w_1- \alpha \frac{\partial Cost_{tot}}{\partial w_3} = 0.4 - 0.5\times 0.0007100860239006579 = 0.39964497089385986$
  * $w_4^+ = w_1- \alpha \frac{\partial Cost_{tot}}{\partial w_4} = 0.35 - 0.5\times 0.0014201720478013158 = 0.3492898941040039$
"""

dcost_h1_1 = -(y1 - o1) * o1*(1-o1)*w5
dcost_h1_2 = -(y2-o2)*o2*(1-o2)*w7
dcost_h1 = dcost_h1_1 + dcost_h1_2
print(f'dcost1:{dcost_h1_1}, dcost_2:{dcost_h1_2}, dcost:{dcost_h1}')

dcost_h2_1 = -(y1 - o1) *  o1*(1-o1)*w6
dcost_h2_2 = -(y2-o2)*o2*(1-o2)*w8
dcost_h2 = dcost_h2_1 + dcost_h2_2

dh1 = h1* (1-h1)
dh2 = h2*(1-h2)
print(f'dh1:{dh1}')
dw1 = dcost_h1 * dh1 * x1
dw2 = dcost_h1 * dh1 * x2
dw3 = dcost_h2 * dh2 * x1
dw4 = dcost_h2 * dh2 * x2
print(f'dw1:{dw1}, dw2:{dw2}, dw3:{dw3}, dw4:{dw4}')

w1_ = w1 - lr * dw1
w2_ = w2 - lr * dw2
w3_ = w3 - lr * dw3
w4_ = w4 - lr * dw4
print(f'w1+:{w1_}, w2+:{w2_}, w3+:{w3_}, w4+:{w4_}')

h1_ = tf.sigmoid(w1_*x1+w2_*x2)
h2_ = tf.sigmoid(w3_*x1+w4_*x2)
o1_ = tf.sigmoid(w5_*h1_+w6_*h2_)
o2_ = tf.sigmoid(w7_*h1_ + w8_*h2_)
cost_ = 1/2*(y1 - o1_)**2  +  1/2*(y2 - o2_)**2
print(f'updated cost:{cost_} improved:{cost-cost_}')

"""# XOR 문제 - MLP 학습
* 앞서 상수로 풀었던 XOR 문제를 MLP 학습으로 해결
"""

tf.random.set_seed(777)
np.random.seed(0)

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=np.float32)
y = np.array([[0], [1], [1], [0]], dtype=np.float32)

W1 = tf.Variable(tf.random.normal([2,2])) # [2,2] : 첫번깨는 입력 칼럼 개수, 두번째는 퍼센트론 유닛의 개수
b1 = tf.Variable(tf.random.normal([2]))
W2 = tf.Variable(tf.random.normal([2,1]))
b2 = tf.Variable(tf.random.normal([1]))

lr = 0.1
epochs = 10001
for epoch in range(epochs):
  with tf.GradientTape() as tape:
    layer1 = tf.sigmoid(tf.matmul(X,W1)+b1)
    h = tf.sigmoid(tf.matmul(layer1,W2)+b2)
    #cost = tf.keras.losses.MSE(y,h)
    mse = tf.keras.losses.MeanSquaredError()
    cost = mse(y, h)
    d_w1, d_b1, d_w2, d_b2 = tape.gradient(cost,[W1,b1,W2,b2])
    W1.assign_sub(lr*d_w1)
    W2.assign_sub(lr*d_w2)
    b1.assign_sub(lr*d_b1)
    b2.assign_sub(lr*d_b2)
    if epoch %500 == 0:
      print(f'epoch:{epoch}, cost:{cost}')
y_pred = tf.cast(h>=0.5, dtype=tf.float32)
acc = np.mean(y_pred==y)
print(f"Hypothesis:{h}, predict:{y_pred},acc:{acc}")
print(f"W1:{W1.numpy()},b1:{b1.numpy()},W2:{W2.numpy()},b2:{b2.numpy()}")

tf.random.set_seed(777)
np.random.seed(0)

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=np.float32)
y = np.array([[0], [1], [1], [0]], dtype=np.float32)

W1 = tf.Variable(tf.random.normal([2,2]))
b1 = tf.Variable(tf.random.normal([1,2]))
W2 = tf.Variable(tf.random.normal([2,1]))
b2 = tf.Variable(tf.random.normal([1]))

lr = 0.1
epochs = 10001
for epoch in range(epochs):
  with tf.GradientTape() as tape:
    layer1 = tf.sigmoid(tf.matmul(X,W1)+b1)
    h = tf.sigmoid(tf.matmul(layer1,W2)+b2)
    cost = tf.keras.losses.MSE(y,h)
    #mse = tf.keras.losses.MeanSquaredError()
    #cost = mse(y, h)
    d_w1, d_b1, d_w2, d_b2 = tape.gradient(cost,[W1,b1,W2,b2])
    W1.assign_sub(lr*d_w1)
    W2.assign_sub(lr*d_w2)
    b1.assign_sub(lr*d_b1)
    b2.assign_sub(lr*d_b2)
    if epoch %500 == 0:
      print(f'epoch:{epoch}, cost:{cost}')
y_pred = tf.cast(h>=0.5, dtype=tf.float32)
acc = np.mean(y_pred==y)
print(f"Hypothesis:{h}, predict:{y_pred},acc:{acc}")
print(f"W1:{W1.numpy()},b1:{b1.numpy()},W2:{W2.numpy()},b2:{b2.numpy()}")

"""# Optimizer 적용
* opt = tf.keras.optimizers.SGD(0.1)
* optimizer 시각화 : http://www.denizyuret.com/2015/03/alec-radfords-animations-for.html
"""

lst1 = [1,2,3,4]
lst2 = [10,20,30,40]
list(zip(lst1, lst2))

tf.random.set_seed(777)
np.random.seed(0)

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=np.float32)
y = np.array([[0], [1], [1], [0]], dtype=np.float32)

W1 = tf.Variable(tf.random.normal([2,2]))
b1 = tf.Variable(tf.random.normal([1,2]))
W2 = tf.Variable(tf.random.normal([2,1]))
b2 = tf.Variable(tf.random.normal([1]))

weights = [W1,b1, W2,b2]

lr = 0.1
opt = tf.keras.optimizers.SGD(learning_rate=lr,momentum=0.5)
epochs = 10001
for epoch in range(epochs):
  with tf.GradientTape() as tape:
    layer1 = tf.sigmoid(tf.matmul(X,W1)+b1)
    h = tf.sigmoid(tf.matmul(layer1,W2)+b2)
    cost = tf.keras.losses.MSE(y,h)
    #mse = tf.keras.losses.MeanSquaredError()
    #cost = mse(y, h)
#    d_w1, d_b1, d_w2, d_b2 = tape.gradient(cost,[W1,b1,W2,b2])
    gradients = tape.gradient(cost,weights)
    #W1.assign_sub(lr*d_w1)
    #W2.assign_sub(lr*d_w2)
    #b1.assign_sub(lr*d_b1)
    #b2.assign_sub(lr*d_b2)
#    opt.apply_gradients([(d_w1,W1),(d_b1,b1),(d_w2,W2),(d_b2,b2)])
    opt.apply_gradients(zip(gradients,weights))
    if epoch %500 == 0:
      print(f'epoch:{epoch}, cost:{cost}')
y_pred = tf.cast(h>=0.5, dtype=tf.float32)
acc = np.mean(y_pred==y)
print(f"Hypothesis:{h}, predict:{y_pred},acc:{acc}")
print(f"W1:{W1.numpy()},b1:{b1.numpy()},W2:{W2.numpy()},b2:{b2.numpy()}")