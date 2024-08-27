import { Component } from '@angular/core';
import { NgbModal, NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgSelectModule } from '@ng-select/ng-select';
const DATA=[
  {
    id:"1",
    src:"./assets/images/users/16.jpg",
    name:"Adam Cotter",
    country:"France",
    bg:"primary",
    status:"Active",
    date:"09 Dec 2017",
    check:"checked"
  },
  {
    id:"2",
    src:"./assets/images/users/15.jpg",
    name:"Pauline Noble",
    country:"Brazil",
    bg:"danger",
    status:"Inactive",
    date:"09 Dec 2017",
  },
  {
    id:"3",
    src:"./assets/images/users/4.jpg",
    name:"Sherilyn Metzel",
    country:"USA",
    bg:"warning",
    status:"Pending",
    date:"27 Jan 2018",
  },
  {
    id:"4",
    src:"./assets/images/users/3.jpg",
    name:"Terrie Boaler",
    country:"Canada",
    bg:"primary",
    status:"Active",
    date:"20 Jan 2018",
    check:"checked"
  },
  {
    id:"5",
    src:"./assets/images/users/19.jpg",
    name:"Rutter Pude",
    country:"Australia",
    bg:"warning",
    status:"Pending",
    date:"13 Jan 2018",
  },
  {
    id:"6",
    src:"./assets/images/users/21.jpg",
    name:"Clifford Benjamin",
    country:"China",
    bg:"danger",
    status:"Inactive",
    date:"25 Jan 2018",

  },
  {
    id:"7",
    src:"./assets/images/users/12.jpg",
    name:"Thedric Romans",
    country:"Russia",
    bg:"primary",
    status:"Active",
    date:"12 Jan 2018",
   
  },
  {
    id:"8",
    src:"./assets/images/users/1.jpg",
    name:" Haily Carthew",
    country:"Thailand",
    bg:"primary",
    status:"Active",
    date:"27 Jan 2018",
    check:"checked"

  },
  {
    id:"9",
    src:"./assets/images/users/12.jpg",
    name:"Dorothea Joicey",
    country:"Indonesia",
    bg:"primary",
    status:"Inactive",
    date:"12 Dec 2017",
   
  },
  {
    id:"10",
    src:"./assets/images/users/15.jpg",
    name:"Mikaela Pinel",
    country:"France",
    bg:"warning",
    status:"Pending",
    date:"10 Dec 2017",
    
  },
  {
    id:"11",
    src:"./assets/images/users/12.jpg",
    name:"Donnell Farries",
    country:"Poland",
    bg:"primary",
    status:"Active",
    date:"3 Dec 2017",
   
  },
  {
    id:"12",
    src:"./assets/images/users/4.jpg",
    name:"Letizia Puncher",
    country:"Ukraine",
    bg:"danger",
    status:"Inactive",
    date:"9 Dec 2017",
    check:"checked"
  },
]
@Component({
  selector: 'app-userlist',
  standalone: true,
  imports: [SharedModule,NgbModule,NgSelectModule],
  templateUrl: './userlist.component.html',
  styleUrls: ['./userlist.component.scss']
})
export class UserlistComponent {
  constructor(
    private modalService: NgbModal,
  ) { }
  active=1;
  users=DATA;
  click = (id:string)=>{
    const data = this.users.filter((x: {id: string; }) =>{
      return x.id != id;
    });
    this.users = data;
  };
  BasicOpen(basicmodal:any) {
    this.modalService.open(basicmodal);
  }
}

