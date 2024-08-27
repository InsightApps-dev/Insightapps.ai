import { Component } from '@angular/core';
import { Gallery, GalleryItem, GalleryModule, ImageItem } from 'ng-gallery';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { RouterModule } from '@angular/router';
import { LightboxModule } from 'ng-gallery/lightbox';
@Component({
  selector: 'app-search',
  standalone: true,
  imports: [SharedModule,NgbModule,RouterModule,GalleryModule,LightboxModule],
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent {
  active=1;
  items!: GalleryItem[];

  imageData = data;

  constructor(public gallery: Gallery) {}

  ngOnInit() {
    // Creat gallery items
    this.items = this.imageData.map((item) => {
      return new ImageItem({ src: item.srcUrl, thumb: item.previewUrl });
    });
  }
}  

const data = [
  {
    class:"col-xs-6 col-sm-4 col-md-4 col-xl-3 mb-4 border-bottom-0",
    srcUrl: "./assets/images/media/1.jpg",
    previewUrl: "./assets/images/media/1.jpg",
  },
  {
    class:"col-xs-6 col-sm-4 col-md-4 col-xl-3 mb-4 border-bottom-0",
    srcUrl: "./assets/images/media/2.jpg",
    previewUrl: "./assets/images/media/2.jpg",
  },
  {
    class:"col-xs-6 col-sm-4 col-md-4 col-xl-3 mb-4 border-bottom-0",
    srcUrl: "./assets/images/media/3.jpg",
    previewUrl: "./assets/images/media/3.jpg",
  },
  {
    class:"col-xs-6 col-sm-4 col-md-4 col-xl-3 mb-4 border-bottom-0",
    srcUrl: "./assets/images/media/4.jpg",
    previewUrl: "./assets/images/media/4.jpg"
  },
  {
    class:"col-xs-6 col-sm-4 col-md-4 col-xl-4 mb-4 border-bottom-0",
    srcUrl: './assets/images/media/5.jpg',
    previewUrl: './assets/images/media/5.jpg',
  },
  {
    class:"col-xs-6 col-sm-4 col-md-4 col-xl-4 mb-4 border-bottom-0",
    srcUrl: './assets/images/media/6.jpg',
    previewUrl: './assets/images/media/6.jpg',
  },
  {
    class:"col-xs-6 col-sm-4 col-md-4 col-xl-4 mb-4 border-bottom-0",
    srcUrl: './assets/images/media/7.jpg',
    previewUrl: './assets/images/media/7.jpg',
  },
  {
    class:"col-xs-6 col-sm-4 col-md-4 col-xl-3 mb-4 border-bottom-0",
    srcUrl: "./assets/images/media/8.jpg",
    previewUrl: "./assets/images/media/8.jpg",
  },
  {
    class:"col-xs-6 col-sm-4 col-md-4 col-xl-3 mb-4 border-bottom-0",
    srcUrl: "./assets/images/media/9.jpg",
    previewUrl: "./assets/images/media/9.jpg",
  },
  {
    class:"col-xs-6 col-sm-4 col-md-4 col-xl-3 mb-4 border-bottom-0",
    srcUrl: "./assets/images/media/10.jpg",
    previewUrl: "./assets/images/media/10.jpg",
  },
  {
    class:"col-xs-6 col-sm-4 col-md-4 col-xl-3 mb-4 border-bottom-0",
    srcUrl: "./assets/images/media/11.jpg",
    previewUrl: "./assets/images/media/11.jpg",
  },
];
