import { Component } from '@angular/core';
import { SharedModule } from '../../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-pricing-tables',
  standalone: true,
  imports: [SharedModule,NgbModule],
  templateUrl: './pricing-tables.component.html',
  styleUrls: ['./pricing-tables.component.scss']
})
export class PricingTablesComponent {
active=1;
active1=3;
}
