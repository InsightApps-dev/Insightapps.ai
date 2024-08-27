import { Component } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-typicon-icons',
  standalone:true,
  imports:[SharedModule,NgbModule],
  templateUrl: './typicon-icons.component.html',
  styleUrls: ['./typicon-icons.component.scss']
})
export class TypiconIconsComponent {

}
