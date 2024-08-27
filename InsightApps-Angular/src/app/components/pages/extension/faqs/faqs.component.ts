import { Component } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { SharedModule } from '../../../../shared/sharedmodule';

@Component({
  selector: 'app-faqs',
  standalone: true,
  imports: [SharedModule,NgbModule],
  templateUrl: './faqs.component.html',
  styleUrls: ['./faqs.component.scss']
})
export class FaqsComponent {
  panels = ['How To Insert All The Plugins?', 'How Can I Contact?', 'Can I use this Plugins in Another Template','It is Easy to Customizeable?','How can i download this Template?','How can I add another Page in Template'];
  isCollapsed: any = true;
  isCollapsed1: boolean = true;
  isCollapsed2: boolean = true;
  isHorizontalCollapsed: boolean = true;
  constructor() {}

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

  ngOnInit(): void {}

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
}
