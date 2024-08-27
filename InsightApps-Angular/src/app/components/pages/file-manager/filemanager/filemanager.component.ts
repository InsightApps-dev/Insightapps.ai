import { Component } from '@angular/core';
import { NgbModal, NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { SharedModule } from '../../../../shared/sharedmodule';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-filemanager',
  standalone: true,
  imports: [SharedModule,NgbModule,RouterModule],
  templateUrl: './filemanager.component.html',
  styleUrls: ['./filemanager.component.scss']
})
export class FilemanagerComponent {
  constructor( private modalService: NgbModal) {
  }

  File(content:any){
    this.modalService.open(content);
  }
}
