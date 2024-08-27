import { Component } from '@angular/core';
import { SharedModule } from '../../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-blog-details',
  standalone: true,
  imports: [SharedModule,NgbModule,CommonModule,RouterModule],
  templateUrl: './blog-details.component.html',
  styleUrls: ['./blog-details.component.scss']
})
export class BlogDetailsComponent {

}
