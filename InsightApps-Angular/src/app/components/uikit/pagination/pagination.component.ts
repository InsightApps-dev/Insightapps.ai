import { Component } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule, NgbPaginationModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-pagination',
  standalone: true,
  imports: [SharedModule,NgbPaginationModule],
  templateUrl: './pagination.component.html',
  styleUrls: ['./pagination.component.scss']
})
export class PaginationComponent {
	page = 2;
  page2 = 2;
  page1 = 3;
  page4 = 4;
  page5 = 4;
  page6 = 4;
  page7 = 4;
  page8 = 4;
  page9 = 4;
  page10 = 3;
  page11=3;
  page12=3;
  page13=3;
  page14=3;
  page15=3;
	getPageSymbol(current: number) {
		return ['1', '2'][current - 1];
	}
  getPageSymbol1(current: number) {
		return ['1', '2','3'][current - 1];
	}
  getPageSymbol2(current: number) {
		return ['', '',''][current - 1];
	}
}
