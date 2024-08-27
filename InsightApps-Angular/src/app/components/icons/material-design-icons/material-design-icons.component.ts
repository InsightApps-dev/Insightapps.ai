import { Component } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { SharedModule } from '../../../shared/sharedmodule';

@Component({
  selector: 'app-material-design-icons',
  standalone:true,
  imports:[SharedModule,NgbModule],
  templateUrl: './material-design-icons.component.html',
  styleUrls: ['./material-design-icons.component.scss']
})
export class MaterialDesignIconsComponent {

}
