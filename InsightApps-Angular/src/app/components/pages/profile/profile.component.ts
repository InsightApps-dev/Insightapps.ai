import { Component } from '@angular/core';
import {
  Image,
  ModalGalleryService,
   ModalGalleryRef,
 
 } from '@ks89/angular-modal-gallery';
import { DomSanitizer } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Gallery, GalleryItem, GalleryModule, ImageItem } from 'ng-gallery';
import { LightboxModule } from 'ng-gallery/lightbox';

import { NgbModule ,NgbModal} from '@ng-bootstrap/ng-bootstrap';
import { SharedModule } from '../../../shared/sharedmodule';
import { PagesService } from '../pages.service';
@Component({
  selector: 'app-profile',
  standalone:true,
  imports: [SharedModule, NgbModule, GalleryModule,LightboxModule,FormsModule],
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent {
  url1:string = '';
  handleFileInput(event: any): void {
    const file = event.target.files[0];
    if (file) { 
      const reader = new FileReader();
      reader.onload = (e: any) => {
        this.url1 = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  }
  active!:1;
  items!: GalleryItem[];

  imageData = data;

  constructor(public gallery: Gallery,private modalService: NgbModal,private pageService: PagesService) {}

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
  {
    class:"col-xs-6 col-sm-4 col-md-4 col-xl-3 mb-4 border-bottom-0",
    srcUrl: "./assets/images/media/12.jpg",
    previewUrl: "./assets/images/media/12.jpg",
  },
  {
    class:"col-xs-6 col-sm-4 col-md-4 col-xl-3 mb-4 border-bottom-0",
    srcUrl: "./assets/images/media/13.jpg",
    previewUrl: "./assets/images/media/13.jpg",
  },
  {
    class:"col-xs-6 col-sm-4 col-md-4 col-xl-3 mb-4 border-bottom-0",
    srcUrl: "./assets/images/media/14.jpg",
    previewUrl: "./assets/images/media/14.jpg",
  },
  {
    class:"col-xs-6 col-sm-4 col-md-4 col-xl-3 mb-4 border-bottom-0",
    srcUrl: "./assets/images/media/15.jpg",
    previewUrl: "./assets/images/media/15.jpg",
  },
];
