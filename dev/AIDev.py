import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

class AIPMDevelopment:

    # Simple feedforward neural network
    
    def __init__(self):
        # Read your data in and split the dependent and independent
        data = pd.read_csv('IBM.csv')
        X = data.drop(['Delta Close'], axis=1)
        y = data['Delta Close']

        # Train test spit
        X_train, X_test, y_train, y_test = train_test_split(X, y)

        # Create the sequential
        network = Sequential()

        # Create the structure of the neural network
        network.add(Dense(1, input_shape=(X_train.shape[1],), activation='tanh'))
        network.add(Dense(3, activation='tanh'))
        network.add(Dense(3, activation='tanh'))
        network.add(Dense(3, activation='tanh'))
        network.add(Dense(1, activation='tanh'))

        # Compile the model
        network.compile(
                      optimizer='rmsprop',
                      loss='hinge',
                      metrics=['accuracy']
                      )
        # Train the model
        network.fit(X_train.values, y_train.values, epochs=100)

        # Evaluate the predictions of the model
        y_pred = network.predict(X_test.values)
        y_pred = np.around(y_pred, 0)
        print(classification_report(y_test, y_pred))

        # Save structure to json
        model = network.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model)

        # Save weights to HDF5
        network.save_weights("weights.h5")

AIPMDevelopment()
