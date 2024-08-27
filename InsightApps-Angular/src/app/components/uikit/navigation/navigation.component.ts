import { Component, TemplateRef } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule, NgbOffcanvas, OffcanvasDismissReasons } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-navigation',
  standalone: true,
  imports: [SharedModule,NgbModule],
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.scss']
})
export class NavigationComponent {
  active=1;
  active1=2;
  constructor(private offcanvasService: NgbOffcanvas) {}
  closeResult = '';
  open(content: TemplateRef<any>) {
    this.offcanvasService.open(content, { position: 'end' });
  }
 

}
