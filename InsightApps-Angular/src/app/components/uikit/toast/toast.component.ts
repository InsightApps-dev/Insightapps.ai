import { Component, ElementRef, ViewChild } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { ToastrModule, ToastrService } from 'ngx-toastr';
import { ToastService } from './toast.service';

@Component({
  selector: 'app-toast',
  standalone: true,
  imports: [SharedModule,NgbModule,ToastrModule],
  providers: [ToastrService],
  templateUrl: './toast.component.html',
  styleUrls: ['./toast.component.scss']
})
export class ToastComponent {
  show = true;
  show1 = true;
  show2 = true;
  show3 = true;
  show4 = true;
  show9 = true;
  show10=true;
  show11=true;
  show12=true;
  show13=true;
  show14=true;
  show15=true;
  show16=true;
  show17=true;
  show18=true;

  toasts: { autohide: boolean }[] = [];
  @ViewChild('toastContainer') toastContainer!: ElementRef;

  show0 = false;
  autohide = true;

  constructor(
    public toastService: ToastService,
    private toastr: ToastrService
  ) {}
  right:any;
  showToast() {
    const newToast = { autohide: true };
    this.toasts.push(newToast);
  }

  hideToast(toast: { autohide: boolean }) {
    this.toasts = this.toasts.filter((t) => t !== toast);
  }
    //Top Placements
    TopLeft() {
      this.toastr.success('Your,toast message here.', 'Bootstrap', {
        timeOut: 3000,
        positionClass: 'toast-top-left',
      });
    }
    TopRight() {
      this.toastr.success('Your,toast message here.', 'Bootstrap', {
        timeOut: 3000,
        positionClass: 'toast-top-right',
      });
    }
    TopCenter() {
      this.toastr.error(`'Your,toast message here.'`, 'Bootstrap', {
        timeOut: 3000,
        positionClass: 'toast-top-center',
      });
    }
    MiddleLeft() {
      this.toastr.success('Your,toast message here.', 'Bootstrap', {
        timeOut: 3000,
        positionClass: 'toast-bottom-center',
      });
    }
    MiddleCenter() {
      this.toastr.success('Your,toast message here.', 'Bootstrap', {
        timeOut: 3000,
        positionClass: 'toast-bottom-center',
      });
    }
    MiddleRight() {
      this.toastr.success('Your,toast message here.', 'Bootstrap', {
        timeOut: 3000,
        positionClass: 'toast-middle-right',
      });
    }
    BottomLeft() {
      this.toastr.info('Your,toast message here.', 'Bootstrap', {
        timeOut: 3000,
        positionClass: 'toast-bottom-left',
      });
    }
    BottomCenter() {
      this.toastr.success('Your,toast message here.', 'Bootstrap', {
        timeOut: 3000,
        positionClass: 'toast-bottom-center',
      });
    }
    BottomRight() {
      this.toastr.error('Your,toast message here.', 'Bootstrap', {
        timeOut: 3000,
        positionClass: 'toast-bottom-right',
      });
    }

toggleclass = "fade hide";
TopWidth() {
  if (this.toggleclass === "fade hide") {
    this.toggleclass = "fade show";
  } else {
    this.toggleclass = "fade hide";
  }
}
toggleclass1 = "fade hide";
BottomWidth() {
  if (this.toggleclass1 === "fade hide") {
    this.toggleclass1 = "fade show";
  } else {
    this.toggleclass1 = "fade hide";
  }
}
toggleclass2 = "fade hide";
MiddleWidth() {
  if (this.toggleclass2 === "fade hide") {
    this.toggleclass2 = "fade show";
  } else {
    this.toggleclass2 = "fade hide";
  }
}
}
