import { Component } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import Swal, { SweetAlertResult } from 'sweetalert2';

// declare var require:any
// const Swal = require('sweetalert2');
@Component({
  selector: 'app-notifications',
  standalone: true,
  imports: [SharedModule,NgbModule],
  templateUrl: './notifications.component.html',
  styleUrls: ['./notifications.component.scss']
})
export class NotificationsComponent {

 
  constructor(private toastr: ToastrService) {
  
   }

  ngOnInit(): void {
  }
  showDefault() {
    this.toastr.info('This is an example of tip', 'TIP', {
      timeOut: 1500,
      positionClass: 'toast-bottom-right',
      
     
    });
  }
  showSuccess() {
    this.toastr.success('This is an example of tip', 'TIP', {
      timeOut: 3000,
      positionClass: 'toast-bottom-right',
    });
  }
  
  showError() {
    this.toastr.error('This is an example of tip', 'TIP', {
      timeOut: 2000,
      positionClass: 'toast-top-right',
    });
  }

  showInfo() {
    this.toastr.info('This is an example of tip', 'TIP', {
      timeOut: 1500,
      positionClass: 'toast-bottom-right',
    });
  }

  ShowWarning() {
    this.toastr.warning('This is an example of tip', 'TIP', {
      timeOut: 1500,
      positionClass: 'toast-top-left',
    });
  }

  Notification() {
    this.toastr.info('This is an example of tip', 'TIP', {
      timeOut: 1500,
      positionClass: 'toast-top-center',
    });
  }
  Info() {
    Swal.fire({
      icon: 'info',
      title: 'Confirmation Required',
      text: 'Are You sure want to reset password',
      confirmButtonColor: '#40871d',
      cancelButtonColor: '#1c76a6',
      showCancelButton: true,
      confirmButtonText: 'Ok',
      cancelButtonText: 'Cancel',
    });
  }
}
