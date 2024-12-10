import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

class RLAgent:
    def __init__(self, state_size, action_size, model_save_path="C:/Users/juanl/Documents/SoftwareAvanzado/gelm/final_project/rl_model.h5"):
        self.state_size = state_size
        self.action_size = action_size
        self.discount_factor = 0.95  # Factores de descuento
        self.learning_rate = 0.001  # Tasa de aprendizaje
        self.epsilon = 1.0          # Explora inicialmente
        self.epsilon_decay = 0.995  # Decaimiento de la exploración
        self.epsilon_min = 0.01     # Mínimo de exploración
        self.model_save_path = model_save_path

        # Inicializa el modelo
        self.model = self._build_model()
        self.episode_rewards = []  # Registro de recompensas por episodio

    def _build_model(self):
        """Crea un modelo de red neuronal para el agente."""
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def act(self, state):
        """Selecciona una acción basada en el estado."""
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)  # Explora
        act_values = self.model.predict(state, verbose=0)  # Explota
        return np.argmax(act_values[0])

    def train(self, state, action, reward, next_state, done):
        """Entrena el modelo utilizando Q-learning."""
        target = reward
        if not done:
            target += self.discount_factor * np.amax(self.model.predict(next_state, verbose=0)[0])

        target_f = self.model.predict(state, verbose=0)
        target_f[0][action] = target

        self.model.fit(state, target_f, epochs=1, verbose=0)

        # Ajustar epsilon para exploración/explotación
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        # Guardar automáticamente después de cada episodio
        if done:
            self.save_model()

    def save_model(self):
        """Guarda el modelo entrenado."""
        self.model.save(self.model_save_path)
        print(f"Modelo guardado en {self.model_save_path}")



