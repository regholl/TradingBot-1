import numpy as np
import pandas as pd
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout, SimpleRNN
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from hmmlearn.hmm import GaussianHMM
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score



def preProcess(data):
    # Check for NaN values
    print(data.isnull().sum())

    # Drop rows with NaN values
    data = data.dropna()

    # Create a scaler
    scaler = MinMaxScaler(feature_range=(0, 1))

    # Only include numerical columns in the data that you pass to the scaler
    numerical_columns = data.select_dtypes(include=[np.number]).columns

    # Fit the scaler to your data and transform it
    data[numerical_columns] = scaler.fit_transform(data[numerical_columns])

    data = data.select_dtypes(exclude=['object'])

    return data

class LinearRegressor(): 

    def __init__(self):
        self.model = Sequential()

    def train(self, data): 

        data = preProcess(data)

        X = data.drop(['Close'], axis=1)
        y = data['Close']

        X_train, X_test, Y_train, Y_test = train_test_split(X, y)

        self.model.add(Dense(1, input_shape=(X_train.shape[1],), activation='tanh'))
        self.model.add(Dense(3, activation='tanh'))
        self.model.add(Dense(3, activation='tanh'))
        self.model.add(Dense(3, activation='tanh'))
        self.model.add(Dense(1, activation='tanh'))

        self.model.compile(
                      optimizer='rmsprop',
                      loss='hinge',
                      metrics=['accuracy']
                      )

        X_train = X_train.values.astype('float32')
        Y_train = Y_train.values.astype('float32')
        self.model.fit(X_train, Y_train, epochs=100)

        # Evaluate the model
        test_loss, test_mae = self.model.evaluate(X_test, Y_test)

        print('Test loss:', test_loss)
        print('Test MAE:', test_mae)

        self.model.save('models/LinearRegressor.h5')

    def predict(self, X):
        self.model = load_model('models/LinearRegressor.h5')
        predictions = self.model.predict(X)
        return predictions

class RNN(): 
    def __init__(self): 
        self.model = Sequential()

    def train(self, data): 
        
        data = preProcess(data)

        prices = data['Close'].values.reshape(-1, 1)

        scaler = MinMaxScaler(feature_range=(0, 1))
        prices = scaler.fit_transform(prices)

        look_back = 10
        X, Y = self.create_dataset(prices, look_back)

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        self.model.add(SimpleRNN(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        self.model.add(Dropout(0.2))
        self.model.add(SimpleRNN(units=50))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(1))

        self.model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mean_absolute_error'])
        self.model.fit(X_train, Y_train, epochs=100, batch_size=32)

        # Evaluate the model
        test_loss, test_mae = self.model.evaluate(X_test, Y_test)

        print('Test loss:', test_loss)
        print('Test MAE:', test_mae)

        self.model.save('models/RNN.h5')

    def predict(self, X): 
        self.model = load_model('models/RNN.h5')
        predictions = self.model.predict(X)
        return predictions
    
    @staticmethod
    def create_dataset(dataset, look_back=1):
        X, Y = [], []
        for i in range(len(dataset)-look_back-1):
            a = dataset[i:(i+look_back), 0]
            X.append(a)
            Y.append(dataset[i + look_back, 0])
        return np.array(X), np.array(Y)

class LSTMModel(): 
    def __init__(self): 
        self.model = Sequential()

    def train(self, data):
        data = preProcess(data)
        prices = data['Close'].values.reshape(-1, 1)

        scaler = MinMaxScaler(feature_range=(0, 1))
        prices = scaler.fit_transform(prices)

        look_back = 10
        X, Y = self.create_dataset(prices, look_back)

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))


        self.model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(units=50))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(1))

        self.model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mean_absolute_error'])
        self.model.fit(X_train, Y_train, epochs=100, batch_size=32)


        # Evaluate the model
        test_loss, test_mae = self.model.evaluate(X_test, Y_test)

        print('Test loss:', test_loss)
        print('Test MAE:', test_mae)

        self.model.save('models/LSTM.h5')

    def predict(self, X): 
        self.model = load_model('models/LSTM.h5')
        predictions = self.model.predict(X)
        return predictions

    @staticmethod
    def create_dataset(dataset, look_back=1):
        X, Y = [], []
        for i in range(len(dataset)-look_back-1):
            a = dataset[i:(i+look_back), 0]
            X.append(a)
            Y.append(dataset[i + look_back, 0])
        return np.array(X), np.array(Y)

class HMM: 

    def __init__(self): 
        self.model = None

    def train(self, data): 
        data = preProcess(data)

        # Extract the Close column
        close_data = data[["Close"]].values

        # Fit an HMM model
        self.model = GaussianHMM(n_components=3, covariance_type="full", n_iter=1000)
        self.model.fit(close_data)

        # Save the model
        joblib.dump(self.model, "HMM.pkl")

    def predict(self): 
        # Load the model
        self.model = joblib.load("HMM.pkl")

        # Predict hidden states
        hidden_states = self.model.predict(close_data)

        return hidden_states

    def print_details(self): 
        if self.model is None: 
            print("Model not trained yet")
            return

        # Print state transitions
        print("Transition matrix")
        print(self.model.transmat_)

        # Print the means and covariances of each state
        for i in range(self.model.n_components):
            print(f"Mean of state {i+1}: {self.model.means_[i][0]:.2f}")
            print(f"Covariance of state {i+1}:")
            print(self.model.covars_[i])
            print()
