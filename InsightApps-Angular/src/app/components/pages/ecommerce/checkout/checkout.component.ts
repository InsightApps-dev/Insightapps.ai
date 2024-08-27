import { Component } from '@angular/core';
import { SharedModule } from '../../../../shared/sharedmodule';
import { NgSelectModule } from '@ng-select/ng-select';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-checkout',
  standalone: true,
  imports: [SharedModule,NgSelectModule,NgbModule],
  templateUrl: './checkout.component.html',
  styleUrls: ['./checkout.component.scss']
})
export class CheckoutComponent {
active=1;
}
