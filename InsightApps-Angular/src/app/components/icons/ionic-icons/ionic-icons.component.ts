import { Component } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-ionic-icons',
  standalone:true,
  imports:[SharedModule,NgbModule],
  templateUrl: './ionic-icons.component.html',
  styleUrls: ['./ionic-icons.component.scss']
})
export class IonicIconsComponent {

}
