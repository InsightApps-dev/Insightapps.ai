import { Component } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-accordions',
  standalone: true,
  imports: [SharedModule,NgbModule],
  templateUrl: './accordions.component.html',
  styleUrls: ['./accordions.component.scss']
})
export class AccordionsComponent {
  panels = ['Accordion Item #1','Accordion Item #2','Accordion Item #3'];
  panelscheckbox=['Accordion Item #1','Accordion Item #2','Accordion Item #3', 'Accordion Item #4']
  defaults = ['Collapse Group Item #1','Collapse Group Item #2','Collapse Group Item #3'];
 accordions=[
  { name:'Accordion Item #1',icon:"fe fe-grid me-1" },
  { name:'Accordion Item #2',icon:"fe fe-edit me-1" },
  { name:'Accordion Item #3',icon:"fe fe-headphones me-1" },
  { name:'Accordion Item #4',icon:"fe fe-database me-1" },
 ]
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
