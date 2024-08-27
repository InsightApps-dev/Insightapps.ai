import { Component } from '@angular/core';
import { NgApexchartsModule } from 'ng-apexcharts';
import { chartOptions,chartOptions4,chartOptions5,chartOptions3, DonutChartData } from '../../../shared/data/dashboard';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
const DATA=[
  {
    id:'#1537890',
    src:'./assets/images/shop/1.png',
    name:' A semi minimal chair',
    rating:' 5.0 ',
    rating1:'(90 Mem)',
    status:'Shipped',
    customer:'Simon Cowall',
    quantity:'1',
    text:'success',
    bg:'success',
    price:'$4320.29',
    date:'25 Mar 2022',
    check:"checked"
  },
  {
    id:'#1539078',
    src:'./assets/images/shop/2.png',
    name:' A semi minimal chair',
    rating:' 3.0 ',
    rating1:'(50 Mem)',
    status:'Cancelled',
    customer:'Meisha Kerr	',
    quantity:'1',
    text:'danger',
    bg:'danger',
    price:'$6745.29',
    date:'25 Mar 2022',

  },
  {
    id:'#1539832',
    src:'./assets/images/shop/4.png',
    name:'Mony layer headphones',
    rating:' 4.5 ',
    rating1:'(65 Mem)',
    status:'Under Process',
    customer:'Jessica',
    quantity:'2',
    text:'info',
    bg:'info',
    price:'$1176.89',
    date:'27 Feb 2022',

  },
  {
    id:'#1538267',
    src:'./assets/images/shop/3.png',
    name:'Sportive coloured shoes',
    rating:' 2.5 ',
    rating1:'(15 Mem)',
    status:'Shipped',
    customer:'Jason Stathman',
    quantity:'1',
    text:'success',
    bg:'success',
    price:'$1867.29',
    date:'2 Apr 2022',

  },
  {
    id:'#1537880',
    src:'./assets/images/shop/7.png',
    name:'Vayon black shades',
    rating:' 3.5 ',
    rating1:'(36 Mem)',
    status:'Shipped',
    customer:'Khabib Hussain',
    quantity:'1',
    text:'success',
    bg:'success',
    price:'$2439.29',
    date:'8 Apr 2022',

  },

]
@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [SharedModule,NgApexchartsModule,NgbModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})

export class DashboardComponent {
  public chartOptions = chartOptions;
  public chartOptions4 = chartOptions4;
  public chartOptions5 = chartOptions5;
  public chartOptions3 = chartOptions3;

  public donutData = DonutChartData;
  products=DATA;
  click = (id:string)=>{
    const data = this.products.filter((x: {id: string; }) =>{
      return x.id != id;
    });
    this.products = data;
  };
}
