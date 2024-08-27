import { Component, Injectable } from '@angular/core';
import Swal, { SweetAlertResult } from 'sweetalert2';
import { SharedModule } from '../../../shared/sharedmodule';

@Injectable({
  providedIn: 'root',
})
export class SwalService {
  fire(config: any): Promise<SweetAlertResult<any>> {
    return Swal.fire(config);
  }
}
@Component({
  selector: 'app-sweetalerts',
  standalone: true,
  imports: [SharedModule],
  templateUrl: './sweetalerts.component.html',
  styleUrls: ['./sweetalerts.component.scss']
})
export class SweetalertsComponent {
  constructor(private swalService: SwalService) {}

  async openSwal() {
    const { value: email } = await this.swalService.fire({
      title: 'Input email address',
      input: 'email',
      inputLabel: 'Your email address',
      inputPlaceholder: 'Enter your email address',
    });

    if (email) {
      this.swalService.fire(`Entered email: ${email}`);
    }
  }

  basicAlert() {
    Swal.fire({
      title: 'Hello this is  Basic alert Message',
      confirmButtonColor: '#0162e8',
    });
  }
  basicAlert1() {
    Swal.fire({
      icon: 'question',
      title: 'The internet',
      text: 'That thing is still around?',
      confirmButtonColor: '#0162e8',
    });
  }
  basicAlert2() {
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: "Something went wrong!",
      footer: '<a href="#">Why do I have this issue?</a>'
    });
  }
  longWindow(){
    Swal.fire({
      imageUrl: "https://placeholder.pics/svg/300x1500",
      imageHeight: 1500,
      imageAlt: "A tall image"
    });
  }
  htmlAlert(){
    Swal.fire({
      title: "<strong>HTML <u>example</u></strong>",
      icon: "info",
      html: `
        You can use <b>bold text</b>,
        <a href="#">links</a>
        and other HTML tags
      `,
      showCloseButton: true,
      showCancelButton: true,
      focusConfirm: false,
      confirmButtonText: `
        <i class="fe fe-thumbs-up"></i> Great!
      `,
      confirmButtonAriaLabel: "Thumbs up, great!",
      cancelButtonText: `
        <i class="fe fe-thumbs-down"></i>
      `,
      cancelButtonAriaLabel: "Thumbs down"
    });
  }
  multipleButtons(){
    Swal.fire({
      title: "Do you want to save the changes?",
      showDenyButton: true,
      showCancelButton: true,
      confirmButtonText: "Save",
      denyButtonText: `Don't save`
    }).then((result: { isConfirmed: any; isDenied: any; }) => {
      /* Read more about isConfirmed, isDenied below */
      if (result.isConfirmed) {
        Swal.fire("Saved!", "", "success");
      } else if (result.isDenied) {
        Swal.fire("Changes are not saved", "", "info");
      }
    });
  }
  alertDialog(){
    Swal.fire({
      position: "top-end",
      icon: "success",
      title: "Your work has been saved",
      showConfirmButton: false,
      timer: 1500
    });
  }
  confirmAlert(){
    Swal.fire({
      title: "Are you sure?",
      text: "You won't be able to revert this!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, delete it!"
    }).then((result: { isConfirmed: any; }) => {
      if (result.isConfirmed) {
        Swal.fire({
          title: "Deleted!",
          text: "Your file has been deleted.",
          icon: "success"
        });
      }
    });
  }
  parameters(){
    const swalWithBootstrapButtons = Swal.mixin({
      customClass: {
        confirmButton: "btn btn-success",
        cancelButton: "btn btn-danger me-2"
      },
      buttonsStyling: false
    });
    swalWithBootstrapButtons.fire({
      title: "Are you sure?",
      text: "You won't be able to revert this!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "Yes, delete it!",
      cancelButtonText: "No, cancel!",
      reverseButtons: true
    }).then((result: any) => {
      if (result.isConfirmed) {
        swalWithBootstrapButtons.fire({
          title: "Deleted!",
          text: "Your file has been deleted.",
          icon: "success"
        });
      } else if (
        /* Read more about handling dismissals below */
        result.dismiss === Swal.DismissReason.cancel
      ) {
        swalWithBootstrapButtons.fire({
          title: "Cancelled",
          text: "Your imaginary file is safe :)",
          icon: "error"
        });
      }
    });
  }
  ImageAlert(){
    Swal.fire({
      title: "Sweet!",
      text: "Modal with a custom image.",
      imageUrl: "./assets/images/media/2.jpg",
      imageWidth: 400,
      imageHeight: 200,
      imageAlt: "Custom image"
    });
  }
  customAlert(){
    Swal.fire({
      title: "Custom width, padding, color, background.",
      width: 600,
      padding: "3em",
      color: 'rgb(255, 255, 255)',
      background: '#716add url(./assets/images/media/1.jpg)',
    });
  }
  autoClose(){
    Swal.fire({
      title: 'Auto close alert!',
      text: 'I will close in 2 seconds.',
      confirmButtonColor: '#0162e8',
      timer: 2000,
      timerProgressBar: true,
    });
  }
}
