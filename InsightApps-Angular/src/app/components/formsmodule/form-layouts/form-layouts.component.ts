import { Component } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgSelectModule } from '@ng-select/ng-select';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-form-layouts',
  standalone: true,
  imports: [SharedModule,NgSelectModule,NgbModule],
  templateUrl: './form-layouts.component.html',
  styleUrls: ['./form-layouts.component.scss']
})
export class FormLayoutsComponent {
active=1;
}
