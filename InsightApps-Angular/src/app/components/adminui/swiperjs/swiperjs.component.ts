import { Component, ElementRef, ViewChild } from '@angular/core';
import KeenSlider, { KeenSliderInstance, KeenSliderPlugin } from 'keen-slider';
import { SwiperModule } from 'swiper/angular';

import SwiperCore, {
  Navigation,
  Pagination,
  Scrollbar,
  A11y,
  Virtual,
  Zoom,
  Autoplay,
  Thumbs,
  Mousewheel,
  Keyboard,
  EffectCube,
  EffectFade,
  EffectFlip,
  EffectCoverflow,
} from 'swiper';
import { SharedModule } from '../../../shared/sharedmodule';

SwiperCore.use([
  Navigation,
  Pagination,
  Scrollbar,
  A11y,
  Virtual,
  Mousewheel,
  Zoom,
  Autoplay,
  Thumbs,
  Keyboard,
  EffectCube,
  EffectFade,
  EffectFlip,
  EffectCoverflow,
]);
@Component({
  selector: 'app-swiperjs',
  standalone: true,
  imports: [SharedModule,SwiperModule],
  templateUrl: './swiperjs.component.html',
  styleUrls: ['./swiperjs.component.scss']
})
export class SwiperjsComponent {
  indexNumber = 1;
  thumbsSwiper: any;

  setThumbsSwiper(swiper: any) {
    this.thumbsSwiper = swiper;
  }

  swiperOptions = {
    slidesPerView: 1,
    autoplay: {
      delay: 3000,
    },
    // other options...
  };

  @ViewChild('sliderRef') sliderRef!: ElementRef<HTMLElement>;
  opacities: number[] = [];
  slider!: KeenSliderInstance;

  public currentSlide = 1;

  ngAfterViewInit() {
    setTimeout(() => {
      if (this.sliderRef && this.sliderRef.nativeElement) {
        this.slider = new KeenSlider(this.sliderRef.nativeElement, {
          slides: this.imageData.length,
          loop: true,
          defaultAnimation: {
            duration: 3000,
          },
          detailsChanged: (s) => {
            this.opacities = s.track.details.slides.map(
              (slide: { portion: any; }) => slide.portion
            );
          },
        });
      }
    });

    if (this.sliderRef && this.sliderRef.nativeElement) {
      this.slider = new KeenSlider(this.sliderRef.nativeElement);
    }
  }

  ngOnDestroy() {
    if (this.slider) this.slider.destroy();
  }

  imageData = [
    {
      src: './assets/images/media/media-12.jpg',
    },
    {
      src: './assets/images/media/media-8.jpg',
    },
    {
      src: './assets/images/media/media-28.jpg',
    },
    {
      src: './assets/images/media/media-31.jpg',
    },
  ];
  imageData1 = [
    {
      src: './assets/images/media/files/04.jpg',
    },
    {
      src: './assets/images/media/files/05.jpg',
    },
    {
      src: './assets/images/media/files/06.jpg',
    },
  ];
  imageData2 = [
    {
      src: './assets/images/media/11.jpg',
    },
    {
      src: './assets/images/media/12.jpg',
    },
    {
      src: './assets/images/media/13.jpg',
    },
  ];
  imageData3 = [
    {
      src: './assets/images/media/14.jpg',
    },
    {
      src: './assets/images/media/15.jpg',
    },
    {
      src: './assets/images/media/16.jpg',
    },
  ];
  imageData4 = [
    {
      src: './assets/images/media/17.jpg',
    },
    {
      src: './assets/images/media/18.jpg',
    },
    {
      src: './assets/images/media/19.jpg',
    },

  ];
  imageData5 = [
    {
      src: './assets/images/media/27.jpg',
    },
    {
      src: './assets/images/media/28.jpg',
    },
    {
      src: './assets/images/media/29.jpg',
    },
   
  ];
  imageData6 = [
    {
      src: './assets/images/media/34.jpg',
    },
    {
      src: './assets/images/media/35.jpg',
    },
    {
      src: './assets/images/media/36.jpg',
    },
 
  ];
  imageData7 = [
    {
      src:"./assets/images/media/files/01.jpg",
    },
    {
      src: "./assets/images/media/files/02.jpg",
    },
    {
      src:"./assets/images/media/files/03.jpg",
    },
 
  ];
  imageData8 = [
    {
      src: "./assets/images/media/files/04.jpg",
    },
    {
      src: "./assets/images/media/files/05.jpg",
    },
    {
      src: "./assets/images/media/files/06.jpg",
    },
   
  ];
  imageData9 = [
    {
      src: "./assets/images/media/16.jpg",
    },
    {
      src: "./assets/images/media/17.jpg",
    },
    {
      src: "./assets/images/media/18.jpg",
    },
   
  ];
  imageData10 = [
    {
      src: "./assets/images/media/11.jpg",
    },
    {
      src: "./assets/images/media/12.jpg",
    },
    {
      src: "./assets/images/media/13.jpg",
    },
   
  ];
}

