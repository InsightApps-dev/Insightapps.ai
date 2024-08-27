import { DOCUMENT } from '@angular/common';
import { Component, Inject, Renderer2 } from '@angular/core';

@Component({
  selector: 'app-landingpage-layout',
  templateUrl: './landingpage-layout.component.html',
  styleUrls: ['./landingpage-layout.component.scss']
})
export class LandingpageLayoutComponent {
  
  constructor( @Inject(DOCUMENT) private document: Document,private renderer:Renderer2) {
   
 }
 ngOnInit(): void {
  this.renderer.addClass(this.document.body, 'landing-page');
  this.renderer.addClass(this.document.body, 'ltr');
  this.renderer.removeClass(this.document.body, 'sidebar-mini');
 }
 ngOnDestroy(): void  {
  this.renderer.removeClass(this.document.body, 'landing-page');
  this.renderer.removeClass(this.document.body, 'ltr');
  this.renderer.addClass(this.document.body, 'sidebar-mini');
 }
}
