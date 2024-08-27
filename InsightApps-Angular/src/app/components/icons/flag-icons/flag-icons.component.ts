import { Component } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { SharedModule } from '../../../shared/sharedmodule';

@Component({
  selector: 'app-flag-icons',
  standalone:true,
  imports:[SharedModule,NgbModule],
  templateUrl: './flag-icons.component.html',
  styleUrls: ['./flag-icons.component.scss']
})
export class FlagIconsComponent {

}
