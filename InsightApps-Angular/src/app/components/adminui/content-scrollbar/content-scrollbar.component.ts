import { Component } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';
import { SimplebarAngularModule } from 'simplebar-angular';

@Component({
  selector: 'app-content-scrollbar',
  standalone: true,
  imports: [SharedModule,SimplebarAngularModule],
  templateUrl: './content-scrollbar.component.html',
  styleUrls: ['./content-scrollbar.component.scss']
})
export class ContentScrollbarComponent {

}
