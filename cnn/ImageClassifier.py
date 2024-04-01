#from tensorflow import
from tensorflow.keras import datasets, models, losses
from tensorflow.keras.layers import Conv2D, BatchNormalization, MaxPooling2D, Flatten, Dense, Dropout
from matplotlib.pyplot import (subplot, xticks, yticks, cm, imshow as pltImshow,
                               show as pltShow, figure, grid, xlabel)
from numpy import argmax as npArgmax
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, LearningRateScheduler
from tensorflow.keras.regularizers import L2
from tensorflow.math import exp as tfExp



def scheduler(epoch, lr):
    if epoch < 10:
        return float(lr)
    else:
        return float(lr * tfExp(-0.1))
lr_scheduler = LearningRateScheduler(scheduler)


early_stopping = EarlyStopping(monitor='val_loss',
                               patience=10,
                               restore_best_weights=True)

# Cargar y dividir el dataset CIFAR-10
(train_images, train_labels), (test_images,
                               test_labels) = datasets.cifar10.load_data()

# Normalizar los valores de píxeles al rango [0,1]
train_images, test_images = train_images / 255.0, test_images / 255.0

# Definir la arquitectura de la red neuronal convolucional
model = models.Sequential([
    Conv2D(32,
          (3, 3),
           activation='relu',
           input_shape=(32, 32, 3)),
    BatchNormalization(),
    Conv2D(32, (3, 3), activation='relu', kernel_regularizer=L2(0.001)),
    MaxPooling2D((2, 2)),
    Dropout(0.25),

    Conv2D(64, (3, 3), activation='relu'),
    BatchNormalization(),
    Conv2D(64, (3, 3), activation='relu', kernel_regularizer=L2(0.001)),
    MaxPooling2D((2, 2)),
    Dropout(0.25),

    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(10, activation='softmax', kernel_regularizer=L2(0.001))
])

# Compilar el modelo
optimizer = Adam(learning_rate=0.001)
model.compile(optimizer=optimizer,
              loss=losses.SparseCategoricalCrossentropy(
                  from_logits=True),
              metrics=['accuracy'])

# Entrenar el modelo
model.fit(train_images,
          train_labels,
          epochs=200,
          validation_data=(test_images, test_labels),
          callbacks=[early_stopping, lr_scheduler])

# Evaluar la precisión del modelo en el conjunto de prueba
test_loss, test_acc = model.evaluate(test_images, test_labels)
print(f'Exactitud del modelo: {test_acc:.2f}')
print(f'Pérdida del modelo: {test_loss:.2f}')

# Realizar predicciones en el conjunto de prueba
predictions = model.predict(test_images)

# Clases posibles en CIFAR-10
class_names = ['avión', 'automóvil', 'pájaro', 'gato', 'ciervo',
               'perro', 'rana', 'caballo', 'barco', 'camión']

# Mostrar imágenes con etiquetas predichas y reales
figure(figsize=(15, 15))
for i in range(25):
    subplot(5, 5, i + 1)
    xticks([])
    yticks([])
    grid(False)
    pltImshow(test_images[i], cmap=cm.binary)

    # Calcular la etiqueta predicha y la etiqueta real
    predicted_label = npArgmax(predictions[i])
    true_label = test_labels[i][0]

    # Mostrar la etiqueta predicha y la etiqueta real
    if predicted_label == true_label:
        color = 'green'
    else:
        color = 'red'

    xlabel("Pred: {} \nReal: {}".format(class_names[predicted_label],
                                            class_names[true_label]), color=color)

pltShow()
