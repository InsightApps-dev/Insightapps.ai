import { Component } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-pe7-icons',
  standalone:true,
  imports:[SharedModule,NgbModule],
  templateUrl: './pe7-icons.component.html',
  styleUrls: ['./pe7-icons.component.scss']
})
export class Pe7IconsComponent {

}
