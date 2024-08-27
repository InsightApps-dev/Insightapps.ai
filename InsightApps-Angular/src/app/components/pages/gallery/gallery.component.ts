
import { Component, ViewEncapsulation } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { ModalGalleryRef, ModalGalleryService ,Image} from '@ks89/angular-modal-gallery';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { Gallery, GalleryItem, GalleryModule, ImageItem } from 'ng-gallery';
import { SharedModule } from '../../../shared/sharedmodule';
import { LightboxModule } from 'ng-gallery/lightbox';

@Component({
  selector: 'app-gallery',
  standalone:true,
  imports: [SharedModule, NgbModule, GalleryModule,LightboxModule],
  templateUrl: './gallery.component.html',
  styleUrls: ['./gallery.component.scss'],
  encapsulation: ViewEncapsulation.None

})
export class GalleryComponent {
  active!:1;
  items!: GalleryItem[];

  imageData = data;
  imageData1 = data1;
  imageData2 = data2;
  imageData3 = data3;
  imageData4 = data4;
  imageData5 = data5;

  constructor(public gallery: Gallery) {}

  ngOnInit() {
    // Creat gallery items
    this.items = this.imageData.map((item) => {
      return new ImageItem({ src: item.srcUrl, thumb: item.previewUrl });
    });
      // Creat gallery items
      this.items = this.imageData1.map((item) => {
        return new ImageItem({ src: item.srcUrl, thumb: item.previewUrl });
      });
  }
  
}

const data = [
  {
    srcUrl: "./assets/images/media/1.jpg",
    previewUrl: "./assets/images/media/1.jpg",
  },
  {
    srcUrl: "./assets/images/media/2.jpg",
    previewUrl: "./assets/images/media/2.jpg",
  },
  {
    srcUrl: "./assets/images/media/3.jpg",
    previewUrl: "./assets/images/media/3.jpg",
  },
  {
    srcUrl: "./assets/images/media/4.jpg",
    previewUrl: "./assets/images/media/4.jpg"
  },
  {
    srcUrl: './assets/images/media/5.jpg',
    previewUrl: './assets/images/media/5.jpg',
  },
  {
    srcUrl: './assets/images/media/6.jpg',
    previewUrl: './assets/images/media/6.jpg',
  },

];
const data1 = [
  {
    srcUrl: "./assets/images/media/7.jpg",
    previewUrl: "./assets/images/media/7.jpg",
  },
  {
    srcUrl: "./assets/images/media/8.jpg",
    previewUrl: "./assets/images/media/8.jpg",
  },
  {
    srcUrl: "./assets/images/media/9.jpg",
    previewUrl: "./assets/images/media/9.jpg",
  },
  {
    srcUrl: "./assets/images/media/10.jpg",
    previewUrl: "./assets/images/media/10.jpg"
  },
  {
    srcUrl: './assets/images/media/11.jpg',
    previewUrl: './assets/images/media/11.jpg',
  },
  {
    srcUrl: './assets/images/media/12.jpg',
    previewUrl: './assets/images/media/12.jpg',
  },

];
const data2 = [
  {
    srcUrl: "./assets/images/media/1.jpg",
    previewUrl: "./assets/images/media/1.jpg",
  },
  {
    srcUrl: "./assets/images/media/2.jpg",
    previewUrl: "./assets/images/media/2.jpg",
  },
  {
    srcUrl: "./assets/images/media/3.jpg",
    previewUrl: "./assets/images/media/3.jpg",
  },
  {
    srcUrl: "./assets/images/media/4.jpg",
    previewUrl: "./assets/images/media/4.jpg"
  },
  {
    srcUrl: './assets/images/media/5.jpg',
    previewUrl: './assets/images/media/5.jpg',
  },
  {
    srcUrl: './assets/images/media/6.jpg',
    previewUrl: './assets/images/media/6.jpg',
  },

];
const data3 = [
  {
    srcUrl: "./assets/images/media/1.jpg",
    previewUrl: "./assets/images/media/1.jpg",
  },
  {
    srcUrl: "./assets/images/media/1.jpg",
    previewUrl: "./assets/images/media/1.jpg",
  },
  {
    srcUrl: "./assets/images/media/1.jpg",
    previewUrl: "./assets/images/media/1.jpg",
  },
  {
    srcUrl: "./assets/images/media/1.jpg",
    previewUrl: "./assets/images/media/1.jpg"
  },
  {
    srcUrl: './assets/images/media/1.jpg',
    previewUrl: './assets/images/media/1.jpg',
  },
  {
    srcUrl: './assets/images/media/1.jpg',
    previewUrl: './assets/images/media/1.jpg',
  },

];
const data4 = [
  {
    srcUrl: "./assets/images/media/1.jpg",
    previewUrl: "./assets/images/media/1.jpg",
  },
  {
    srcUrl: "./assets/images/media/2.jpg",
    previewUrl: "./assets/images/media/2.jpg",
  },
  {
    srcUrl: "./assets/images/media/3.jpg",
    previewUrl: "./assets/images/media/3.jpg",
  },
  {
    srcUrl: "./assets/images/media/4.jpg",
    previewUrl: "./assets/images/media/4.jpg"
  },


];
const data5 = [
  {
    srcUrl: "./assets/images/media/1.jpg",
    previewUrl: "./assets/images/media/1.jpg",
  },
  {
    srcUrl: "./assets/images/media/2.jpg",
    previewUrl: "./assets/images/media/2.jpg",
  },
  {
    srcUrl: "./assets/images/media/3.jpg",
    previewUrl: "./assets/images/media/3.jpg",
  },
  {
    srcUrl: "./assets/images/media/4.jpg",
    previewUrl: "./assets/images/media/4.jpg"
  },


];