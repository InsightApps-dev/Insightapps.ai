import { Component } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-font-awesome-icons',
  standalone:true,
  imports:[SharedModule,NgbModule],
  templateUrl: './font-awesome-icons.component.html',
  styleUrls: ['./font-awesome-icons.component.scss']
})
export class FontAwesomeIconsComponent {

}
