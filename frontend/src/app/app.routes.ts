import { Routes } from '@angular/router';

export const routes: Routes = [
  // Quand l'utilisateur arrive sur le site (chaîne vide), on le redirige vers /calendar
  { 
    path: '', 
    redirectTo: 'calendar', 
    pathMatch: 'full' 
  },
  // Déclaration de notre page Calendrier
  { 
    path: 'calendar', 
    loadComponent: () => import('./pages/calendar/calendar.component').then(m => m.CalendarComponent) 
  }
];