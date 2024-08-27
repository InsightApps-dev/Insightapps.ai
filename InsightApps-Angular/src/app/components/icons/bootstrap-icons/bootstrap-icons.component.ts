import { Component } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { SharedModule } from '../../../shared/sharedmodule';

@Component({
  selector: 'app-bootstrap-icons',
  standalone:true,
  imports:[SharedModule,NgbModule],
  templateUrl: './bootstrap-icons.component.html',
  styleUrls: ['./bootstrap-icons.component.scss']
})
export class BootstrapIconsComponent {

}
