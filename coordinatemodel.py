import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
import random
#%matplotlib inline
import matplotlib.pyplot as plt

xy = np.loadtxt('드론 좌표 27개 방향3.csv', delimiter=',', dtype=np.float)

x_data = xy[:, 0:-1]
y_data = xy[:, [-1]]

x_test = xy[-1:-100, 0:-1]
y_test = xy[-1:-100, [-1]]

y_data = to_categorical(y_data, num_classes=27)
y_test = to_categorical(y_test, num_classes=27)

model = Sequential()
model.add(Dense(108, input_dim=3, activation='relu'))
model.add(Dense(54, activation='relu'))
model.add(Dense(27, activation='softmax'))

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

hist = model.fit(x_data, y_data, nb_epoch=6000, batch_size=64)



fig, loss_ax = plt.subplots()

acc_ax = loss_ax.twinx()

loss_ax.set_ylim([0.0, 3.0])
acc_ax.set_ylim([0.0, 1.0])

loss_ax.plot(hist.history['loss'], 'y', label='train loss')
acc_ax.plot(hist.history['acc'], 'b', label='train acc')

loss_ax.set_xlabel('epoch')
loss_ax.set_ylabel('loss')
acc_ax.set_ylabel('accuray')

loss_ax.legend(loc='upper left')
acc_ax.legend(loc='lower left')

plt.show()

# 6. 모델 평가하기
loss_and_metrics = model.evaluate(x_test, y_test, batch_size=32)
print('loss_and_metrics : ' + str(loss_and_metrics))

from keras.models import load_model
model.save('model.h5')