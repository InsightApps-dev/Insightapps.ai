import { Component, ElementRef, HostListener, Inject, Renderer2, ViewChild } from '@angular/core';
import { LayoutConfigService } from '../../../shared/services/layout-config.service';
import { CommonModule, DOCUMENT, ViewportScroller } from '@angular/common';
import { CarouselModule, OwlOptions, SlidesOutputData } from 'ngx-owl-carousel-o';
import { fromEvent } from 'rxjs';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { SwiperModule } from 'swiper/angular';

@Component({
  selector: 'app-landingpage',
  standalone:true,
  imports:[NgbModule,CarouselModule,CommonModule,FormsModule,ReactiveFormsModule,RouterModule,SwiperModule],
  templateUrl: './landingpage.component.html',
  styleUrls: ['./landingpage.component.scss']
})
export class LandingpageComponent {
  constructor(
    @Inject(DOCUMENT) private document: Document,
    private el: ElementRef,
    private elementRef: ElementRef,
    private viewScroller: ViewportScroller,
    public renderer: Renderer2
  ) {
    const htmlElement =
      this.elementRef.nativeElement.ownerDocument.documentElement;
    const bodyElement = document.body;
    this.renderer.setAttribute(htmlElement, 'data-toggled', 'close');
    // this.renderer.setAttribute(htmlElement, 'data-theme-mode', 'light');
    this.renderer.removeClass(bodyElement, 'sidebar-mini');
    this.renderer.setAttribute(htmlElement, 'data-nav-layout', 'horizontal');
    this.renderer.setAttribute(htmlElement, 'data-nav-style', 'menu-click');
    this.renderer.removeAttribute(htmlElement, 'data-width');
        this.renderer.setAttribute(htmlElement, 'data-menu-styles', 'light');
        this.renderer.removeAttribute(htmlElement, 'loader');
        this.renderer.removeAttribute(htmlElement, 'data-width');
        this.renderer.removeAttribute(htmlElement, 'data-bg-img');
        this.renderer.removeAttribute(htmlElement, 'data-vertical-style');
    
        this.renderer.removeAttribute(htmlElement, 'data-nav-style', 'icon-click');
  }
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
  Swicher(){
    document.querySelector('.offcanvas-end')?.classList.add('show')
  }

  scroll(el: HTMLElement) {
    el.scrollIntoView({ behavior: 'smooth' });
  }

  scrolled: boolean = false;

  @HostListener('window:scroll', [])
  onWindowScroll() {
    this.scrolled = window.scrollY > 10;
    const sections = this.el.nativeElement.querySelectorAll('.side-menu__item');
    const scrollPos =
      window.scrollY ||
      this.elementRef.nativeElement.ownerDocument.documentElement.scrollTop ||
      document.body.scrollTop;
    sections.forEach((el: any, i: string | number) => {
      const currLink = sections[i];
      const val: any = currLink.getAttribute('value');
      const refElement: any = this.el.nativeElement.querySelector('#' + val);
  
      if (refElement !== null) {
        const scrollTopMinus = scrollPos + 73;
        if (
          refElement.offsetTop <= scrollTopMinus &&
          refElement.offsetTop + refElement.offsetHeight > scrollTopMinus
        ) {
          const activeNav =
            this.el.nativeElement.querySelector('.nav-scroll.active');
          if (activeNav) {
            this.renderer.removeClass(activeNav, 'active');
          }
          this.renderer.addClass(currLink, 'active');
        } else {
          this.renderer.removeClass(currLink, 'active');
        }
      }
    });
  }
  expande = false;
  expande1 = false;
  expande2 = false;

  // @ViewChild('dropmenu', { static: true }) dropmenu!: ElementRef;

  toggleExpand(): void {
    this.expande = !this.expande;
    if (localStorage.getItem('data-menu-styles') == 'light') {
      document.querySelector('html')?.setAttribute('data-menu-styles', 'light');
    } else if (localStorage.getItem('data-menu-styles') == 'light') {
      document.querySelector('html')?.setAttribute('data-menu-styles', 'light');
    }
  }
  panels = ['How To Insert All The Plugins?', 'How Can I Contact?', 'Can I use this Plugins in Another Template','It is Easy to Customizeable?','How can i download this Template?','How can I add another Page in Template'];
  isCollapsed: any = true;
  isCollapsed1: boolean = true;
  isCollapsed2: boolean = true;
  isHorizontalCollapsed: boolean = true;

  toggleCollapse(id: string) {
    if (this.isCollapsed[id] === undefined) {
      this.isCollapsed[id] = true;
    } else {
      this.isCollapsed[id] = !this.isCollapsed[id];
    }
  }
  
  toggleHorizontalCollapse() {
    this.isHorizontalCollapsed = !this.isHorizontalCollapsed;
  }



  public isFirstGradient = false;
  public isSecondGradient = false;

  FirstGradient() {
    this.isFirstGradient = !this.isFirstGradient;
    if (this.isFirstGradient == true) {
      document.querySelector('.firstgradient')?.classList.remove('collapsed');
    } else {
      document.querySelector('.firstgradient')?.classList.add('collapsed');
    }
  }
  SecondGradient() {
    this.isSecondGradient = !this.isSecondGradient;
    if (this.isSecondGradient == true) {
      document.querySelector('.secondgradient')?.classList.remove('collapsed');
    } else {
      document.querySelector('.secondgradient')?.classList.add('collapsed');
    }
  }
  customOptions: OwlOptions = {
    loop: true,
    mouseDrag: true,
    touchDrag: true,
    pullDrag: false,
    margin:30,
    dots: true,
    navSpeed: 700,
    autoplay: true,
    navText: ['<', '>'],
    responsive: {
      0: {
        items: 1, // 1 item visible for screen width less than 400 pixels
      },
      400: {
        items: 1, // 1 item visible for screen width 400 pixels or more
      },
      740: {
        items: 1, // 2 items visible for screen width 740 pixels or more
      },
      1000: {
        items: 3, // 2 items visible for screen width 1000 pixels or more
      },
    },
    nav: false,
  };
  
  activeSlides!: SlidesOutputData;
  
  slidesStore: any[] = [
    {
      img:"./assets/images/users/12.jpg",
      name:'Sophiee carr',
      role:'Web Developer',
    },
    {
      img:"./assets/images/users/1.jpg",
      name:'Ralph Alice',
      role:'Web Developer',
    },
    {
      img:"./assets/images/users/16.jpg",
      name:'Lois Lane',
      role:'Web Developer',
    },
    {
      img:"./assets/images/users/14.jpg",
      name:'Kramden',
      role:'Web Developer',
    },
    {
      img:"./assets/images/users/14.jpg",
      name:'Ralph Alice',
      role:'Web Developer',
    },
    {
      img:"./assets/images/users/14.jpg",
      name:'Ralph Alice',
      role:'Web Developer',
    },
   
  ];
  ngOnInit(): void {
    this.menuResizeFn()
    this.renderer.addClass(this.document.body, 'landing-body');
    // switcher.localStorageBackUp();
 
    const ltr = this.elementRef.nativeElement.querySelectorAll('#switcher-ltr');
    const rtl = this.elementRef.nativeElement.querySelectorAll('#switcher-rtl');

    fromEvent(ltr, 'click').subscribe(() => {
      this.customOptions = { ...this.customOptions, rtl: false };
    });

    fromEvent(rtl, 'click').subscribe(() => {
      this.customOptions = { ...this.customOptions, rtl: true, autoplay: true };
    });

  }
  isChecked: boolean = true; // Default to Monthly

  toggleTabs(event: any): void {
    this.isChecked = event.target.checked;

  }
  toggleSidebar() {
    const htmlElement =
      this.elementRef.nativeElement.ownerDocument.documentElement;
    const currentToggleValue = htmlElement.getAttribute('data-toggled');
  
    if (currentToggleValue !== 'open') {
      this.renderer.setAttribute(htmlElement, 'data-toggled', 'open');
    } else {
      this.renderer.setAttribute(htmlElement, 'data-toggled', 'close');
    }
  }
  bodyclick() {
    this.expande1 = false;
    this.expande2 = false;
    this.expande = false; 
    const htmlElement =
      this.elementRef.nativeElement.ownerDocument.documentElement;
    this.renderer.setAttribute(htmlElement, 'data-toggled', 'close');
    document.querySelector('.offcanvas-end')?.classList.remove('show')
  }
  screenWidth!: number;
  eventTriggered: boolean = false;
  @HostListener('window:resize', ['$event'])
  onResize(event: any): void {
   this.menuResizeFn();
 
    this.screenWidth = window.innerWidth;
 
    // Check if the event hasn't been triggered and the screen width is less than or equal to your breakpoint
    if (!this.eventTriggered && this.screenWidth <= 992) {
      document.documentElement?.setAttribute('data-toggled', 'close')
 
      
      // Trigger your event or perform any action here
      this.eventTriggered = true; // Set the flag to true to prevent further triggering
    } else if (this.screenWidth > 992) {
      // Reset the flag when the screen width goes beyond the breakpoint
      this.eventTriggered = false;
    }
  }
  // Close Nav menu
  WindowPreSize: number[] = [window.innerWidth];
  menuResizeFn(): void {
   this.WindowPreSize.push(window.innerWidth);
 
   if (this.WindowPreSize.length > 2) {
     this.WindowPreSize.shift();
   }
 
   if (this.WindowPreSize.length > 1) {
     const html = document.documentElement;
 
     if (this.WindowPreSize[this.WindowPreSize.length - 1] < 992 && this.WindowPreSize[this.WindowPreSize.length - 2] >= 992) {
       // less than 992
       html.setAttribute('data-toggled', 'close');
     }
 
     if (this.WindowPreSize[this.WindowPreSize.length - 1] >= 992 && this.WindowPreSize[this.WindowPreSize.length - 2] < 992) {
       // greater than 992
       html.removeAttribute('data-toggled');
       document.querySelector('#responsive-overlay')?.classList.remove('active');
 
     }
   }
 }
}
