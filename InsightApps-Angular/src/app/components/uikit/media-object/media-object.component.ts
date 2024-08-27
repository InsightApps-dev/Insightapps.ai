import { Component } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-media-object',
  standalone: true,
  imports: [SharedModule,NgbModule],
  templateUrl: './media-object.component.html',
  styleUrls: ['./media-object.component.scss']
})
export class MediaObjectComponent {

}
