import { Component, AfterViewInit } from '@angular/core';
import { RLService } from '../../services/rl.service';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import axios from 'axios';

declare const google: any;

@Component({
  standalone: true,
  selector: 'app-predict',
  imports: [FormsModule, HttpClientModule, CommonModule],
  templateUrl: './predict.component.html',
  styleUrls: ['./predict.component.css'],
})
export class PredictComponent implements AfterViewInit {
[x: string]: any;
  direccionOrigen: string = '';
  direccionDestino: string = '';
  map: any;
  directionsService: any;
  directionsRenderer: any;
  route: any;
  carMarker: any;
  stepIndex: number = 0;
  state: number[]= [0.5, 0.2, 0.1, 0.8];
  showModal: boolean = false;
  tiempoEstimado: string = '';
  gasolinaGastada: number = 0;
  precioGasolinaPorLitro: number = 12000;
  costoTrayecto: number = 0;
  clima: string = '';
  placa: string = '';
  bikeRoutes: any;
  showModal1: boolean = false;
  showModal2: boolean = false;
  showModal3: boolean = false;
  modalMessage: string = '';
  responses: boolean = false;
  responses2: boolean = false;
  distanciaTrayecto: number = 0;  
  

  private apiKey = 'ea557625ad034f98aed25148242111';

  constructor(private rlService: RLService) {}

  ngAfterViewInit() {
    this.initMap();
  }

  initMap() {
    this.map = new google.maps.Map(document.getElementById('map')!, {
      center: { lat: 4.60971, lng: -74.08175 },
      zoom: 13,
    });
    this.directionsService = new google.maps.DirectionsService();
    this.directionsRenderer = new google.maps.DirectionsRenderer();
    this.directionsRenderer.setMap(this.map);
  }

  realizarPrediccion() {
    const data = {
      license_plate: this.placa,
      origin: this.direccionOrigen,
      destination: this.direccionDestino,
    };

    this.rlService.loadModel().subscribe(
      (loadResponse) => {
        
        this.responses = true;

        this.rlService.predict(this.state).subscribe(


          (loadResponse) => {
          
            this.responses2 = true;


            this.rlService.calculateRoute(data).subscribe(

      
              (response) => {
                if (response.restricted) {
                  this.modalMessage = "Hoy no puedes circular con tu vehículo, por ende, te brindaremos una ruta alterna para ciclistas.";
                  this.showModal2 = true; 
                  this.trazarRuta3(response.bike_routes, true); // Ruta alterna para ciclistas
                } else {
                  this.trazarRuta(response.recommended_route, false); // Ruta recomendada para automóvil
                  this.modalMessage = "¡Llegaste al destino!";
                  setTimeout(() => {
                    this.showModal1 = true; 
                  }, 14000);
                }
              },
              (error) => {
                console.error(error);
                alert("Ocurrió un error al calcular la ruta.");
              }
            );



          },
          (error) => {
         
            console.error('Error al predecir con el modelo:', error);
            this.responses = false;
          }
    
    
          
        )

      },
      (error) => {
        
        console.error('Error al cargar el modelo:', error);
        this.responses = false;
      }
    );
    
  }


  
  trazarRuta(routeData: any, esPersona: boolean) {
    const origin = this.direccionOrigen;
    const destination = this.direccionDestino;
  
    const request = {
      origin: origin,
      destination: destination,
      travelMode: esPersona ? google.maps.TravelMode.WALKING : google.maps.TravelMode.DRIVING,
    };
  
    this.directionsService.route(request, (result: any, status: any) => {
      if (status === google.maps.DirectionsStatus.OK) {
        this.directionsRenderer.setDirections(result);
        this.route = result.routes[0].legs[0].steps;
        this.tiempoEstimado = result.routes[0].legs[0].duration.text;
        this.gasolinaGastada = esPersona ? 0 : this.simularGasolina(result.routes[0].legs[0].distance.value);
  
        // Calcular distancia y velocidad promedio
        const distanciaMetros = result.routes[0].legs[0].distance.value;
        this.distanciaTrayecto = distanciaMetros / 1000;  // Convertir de metros a kilómetros
  
        const duracionSegundos = result.routes[0].legs[0].duration.value;
        
  
        const destinoLat = result.routes[0].legs[0].end_location.lat();
        const destinoLng = result.routes[0].legs[0].end_location.lng();
        this.obtenerClima(destinoLat, destinoLng);
  
        this.iniciarMarcadores(result.routes[0].legs[0].start_location, result.routes[0].legs[0].end_location, esPersona);
        this.iniciarMovimientoCarro(esPersona);
      } else {
        alert('No se pudo trazar la ruta. Verifica las direcciones.');
        console.error('Error en DirectionsService:', status);
      }
    });
  }
  
  trazarRuta3(routeData: any, esPersona: boolean) {
    const origin = this.direccionOrigen;
    const destination = this.direccionDestino;
  
    const request = {
      origin: origin,
      destination: destination,
      travelMode: esPersona ? google.maps.TravelMode.WALKING : google.maps.TravelMode.DRIVING,
    };
  
    this.directionsService.route(request, (result: any, status: any) => {
      if (status === google.maps.DirectionsStatus.OK) {
        this.directionsRenderer.setDirections(result);
        this.route = result.routes[0].legs[0].steps;
        this.tiempoEstimado = result.routes[0].legs[0].duration.text;
        this.gasolinaGastada = esPersona ? 0 : this.simularGasolina(result.routes[0].legs[0].distance.value);
  
        // Calcular distancia y velocidad promedio
        const distanciaMetros = result.routes[0].legs[0].distance.value;
        this.distanciaTrayecto = distanciaMetros / 1000;  // Convertir de metros a kilómetros
  
        const duracionSegundos = result.routes[0].legs[0].duration.value;
        
  
        const destinoLat = result.routes[0].legs[0].end_location.lat();
        const destinoLng = result.routes[0].legs[0].end_location.lng();
        this.obtenerClima(destinoLat, destinoLng);
  
        this.iniciarMarcadores(result.routes[0].legs[0].start_location, result.routes[0].legs[0].end_location, esPersona);
        this.iniciarMovimientoCarro3(esPersona);
      } else {
        alert('No se pudo trazar la ruta. Verifica las direcciones.');
        console.error('Error en DirectionsService:', status);
      }
    });
  }
  
  

  iniciarMarcadores(startLocation: any, endLocation: any, esPersona: boolean) {
    const icon = esPersona 
      ? 'assets/person-icon.png' 
      : 'assets/car-icon.png';
  
    // Marcador de origen
    new google.maps.Marker({
      position: startLocation,
      map: this.map,
      title: esPersona ? 'Inicio del recorrido a pie' : 'Origen',
      icon: {
        url: icon,
        scaledSize: new google.maps.Size(32, 32),
      },
    });
  
    // Marcador de destino
    new google.maps.Marker({
      position: endLocation,
      map: this.map,
      title: 'Destino',
      icon: {
        url: 'assets/destination-icon.png',
        scaledSize: new google.maps.Size(32, 32),
      },
    });
  }
  

  iniciarMovimientoCarro(esPersona: boolean) {
    const icon = esPersona
      ? 'assets/person-icon.png'
      : 'assets/car-icon.png';
  
    this.carMarker = new google.maps.Marker({
      position: this.route[0].start_location,
      map: this.map,
      icon: {
        url: icon,
        scaledSize: new google.maps.Size(32, 32),
      },
      title: esPersona ? 'Persona en movimiento' : 'Carro',
    });
  
    this.moverCarro();
  }

  iniciarMovimientoCarro3(esPersona: boolean) {
    const icon = esPersona
      ? 'assets/person-icon.png'
      : 'assets/car-icon.png';
  
    this.carMarker = new google.maps.Marker({
      position: this.route[0].start_location,
      map: this.map,
      icon: {
        url: icon,
        scaledSize: new google.maps.Size(32, 32),
      },
      title: esPersona ? 'Persona en movimiento' : 'Carro',
    });
  
    this.moverCarro2();
  }
  
  moverCarro() {
    if (this.stepIndex < this.route.length) {
      const step = this.route[this.stepIndex];
  
      // Mueve el carro al siguiente punto
      this.carMarker.setPosition(step.start_location);
  
      // Incrementa el índice de los pasos
      this.stepIndex++;
  
      // Llama a la función nuevamente para continuar moviendo el carro
      setTimeout(() => {
        this.moverCarro();
      }, 500); // El carro se mueve cada 500 ms para una animación más fluida
    } else {
      // Cuando el carro llega al destino, muestra el modal
      this.mostrarModal();
    }
  }
  
  moverCarro2() {
    if (this.stepIndex < this.route.length) {
      const step = this.route[this.stepIndex];
  
      
      this.carMarker.setPosition(step.start_location);
  
     
      this.stepIndex++;
  
     
      setTimeout(() => {
        this.moverCarro2();
      }, 500); 
    } else {
     
      this.mostrarModal3();
    }
  }


  obtenerClima(lat: number, lng: number) {
    const bogotaLat = 4.60971;
    const bogotaLng = -74.08175;

    axios
      .get(`https://api.weatherapi.com/v1/current.json?key=${this.apiKey}&q=${bogotaLat},${bogotaLng}&aqi=no&lang=es`)
      .then((response) => {
        this.clima = response.data.current.condition.text;
      })
      .catch((error) => {
        console.error('Error al obtener el clima:', error);
        this.clima = 'No disponible';
      });
  }

  simularGasolina(distanciaMetros: number): number {
    const consumoPorKm = 0.08;
    const distanciaKm = distanciaMetros / 1000;
    return +(distanciaKm * consumoPorKm).toFixed(2);
  }

  calcularCostoTrayecto() {
    this.costoTrayecto = this.gasolinaGastada * this.precioGasolinaPorLitro;
  }

  mostrarModal() {
    this.calcularCostoTrayecto();
    this.showModal1 = true;
  }

  cerrarModal1() {
    this.showModal1 = false;
    window.location.reload()
  }


  cerrarModal2() {
    this.showModal2 = false;
  }

  mostrarModal3() {
    this.calcularCostoTrayecto();
    this.showModal3 = true;
  }

  cerrarModal3() {
    this.showModal3 = false;
    window.location.reload()
  }


}


  
  

