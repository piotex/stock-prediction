import numpy as np
import matplotlib.pyplot as plt

# Generowanie danych
x = np.linspace(0, 10, 100)
y1 = np.sin(x)  # Wykres sinusoidy
y2 = np.cos(x)  # Wykres cosinusoidy

# Tworzenie wykresów w układzie 2 wierszy i 1 kolumny
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))  # figsize ustawia rozmiar figury

# Wykres 1
ax1.plot(x, y1, color='blue', label='sin(x)')
ax1.set_title('Wykres sin(x)')
ax1.set_xlabel('Oś X')
ax1.set_ylabel('sin(x)')
ax1.legend()
ax1.grid(True)

# Wykres 2
ax2.plot(x, y2, color='red', label='cos(x)')
ax2.set_title('Wykres cos(x)')
ax2.set_xlabel('Oś X')
ax2.set_ylabel('cos(x)')
ax2.legend()
ax2.grid(True)

# Ustawienie odstępu między wykresami
plt.subplots_adjust(hspace=0.4)

# Wyświetlenie wykresów
plt.show()