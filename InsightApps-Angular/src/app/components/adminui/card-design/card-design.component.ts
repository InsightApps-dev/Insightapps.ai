import { Component, HostListener } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-card-design',
  standalone: true,
  imports: [SharedModule,NgbModule,FormsModule,ReactiveFormsModule],
  templateUrl: './card-design.component.html',
  styleUrls: ['./card-design.component.scss']
})

export class CardDesignComponent {

  scroll(el: HTMLElement) {
    el.scrollIntoView({ behavior: 'smooth' });
  }

  scrolled: boolean | unknown = false;

  @HostListener('window:scroll', [])
  onWindowScroll() {
    this.scrolled = window.scrollY > 10;

  }
  public isCollapsed1 = false;
  public isClosed1 = false;
  public isClosed2 = false;
  public isCollapsed2 = true;
  public isClosed3 = false;
  public isCollapsed3 = false;
  public isClosed4 = false;
  public isCollapsed4 = false;
  public isClosed5 = false;
  public isCollapsed5 = false;
  public isClosed6 = false;
  public isCollapsed6 = false;
  Collapsetoggle1() {
    this.isCollapsed1 = !this.isCollapsed1;
  }
  Closetoggle1() {
    this.isClosed1 = true
  }
  Collapsetoggle2() {
    this.isCollapsed2 = !this.isCollapsed2;
  }
  Closetoggle2() {
    this.isClosed2 = true
  }
  Collapsetoggle3() {
    this.isCollapsed3 = !this.isCollapsed3;
  }
  Closetoggle3() {
    this.isClosed3 = true
  }
  Collapsetoggle4() {
    this.isCollapsed4 = !this.isCollapsed4;
  }
  Closetoggle4() {
    this.isClosed4 = true
  }
  Collapsetoggle5() {
    this.isCollapsed5 = !this.isCollapsed5;
  }
  Closetoggle5() {
    this.isClosed5 = true
  }
  Collapsetoggle6() {
    this.isCollapsed6 = !this.isCollapsed6;
  }
  Closetoggle6() {
    this.isClosed6 = true
  }
  toggleClass = "fe fe-maximize";
  public fullScreen: boolean = false;

  fullScreenToggle() {
    document
    .querySelector('.fullscreentoggle')
    ?.classList.toggle('card-fullscreen');

    if (this.toggleClass === "fe fe-maximize") {
      this.toggleClass = "fe fe-minimize";
    } else {
      this.toggleClass = "fe fe-maximize";
    }
  }
  active=1;
  active1=4;

}
