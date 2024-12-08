import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class RLService {
  private apiUrl = 'http://127.0.0.1:5000'; // URL del backend

  constructor(private http: HttpClient) {}

  loadModel(): Observable<{ message: string }> {
    return this.http.get<{ message: string }>(`${this.apiUrl}/load-model`);
  }

  

  predict(state: number[]): Observable<{ action: number }> {
    return this.http.post<{ action: number }>(`${this.apiUrl}/predict`, { state });
  }

  calculateRoute(data: { 
    license_plate: string; 
    origin: string; 
    destination: string; 
  }): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/route`, data);
  }

  
}

