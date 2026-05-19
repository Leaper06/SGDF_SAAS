import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Camp, ApiResponse } from '../models/camp.model';

@Injectable({
  providedIn: 'root'
})
export class CampService {
  // En dev local, l'API tourne sur le port 5000 de Flask
  private apiUrl = 'http://localhost:5000/api/camps';

  constructor(private http: HttpClient) {}

  /**
   * Récupère la liste de tous les camps ordonnés par date
   */
  getallCamps(): Observable<ApiResponse<Camp[]>> {
    return this.http.get<ApiResponse<Camp[]>>(this.apiUrl);
  }
}