import { Component, Renderer2 } from '@angular/core';
import { NgbModal, NgbModalOptions, NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { SharedModule } from '../../../shared/sharedmodule';
import { SimplebarAngularModule } from 'simplebar-angular';

@Component({
  selector: 'app-modal',
  standalone: true,
  imports: [SharedModule,NgbModule,SimplebarAngularModule],
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.scss']
})
export class ModalComponent {
scale: any;
  constructor(private modalService: NgbModal, private renderer: Renderer2) {}
  openScale(modal: any) {
    this.modalService.open(modal, {
      centered: true,
      windowClass: 'animate__animated animate__zoomIn',
    });
  }
  openSlideRight(content: any) {
    this.modalService.open(content, {
      centered: true,
      windowClass: 'animate__animated animate__slideInRight',
    });
  }

  openSlideBottom(modal: any) {
    this.modalService.open(modal, {
      centered: true,
      windowClass: 'animate__animated animate__backInUp',
    });
  }
  openNewspaper(modal: any) {
    this.modalService.open(modal, {
      centered: true,
      windowClass: 'animate__animated animate__rotateIn',
    });
  }
  openFall(modal: any) {
    this.modalService.open(modal, {
      centered: true,
      windowClass: 'animate__animated animate__zoomIn',
    });
  }
  openFlipHorizontal(modal: any) {
    this.modalService.open(modal, {
      centered: true,
      windowClass: 'animate__animated animate__flip',
    });
  }
  openFlipVertical(modal: any) {
    this.modalService.open(modal, {
      centered: true,
      windowClass: 'animate__animated animate__flipInX',
    });
  }
  openSuperScaled(modal: any) {
    this.modalService.open(modal, {
      centered: true,
      windowClass: 'animate__animated animate__zoomIn',
    });
  }
  openSign(modal: any) {
    this.modalService.open(modal, {
      centered: true,
      windowClass: 'animate__animated animate__flipInX',
    });
  }
  openRotateBottom(modal: any) {
    this.modalService.open(modal, {
      centered: true,
      windowClass: 'animate__animated animate__slideInUp',
    });
  }
  openRotateLeft(modal: any) {
    this.modalService.open(modal, {
      centered: true,
      windowClass: 'animate__animated animate__slideInLeft',
    });
  }

  openJustMe(justme: any) {
    this.modalService.open(justme, {
      centered: true,
      windowClass: 'dark-modal',
    });
  }

  openright(right: any) {
    this.modalService.open(right, { centered: true });
  }

  openBasic(basicModal: any) {
    this.modalService.open(basicModal);
  }

  StaticBackdrop(staticbackdropModal: any) {
    this.modalService.open(staticbackdropModal);
  }

  VerticalCenter(VerticalCenterModal: any) {
    this.modalService.open(VerticalCenterModal, { centered: true });
  }

  GridOpen(gridModal: any) {
    this.modalService.open(gridModal, { size: 'lg' });
  }
  Openmdo(OpenmdoModal: any) {
    this.modalService.open(OpenmdoModal);
  }
  Openfat(OpenfatModal: any) {
    this.modalService.open(OpenfatModal);
  }
  Opengetbootstrap(OpengetbootstrapModal: any) {
    this.modalService.open(OpengetbootstrapModal);
  }
  openSmall(SmallModal: any) {
    this.modalService.open(SmallModal, { size: 'sm' });
  }
  openLarge(LargeModal: any) {
    this.modalService.open(LargeModal, { size: 'lg' });
  }
  openextraLarge(extraLargeModal: any) {
    this.modalService.open(extraLargeModal, { size: 'xl' });
  }
  openScrolling(ScrollingcontentModal: any) {
    this.modalService.open(ScrollingcontentModal, { scrollable: true });
  }
  openFullscreen(FullscreenModal: any) {
    this.modalService.open(FullscreenModal, { fullscreen: true });
  }
  Openmodal(OpenmdoModal: any) {
    this.modalService.open(OpenmdoModal);
  }
  private firstModalRef: any;
  private secondModalRef: any;

   openFirstModal(content1: any) {
  // Close the second modal if it's open
  if (this.secondModalRef) {
    this.secondModalRef.close();
  }

  // Open the first modal
  const modalRef = this.modalService.open(content1, this.modalOptions);
  this.firstModalRef = modalRef;

  modalRef.result.then((result) => {
    // Handle modal close event if needed
  }).catch((reason) => {
    // Handle modal dismiss event if needed
  });
}
    // Define modal options
    modalOptions: NgbModalOptions = {
      centered: true
    };

openSecondModal(content1: any, content2: any) {
  // Close the first modal if it's open
  if (this.firstModalRef) {
    this.firstModalRef.close();
  }

  const modalRef = this.modalService.open(content2, this.modalOptions);
  this.secondModalRef = modalRef;

  modalRef.result.then((result) => {
    // Handle modal close event if needed
  }).catch((reason) => {
    // Handle modal dismiss event if needed
  });
}
TooltipPopovers(TooltipPopoversModal: any) {
  this.modalService.open(TooltipPopoversModal, { centered: true });
}
}
