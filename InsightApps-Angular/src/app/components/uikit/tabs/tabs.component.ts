import { Component, HostListener } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-tabs',
  standalone: true,
  imports: [SharedModule,NgbModule],
  templateUrl: './tabs.component.html',
  styleUrl: './tabs.component.scss'
})
export class TabsComponent {
  ngAfterViewInit() {
    const plusButtons = document.querySelectorAll('.counter-plus');
    const minusButtons = document.querySelectorAll('.counter-minus');
  
    function perfectChart() {
      plusButtons.forEach((plusButton: any) => {
        plusButton.addEventListener('click', () => {
          const parentDiv = plusButton.closest('.handle-counter');
          const quantityInput = parentDiv.querySelector('.qty');
  
          if (quantityInput) {
            quantityInput.value = String(Number(quantityInput.value) + 1);
          }
        });
      });
  
      minusButtons.forEach((minusButton: any) => {
        minusButton.addEventListener('click', () => {
          const parentDiv = minusButton.closest('.handle-counter');
          const quantityInput = parentDiv.querySelector('.qty');
  
          if (quantityInput && quantityInput.value > 0) {
            quantityInput.value = String(Number(quantityInput.value) - 1);
          }
        });
      });
    }
  
    perfectChart();
  }
  public isClosed1 = false;
  Closetoggle(item: any) {
   
    if (item == 'one') {
      this.isClosed1 = true;
    }
  }
  scroll(el: HTMLElement) {
    el.scrollIntoView({ behavior: 'smooth' });
  }

  scrolled: boolean | unknown = false;

  @HostListener('window:scroll', [])
  onWindowScroll() {
    this.scrolled = window.scrollY > 10;

  }
}
