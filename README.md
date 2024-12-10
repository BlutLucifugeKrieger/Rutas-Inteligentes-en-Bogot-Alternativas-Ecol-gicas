# Rutas Inteligentes en Bogotá - Alternativas Ecológicas

Juan Camilo Castro Velasquez

El propósito de este trabajo es desarrollar e implementar una solución innovadora para mejorar la movilidad urbana en Bogotá, 
enfocándose en ofrecer alternativas sostenibles y eficientes frente al reto del Pico y Placa. A través del uso de inteligencia artificial, específicamente con técnicas de aprendizaje por refuerzo (RL)


## Descripción

El sistema analiza la situación del tráfico y el clima para sugerir las mejores rutas para los usuarios, teniendo en cuenta tanto los vehículos como las opciones ecológicas para ciclistas. 

### Características principales:.
- **Integración con Google Maps**: Utiliza la API de Google Maps para la geocodificación y trazado de rutas.
- **Clima en tiempo real**: Obtención de información meteorológica actual para el destino.
- **Restricciones de tránsito**: El sistema verifica si un vehículo está restringido para circular en ciertas zonas y sugiere rutas alternativas si es necesario.
- **Alternativas ecológicas**: Ofrece rutas ecológicas para ciclistas en caso de restricciones de tránsito para vehículos.

## Requisitos

Para ejecutar este proyecto en tu máquina local, asegúrate de tener los siguientes requisitos:

- Python 3.x
- Node.js
- npm o yarn (para gestionar dependencias de front-end)
- Claves API de Google Maps y WeatherAPI

### Librerías necesarias

1. **Backend**: 
   - `Flask` para crear el servidor backend.
   - `googlemaps` para interactuar con la API de Google Maps.
   - `requests` para obtener datos de clima en tiempo real.
   
   Instálalas con:
   ```bash
   pip install -r requirements.txt


2. **Frontend**: 
- **Angular**: Para la interfaz de usuario.
- **Axios**: Para la interacción con la API backend.
   
  #### Instalación de dependencias:

  Ejecuta el siguiente comando para instalar las dependencias necesarias:
   ```bash
   npm install
   
### 2. **Frontend**

- **Angular**: Para la interfaz de usuario.
- **Axios**: Para la interacción con la API backend.

#### Instalación de dependencias:

Ejecuta el siguiente comando para instalar las dependencias necesarias:

```bash
npm install





