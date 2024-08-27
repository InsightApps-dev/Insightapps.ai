import { Component } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';
import { SimplebarAngularModule } from 'simplebar-angular';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [SharedModule,SimplebarAngularModule,NgbModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss']
})
export class ChatComponent {
active=1;
}
