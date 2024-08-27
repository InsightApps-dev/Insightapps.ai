import { Component } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-tooltip-popover',
  standalone: true,
  imports: [SharedModule,NgbModule],
  templateUrl: './tooltip-popover.component.html',
  styleUrls: ['./tooltip-popover.component.scss']
})
export class TooltipPopoverComponent {

}
