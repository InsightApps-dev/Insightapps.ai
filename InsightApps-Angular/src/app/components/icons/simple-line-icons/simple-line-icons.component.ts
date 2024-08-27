import { Component } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-simple-line-icons',
  standalone:true,
  imports:[SharedModule,NgbModule],
  templateUrl: './simple-line-icons.component.html',
  styleUrls: ['./simple-line-icons.component.scss']
})
export class SimpleLineIconsComponent {

}
