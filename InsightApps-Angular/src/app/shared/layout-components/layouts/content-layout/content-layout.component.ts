import { Component, ElementRef, HostListener, Renderer2 } from '@angular/core';
import { Menu, NavService } from '../../../services/navservice';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs';

@Component({
  selector: 'app-content-layout',
  templateUrl: './content-layout.component.html',
  styleUrls: ['./content-layout.component.scss']
})
export class ContentLayoutComponent {

 public menuItems!: Menu[];
  currentRoute:  string | undefined;
  urlData:  string[] | undefined;
 constructor(
  private router:Router, 
   public navServices: NavService,
   private elementRef: ElementRef,
   private renderer: Renderer2,
 ) {
  this.router.events.pipe(
    filter(event => event instanceof NavigationEnd)
  ).subscribe(() => {
    window.scrollTo(0, 0);
  });
  document.body.classList.remove( 'landing-page','ltr');
  document.body.classList.add('sidebar-mini');
  document.body.classList.add('app');

   this.navServices.items.subscribe((menuItems: any) => {
     this.menuItems = menuItems;
   });
  
 }
 togglesidemenuBody() {
  document.querySelector('.offcanvas-end')?.classList.remove('show')
  document.querySelector("body")!.classList.remove("overflow:hidden");
  document.querySelector("body")!.classList.remove("padding-right:4px");


  if(localStorage.getItem('insightappsverticalstyles') == 'icontext'){
    document.documentElement.removeAttribute('icon-text');
  }
  if (document.documentElement.getAttribute('data-nav-layout') == 'horizontal' && window.innerWidth > 992) {
    this.closeMenu();
  }
  let html = this.elementRef.nativeElement.ownerDocument.documentElement;
  if (window.innerWidth <= 992) {
    html?.setAttribute(
      'data-toggled',
      html?.getAttribute('data-toggled') == 'close' ? 'close' : 'close'
    );
  }
  document
  .querySelector('.header-search')
  ?.classList.remove('searchdrop');
}

closeMenu() {
  this.menuItems?.forEach((a: any) => {
    if (this.menuItems) {
      a.active = false;
    }
    a?.children?.forEach((b: any) => {
      if (a.children) {
        b.active = false;
      }
    });
  });
}
clearToggle() {
  let html = this.elementRef.nativeElement.ownerDocument.documentElement;
  html?.setAttribute('data-toggled', 'open');
 
  document.querySelector('#responsive-overlay')?.classList.remove('active');
}

}
