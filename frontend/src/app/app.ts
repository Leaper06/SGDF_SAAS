import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet], 
  templateUrl: './app.html',
  styleUrls: ['./app.scss'] // (ou './app.css' si tu n'utilises pas SASS)
})
export class AppComponent {
  title = 'PolyMaîtrise';
}