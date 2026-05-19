import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common'; // Requis pour les pipes et directives
import { CampService } from '../../services/camp.service';
import { Camp } from '../../models/camp.model';

@Component({
  selector: 'app-calendar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.css']
})
export class CalendarComponent implements OnInit {
  campsList: Camp[] = [];
  errorMessage: string = '';
  loading: boolean = true;

  constructor(private campService: CampService) {}

  ngOnInit(): void {
    this.loadCalendarEvents();
  }

  loadCalendarEvents(): void {
    this.campService.getallCamps().subscribe({
      next: (response) => {
        if (response.status === 'success') {
          this.campsList = response.data;
        }
        this.loading = false;
      },
      error: (err) => {
        console.error('Erreur lors du chargement du calendrier:', err);
        this.errorMessage = 'Impossible de charger les événements.';
        this.loading = false;
      }
    });
  }
}