import { Component } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { SharedModule } from '../../../shared/sharedmodule';

@Component({
  selector: 'app-weather-icons',
  standalone:true,
  imports:[SharedModule,NgbModule],
  templateUrl: './weather-icons.component.html',
  styleUrls: ['./weather-icons.component.scss']
})
export class WeatherIconsComponent {

}
