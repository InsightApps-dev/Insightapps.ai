import { Component, OnInit, ViewChild } from '@angular/core';
import { WorkbenchService } from '../workbench.service';
import Swal from 'sweetalert2';
import { CommonModule } from '@angular/common';
import { NgbModal, NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { SharedModule } from '../../../shared/sharedmodule';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { NgxPaginationModule } from 'ngx-pagination';
import { InsightsButtonComponent } from '../insights-button/insights-button.component';
import { ViewTemplateDrivenService } from '../view-template-driven.service';
import { NgSelectModule } from '@ng-select/ng-select';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-dashboard-page',
  standalone: true,
  imports: [NgbModule,CommonModule,SharedModule,FormsModule,NgxPaginationModule,InsightsButtonComponent,NgSelectModule],
  templateUrl: './dashboard-page.component.html',
  styleUrl: './dashboard-page.component.scss'
})
export class DashboardPageComponent implements OnInit{
  savedDashboardList:any[]=[];
  dashboardName :any;
  itemsPerPage!:any;
  pageNo = 1;
  page: number = 1;
  totalItems:any;
  gridView = true;
  viewDashboardList = false;
  dashboardId:any;
  dashboardPropertyTitle:any;
  roleDetails = [] as any;
  selectedRoleIds = [] as any;
  selectedRoleIdsToNumbers = [] as any;
  selectedUserIds = [] as any;
  selectedUserIdsToNumbers = [] as any;
  usersOnSelectedRole = [] as any;
  createUrl =false;
  publicUrl:any;
  shareAsPrivate = false;

  @ViewChild('propertiesModal') propertiesModal : any;

constructor(private workbechService:WorkbenchService,private router:Router,private templateViewService:ViewTemplateDrivenService,
  private modalService:NgbModal,private toasterservice:ToastrService){
  this.viewDashboardList=this.templateViewService.viewDashboard()
}
ngOnInit(){
  if(this.viewDashboardList){
  this.getuserDashboardsListput();
  }
}
pageChangeUserDashboardsList(page:any){
this.pageNo=page;
this.getuserDashboardsListput();
}
searchDashboarList(){
  this.pageNo=1;
  this.getuserDashboardsListput();
}
getuserDashboardsListput(){
  const Obj ={
    search:this.dashboardName,
    page_no:this.pageNo,
    page_count:this.itemsPerPage

  }
  if(Obj.search == '' || Obj.search == null){
    delete Obj.search;
  }
  if(Obj.page_count == undefined || Obj.page_count == null){
    delete Obj.page_count;
  }
  this.workbechService.getuserDashboardsListput(Obj).subscribe(
    {
      next:(data:any) =>{
        this.savedDashboardList=data.sheets
        this.itemsPerPage = data.items_per_page;
        this.totalItems = data.total_items;
        console.log('dashboardList',this.savedDashboardList)

      },
      error:(error:any)=>{
      console.log(error);
      Swal.fire({
        icon: 'error',
        title: 'oops!',
        text: error.error.message,
        width: '400px',
      })
    }
    })
}
deleteDashboard(dashboardId:any){
  Swal.fire({
    title: 'Are you sure?',
    text: "You won't be able to revert this!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Yes, delete it!'
  }).then((result)=>{
    if(result.isConfirmed){
      this.workbechService.deleteDashboard(dashboardId)
      .subscribe(
        {
          next:(data:any) => {
            console.log(data);      
            if(data){
              Swal.fire({
                icon: 'success',
                title: 'Deleted!',
                text: 'Dashboard Deleted Successfully',
                width: '400px',
              })
            }
            this.getuserDashboardsListput();
          },
          error:(error:any)=>{
            Swal.fire({
              icon: 'warning',
              text: error.error.message,
              width: '300px',
            })
            console.log(error)
          }
        } 
      )
    }})
}
viewDashboard(serverId:any,querysetId:any,dashboardId:any){
  const encodedServerId = btoa(serverId.toString());
  const encodedQuerySetId = btoa(querysetId.toString());
  const encodedDashboardId = btoa(dashboardId.toString());

  this.router.navigate(['/workbench/landingpage/sheetsdashboard/'+encodedDashboardId])
}
dashboardRoute(){
this.router.navigate(['/workbench/sheetsdashboard']);
}



viewPropertiesTab(name:any,dashboardId:any){
  this.modalService.open(this.propertiesModal);
  this.getRoleDetailsDshboard();
  this.dashboardPropertyTitle = name;
  this.dashboardId = dashboardId;
  this.getAddedDashboardProperties();

}
onRolesChange(selected: string[]) {
  this.selectedRoleIds = selected
  this.selectedRoleIdsToNumbers = selected.map(value => Number(value));
  console.log('selectedRoles',this.selectedRoleIdsToNumbers)

  // You can store or process the selected values here
}
getRoleDetailsDshboard(){
this.workbechService.getRoleDetailsDshboard().subscribe({
  next:(data)=>{
    console.log('dashboardroledetails',data);
    this.roleDetails = data;
    // this.getUsersforRole();
   },
  error:(error)=>{
    console.log(error);
    Swal.fire({
      icon: 'error',
      title: 'oops!',
      text: error.error.message,
      width: '400px',
    })
  }
}) 
}
getUsersforRole(){
const obj ={
  role_ids:this.selectedRoleIdsToNumbers
}
this.workbechService.getUsersOnRole(obj).subscribe({
  next:(data)=>{
    this.usersOnSelectedRole = data
    console.log('usersOnselecetdRoles',data);
   },
  error:(error)=>{
    console.log(error);
    Swal.fire({
      icon: 'error',
      title: 'oops!',
      text: error.error.message,
      width: '400px',
    })
  }
})
}
getSelectedUsers(selected: string[]){
this.selectedUserIds = selected;
this.selectedUserIdsToNumbers = this.selectedUserIds.map((value: any) => Number(value));
console.log('selectedUsers',this.selectedUserIdsToNumbers)

}

saveDashboardProperties(){
const obj ={
  dashboard_id:this.dashboardId,
  role_ids:this.selectedRoleIdsToNumbers,
  user_ids:this.selectedUserIdsToNumbers
}
this.workbechService.saveDashboardProperties(obj).subscribe({
  next:(data)=>{
    console.log('properties save',data);
    this.modalService.dismissAll();
    Swal.fire({
      icon: 'success',
      title: 'Done!',
      text: data.message,
      width: '400px',
    })
   },
  error:(error)=>{
    console.log(error);
    Swal.fire({
      icon: 'error',
      title: 'oops!',
      text: error.error.message,
      width: '400px',
    })
  }
})
}
getAddedDashboardProperties(){
  this.workbechService.getAddedDashboardProperties(this.dashboardId).subscribe({
    next:(data)=>{
      this.selectedRoleIds = data.roles.map((role: any) => role.role);
      this.selectedUserIds = data.users.map((user:any)=>user.username);
      console.log('savedrolesandUsers',data);
      this.selectedRoleIdsToNumbers = data.roles?.map((role:any) => role.id);
      this.selectedUserIdsToNumbers = data.users?.map((user:any) => user.user_id);

     },
    error:(error)=>{
      console.log(error);
      Swal.fire({
        icon: 'error',
        title: 'oops!',
        text: error.error.message,
        width: '400px',
      })
    }
  }) 
}


sharePublish(value:any){
  console.log(value);
  if(value === 'public'){
    this.createUrl = true;
    this.shareAsPrivate = false
    const publicDashboardId = btoa(this.dashboardId.toString());
    this.publicUrl = 'http://54.67.88.195:4200/public/dashboard/'+publicDashboardId
  } else if(value === 'private'){
    this.createUrl = false;
    this.shareAsPrivate = true;
  }
  }
copyUrl(): void {
  if (navigator.clipboard) {
    navigator.clipboard.writeText(this.publicUrl).then(() => {
      console.log(this.publicUrl);
      this.toasterservice.success('Link Copied', 'success', { positionClass: 'toast-center-center' });
    }).catch(err => {
      console.error('Could not copy text: ', err);
      this.fallbackCopyTextToClipboard(this.publicUrl);
    });
  } else {
    // Fallback if navigator.clipboard is not available
    this.fallbackCopyTextToClipboard(this.publicUrl);
  }
}

fallbackCopyTextToClipboard(text: string): void {
  const textArea = document.createElement('textarea');
  textArea.value = text;
  textArea.style.position = 'fixed';  // Avoid scrolling to bottom
  textArea.style.opacity = '0';
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  try {
    const successful = document.execCommand('copy');
    if (successful) {
      this.toasterservice.success('Link Copied', 'success', { positionClass: 'toast-center-center' });
    } else {
      console.error('Fallback: Could not copy text');
    }
  } catch (err) {
    console.error('Fallback: Unable to copy', err);
  }
  document.body.removeChild(textArea);
}
}
