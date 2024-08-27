import { Component } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { NgSelectModule } from '@ng-select/ng-select';
import { SharedModule } from '../../../shared/sharedmodule';

@Component({
  selector: 'app-form-input-spinners',
  standalone: true,
  imports: [SharedModule,NgSelectModule,NgbModule],
  templateUrl: './form-input-spinners.component.html',
  styleUrls: ['./form-input-spinners.component.scss']
})
export class FormInputSpinnersComponent {

}
