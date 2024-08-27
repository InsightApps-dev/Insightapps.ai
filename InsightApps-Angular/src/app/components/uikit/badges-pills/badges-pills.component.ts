import { Component } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-badges-pills',
  standalone: true,
  imports: [SharedModule,NgbModule],
  templateUrl: './badges-pills.component.html',
  styleUrls: ['./badges-pills.component.scss']
})
export class BadgesPillsComponent {

}
