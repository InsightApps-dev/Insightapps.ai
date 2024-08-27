import { Component } from '@angular/core';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
interface Alert {
  type: string;
  message:string;
  message1:string;
}
interface Alert1 {
  type: string;
  message:string;
  message1:string;
  message2:string;
}
interface Alert2 {
  type:string;
  icon: string;
  message:string;
 
}
interface Alert3 {
  type:string;
  img: string;
 
}
interface Alert4 {
  type:string;
  message: string;
  message1: string;
  message2: string;
  icon:string


 
}
const dismissingAlerts: Alert[] = [
  {
    type: 'primary',
    message:"Well done!",
    message1:'You successfully read this important alert message.'
  },
  {
    type: 'secondary',
    message:"Well done!",
    message1:'You successfully read this important alert message.'
  },
  {
    type: 'success',
    message:"Well done!",
    message1:'You successfully read this important alert message.'
  },
  {
    type: 'info',
    message:"Heads up!",
    message1:"This alert needs your attention, but it's not super important."
  },
  {
    type: 'light',
    message:"Heads up!",
    message1:"This alert needs your attention, but it's not super important."
  },
  {
    type: 'dark',
    message:"Heads up!",
    message1:"This alert needs your attention, but it's not super important."
  },
  {
    type: 'warning',
    message:"Warning!",
    message1:"Better check yourself, you're not looking too good."
  },
  {
    type: 'danger',
    message:"Oh snap!",
    message1:'Change a few things up and try submitting again.'
  },
];
const linkAlerts: Alert1[] = [
  {
    type: 'primary',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message."
  },
  {
    type: 'secondary',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message."
  },
  {
    type: 'success',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message."
  },
  {
    type: 'info',
    message:"Heads up!",
    message1:"This  but it's not super important.",
    message2:"alert needs your attention,"
  },
 
  {
    type: 'warning',
    message:"Warning!",
    message1:"Better check yourself, you're ",
    message2:"not looking too good."
  },
  {
    type: 'dark',
    message:"Oh snap!",
    message1:'Change a few things up',
    message2:"and try submitting again."
  },
];
const iconAlerts: Alert2[] = [
  {
    type: 'primary',
    message:'Well done! You successfully read this important alert message.',
    icon:'check-circle'
  },
  {
    type: 'secondary',
    message:"Heads up! This alert needs your attention, but it's not super important.",
    icon:'bell'
  },
  {
    type: 'success',
    message:"Well done! You successfully read this important alert message.",
    icon:'check-circle'
  },
  {
    type: 'info',
    message:"Heads up! This alert needs your attention, but it's not super important.",
    icon:"bell"
  },

  {
    type: 'warning',
    icon:"exclamation",
    message:"Better check yourself, you're not looking too good."
  },
  {
    type: 'danger',
    message:"Oh snap!Change a few things up and try submitting again.",
    icon:'frown'
  },
];
const avatarAlerts: Alert3[] = [
  {
    type: 'primary',
    img:"./assets/images/users/14.jpg",
  },
  {
    type: 'secondary',
    img:"./assets/images/users/14.jpg",
  },
  {
    type: 'success',
    img:"./assets/images/users/5.jpg",
  },
  {
    type: 'info',
    img:"./assets/images/users/5.jpg",
  },

  {
    type: 'warning',
    img:"./assets/images/users/15.jpg"
  },
  {
    type: 'danger',
    img:"./assets/images/users/6.jpg",
  },
];
const outlineAlerts: Alert4[] = [
  {
    type: 'primary',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'fe fe-check-circle me-2 d-inline-flex text-primary'
  },
  {
    type: 'secondary',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'fe fe-user-check me-2 d-inline-flex text-secondary'
   },
  {
    type: 'success',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'fe fe-thumbs-up me-2 d-inline-flex text-success'
  },
  {
    type: 'info',
    message:"Heads up!",
    message1:"This  but it's not super important.",
    message2:"alert needs your attention,",
    icon:'fe fe-bell me-2 d-inline-flex text-info'
  },
 
  {
    type: 'warning',
    message:"Warning!",
    message1:"Better check yourself, you're ",
    message2:"not looking too good.",
    icon:'fe fe-info me-2 d-inline-flex text-warning'
  },

];
const solidAlerts: Alert4[] = [
  {
    type: 'primary',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'check-circle-o'
  },
  {
    type: 'secondary',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'bell-o'
   },
  {
    type: 'success',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'check-circle-o'
  },
  {
    type: 'info',
    message:"Heads up!",
    message1:"This  but it's not super important.",
    message2:"alert needs your attention,",
    icon:'bell-o'
  },
 
  {
    type: 'warning',
    message:"Warning!",
    message1:"Better check yourself, you're ",
    message2:"not looking too good.",
    icon:'exclamation'
  },

];
const roundedAlerts: Alert4[] = [
  {
    type: 'primary',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'fe fe-check-circle me-2 d-inline-flex lh-1 text-primary'
  },
  {
    type: 'secondary',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'fe fe-user-check me-2 d-inline-flex lh-1 text-secondary'
   },
  {
    type: 'success',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'fe fe-thumbs-up me-2 d-inline-flex lh-1 text-success'
  },
  {
    type: 'info',
    message:"Heads up!",
    message1:"This  but it's not super important.",
    message2:"alert needs your attention,",
    icon:'fe fe-bell me-2 d-inline-flex lh-1 text-info'
  },
 
  {
    type: 'warning',
    message:"Warning!",
    message1:"Better check yourself, you're ",
    message2:"not looking too good.",
    icon:'fe fe-info me-2 d-inline-flex lh-1 text-warning'
  },

];
const roundedsolidAlerts: Alert4[] = [
  {
    type: 'primary',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'check-circle'
  },
  {
    type: 'secondary',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'bell'
   },
  {
    type: 'success',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'thumbs-up'
  },
  {
    type: 'info',
    message:"Heads up!",
    message1:"This  but it's not super important.",
    message2:"alert needs your attention,",
    icon:'bell'
  },
 
  {
    type: 'warning',
    message:"Warning!",
    message1:"Better check yourself, you're ",
    message2:"not looking too good.",
    icon:'exclamation'
  },

];
const roundedbgAlerts: Alert4[] = [
  {
    type: 'primary',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'check-circle'
  },
  {
    type: 'secondary',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'user-check'
   },
  {
    type: 'success',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'thumbs-up'
  },
  {
    type: 'info',
    message:"Heads up!",
    message1:"This  but it's not super important.",
    message2:"alert needs your attention,",
    icon:'bell'
  },
 
  {
    type: 'warning',
    message:"Warning!",
    message1:"Better check yourself, you're ",
    message2:"not looking too good.",
    icon:'info'
  },

];
const bgAlerts: Alert4[] = [
  {
    type: 'primary',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'check-circle'
  },
  {
    type: 'secondary',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'user-check'
   },
  {
    type: 'success',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'thumbs-up'
  },
  {
    type: 'info',
    message:"Heads up!",
    message1:"This  but it's not super important.",
    message2:"alert needs your attention,",
    icon:'bell'
  },
 
  {
    type: 'warning',
    message:"Warning!",
    message1:"Better check yourself, you're ",
    message2:"not looking too good.",
    icon:'info'
  },

];
const shadowAlerts: Alert4[] = [
  {
    type: 'alert alert-primary rounded-pill',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'fe fe-check-circle me-2 d-inline-flex lh-1 text-primary'
  },
  {
    type: 'alert alert-secondary rounded-pill shadow-secondary',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'fe fe-user-check me-2 d-inline-flex lh-1 text-secondary'
   },
  {
    type: 'alert alert-success rounded-pill shadow-success',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'fe fe-thumbs-up me-2 d-inline-flex lh-1 text-success'
  },
  {
    type: 'alert alert-info rounded-pill shadow-info',
    message:"Heads up!",
    message1:"This  but it's not super important.",
    message2:"alert needs your attention,",
    icon:'fe fe-bell me-2 d-inline-flex lh-1 text-info'
  },
 
  {
    type: 'alert alert-warning rounded-pill shadow-warning',
    message:"Warning!",
    message1:"Better check yourself, you're ",
    message2:"not looking too good.",
    icon:'fe fe-info me-2 d-inline-flex lh-1 text-warning'
  },

];
const gradientAlerts: Alert4[] = [
  {
    type: 'primary',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'check-circle'
  },
  {
    type: 'secondary',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'bell'
   },
  {
    type: 'success',
    message:"Well done!",
    message1:'You successfully read ',
    message2:"this important alert message.",
    icon:'thumbs-up'
  },
  {
    type: 'info',
    message:"Heads up!",
    message1:"This  but it's not super important.",
    message2:"alert needs your attention,",
    icon:'bell'
  },
 
  {
    type: 'warning',
    message:"Warning!",
    message1:"Better check yourself, you're ",
    message2:"not looking too good.",
    icon:'exclamation'
  },

];
@Component({
  selector: 'app-alerts',
  standalone: true,
  imports: [SharedModule,NgbModule],
  templateUrl: './alerts.component.html',
  styleUrls: ['./alerts.component.scss']
})
export class AlertsComponent {
  public isClosed = false;
  public isClosed1 = false;
  public isClosed2 = false;
  public isClosed3 = false;
  public isClosed4 = false;

  dismissingAlerts: Alert[] = dismissingAlerts;
i: any;
  dismissClose(index: number) {
    // Remove the alert from the array based on the index
    this.dismissingAlerts.splice(index, 1);
  }
  linkAlerts:Alert1[]=linkAlerts;
  iconAlerts:Alert2[]=iconAlerts;
  avatarAlerts:Alert3[]=avatarAlerts;
  outlineAlerts:Alert4[]=outlineAlerts;
  solidAlerts:Alert4[]=solidAlerts;
  roundedAlerts:Alert4[]=roundedAlerts;
  roundedbgAlerts:Alert4[]=roundedbgAlerts;
  bgAlerts:Alert4[]=bgAlerts;
  shadowAlerts:Alert4[]=shadowAlerts;
  gradientAlerts:Alert4[]=gradientAlerts;

  roundedsolidAlerts:Alert4[]=roundedsolidAlerts;
  linkClose(index: number) {
    // Remove the alert from the array based on the index
    this.linkAlerts.splice(index, 1);
  }
  iconClose(index: number) {
    // Remove the alert from the array based on the index
    this.iconAlerts.splice(index, 1);
  }
  avatarClose(index: number) {
    // Remove the alert from the array based on the index
    this.avatarAlerts.splice(index, 1);
  }
  outlineClose(index: number) {
    // Remove the alert from the array based on the index
    this.outlineAlerts.splice(index, 1);
  }
  solidClose(index: number) {
    // Remove the alert from the array based on the index
    this.solidAlerts.splice(index, 1);
  }
  roundedClose(index: number) {
    // Remove the alert from the array based on the index
    this.roundedAlerts.splice(index, 1);
  }
  roundedsolidClose(index: number) {
    // Remove the alert from the array based on the index
    this.roundedsolidAlerts.splice(index, 1);
  }
  roundedbgClose(index: number) {
    // Remove the alert from the array based on the index
    this.roundedbgAlerts.splice(index, 1);
  }
 bgClose(index: number) {
    // Remove the alert from the array based on the index
    this.bgAlerts.splice(index, 1);
  }
  shadowClose(index: number) {
    // Remove the alert from the array based on the index
    this.shadowAlerts.splice(index, 1);
  }
  gradientClose(index: number) {
    // Remove the alert from the array based on the index
    this.gradientAlerts.splice(index, 1);
  }
  Closetoggle(item: any) {
    if (item == 'zero') {
      this.isClosed = true;
    }
    if (item == 'one') {
      this.isClosed1 = true;
    }
    if (item == 'two') {
      this.isClosed2 = true;
    }
    if (item == 'three') {
      this.isClosed3 = true;
    }
    if (item == 'four') {
      this.isClosed4 = true;
    }
  }
  livealerts: { message: string; show: boolean }[] = [];

  showAlert() {
    // Add a new alert to the array
    this.livealerts.push({
      message: 'Nice, you triggered this alert message!',
      show: true,
    });
  }
  
  closeAlert(index: number) {
    this.livealerts.splice(index, 1);
  }
}
