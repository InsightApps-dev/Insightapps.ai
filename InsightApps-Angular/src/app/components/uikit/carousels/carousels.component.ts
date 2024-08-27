import { Component } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-carousels',
  standalone: true,
  imports: [SharedModule,NgbModule],
  templateUrl: './carousels.component.html',
  styleUrls: ['./carousels.component.scss']
})
export class CarouselsComponent {
  images = [
    "./assets/images/media/19.jpg",
    "./assets/images/media/21.jpg",
    "./assets/images/media/20.jpg",
    "./assets/images/media/22.jpg",
    "./assets/images/media/23.jpg"
  ];
  images1 = [
    "./assets/images/media/24.jpg",
    "./assets/images/media/25.jpg",
    "./assets/images/media/1.jpg",
    "./assets/images/media/2.jpg",
    "./assets/images/media/3.jpg"
  ];
  images2 = [
    "./assets/images/media/4.jpg",
    "./assets/images/media/5.jpg",
    "./assets/images/media/6.jpg",
    "./assets/images/media/7.jpg",
    "./assets/images/media/8.jpg"
  ];
  images3 = [
    "./assets/images/media/14.jpg",
    "./assets/images/media/15.jpg",
    "./assets/images/media/17.jpg",
   
  ];
  images4 = [
    "./assets/images/media/3.jpg",
    "./assets/images/media/4.jpg",
    "./assets/images/media/5.jpg",
   
  ];
  images5 = [
    "./assets/images/media/14.jpg",
    "./assets/images/media/15.jpg",
    "./assets/images/media/16.jpg",
    "./assets/images/media/17.jpg",
    "./assets/images/media/18.jpg"
  ];
  darkimg = [
    './assets/images/media/media-63.jpg',
    './assets/images/media/media-62.jpg',
    './assets/images/media/media-64.jpg',
  ];
}
