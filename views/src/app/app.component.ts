import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { PredictComponent } from "./components/predict/predict.component";
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, PredictComponent,FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'views';
}
