#from tensorflow import 
from tensorflow.keras import datasets, layers, models, losses
from matplotlib.pyplot import (subplot, xticks, yticks, cm, imshow as pltImshow, 
                               show as pltShow, figure, grid, xlabel)
from numpy import argmax as npArgmax

# Cargar y dividir el dataset CIFAR-10
(train_images, train_labels), (test_images,
                               test_labels) = datasets.cifar10.load_data()

# Normalizar los valores de píxeles al rango [0,1]
train_images, test_images = train_images / 255.0, test_images / 255.0

# Definir la arquitectura de la red neuronal convolucional
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10)
])

# Compilar el modelo
model.compile(optimizer='adam',
              loss=losses.SparseCategoricalCrossentropy(
                  from_logits=True),
              metrics=['accuracy'])

# Entrenar el modelo
model.fit(train_images, train_labels, epochs=10)

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
