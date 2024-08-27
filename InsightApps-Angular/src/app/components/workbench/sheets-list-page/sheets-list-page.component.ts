import { Component, OnInit } from '@angular/core';
import { WorkbenchService } from '../workbench.service';
import Swal from 'sweetalert2';
import { SharedModule } from '../../../shared/sharedmodule';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { NgxPaginationModule, PaginatePipe, PaginationControlsComponent } from 'ngx-pagination';
import { Router } from '@angular/router';
import { InsightsButtonComponent } from '../insights-button/insights-button.component';
import { ViewTemplateDrivenService } from '../view-template-driven.service';

@Component({
  selector: 'app-sheets-list-page',
  standalone: true,
  imports: [SharedModule,CommonModule,FormsModule,NgbModule,NgxPaginationModule,InsightsButtonComponent],
  templateUrl: './sheets-list-page.component.html',
  styleUrl: './sheets-list-page.component.scss'
})
export class SheetsListPageComponent implements OnInit {
  sheetName:any;
  savedSheetsList:any[]=[];
  sheetsList : any[] = [];
  selectedSheetList=0;
  itemsPerPage:any;
  pageNo = 1;
  page: number = 1;
  totalItems:any;
  gridView = true;
  viewSheetList = false;
constructor(private workbechService:WorkbenchService,private router:Router,private viewTemplateService:ViewTemplateDrivenService){
  this.viewSheetList = this.viewTemplateService.viewSheets()
}

  ngOnInit() {
    if (this.viewSheetList) {
      this.fetchSheetsList();
      // this.getUserSheetsList();
    }
  }

  loadSelectedSheetList(){
    if(this.selectedSheetList > 0){
    const Obj ={
      search:this.sheetName,
      page_no:this.pageNo,
      page_count:this.itemsPerPage,
      queryset_id:this.selectedSheetList
    }
    if(Obj.search == '' || Obj.search == null){
      delete Obj.search;
    }
    if(Obj.page_count == undefined || Obj.page_count == null){
      delete Obj.page_count;
    }
    this.workbechService.getUserSheetListPutTest(Obj).subscribe(
      {
        next:(data:any) =>{
          this.savedSheetsList=data.sheets
          this.itemsPerPage = data.items_per_page;
          this.totalItems = data.total_items
          console.log('sheetsList',data)
  
  
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
    } else {
      this.getUserSheetsList();
    }
  }

  fetchSheetsList(){
    const Obj ={
      search:this.sheetName,
      page_no:this.pageNo,
      page_count:this.itemsPerPage
    }
    if(Obj.search == '' || Obj.search == null){
      delete Obj.search;
    }
    if(Obj.page_count == undefined || Obj.page_count == null){
      delete Obj.page_count;
    }
    this.workbechService.fetchSheetsListData().subscribe(
      {
        next:(data:any) =>{
          this.sheetsList = data;
          this.itemsPerPage = data.items_per_page;
          this.totalItems = data.total_items
          console.log('sheetsList',data)
          this.selectedSheetList = 0;
          this.loadSelectedSheetList();
  
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

pageChangegetUserSheetsList(page:any){
this.pageNo=page;
this.getUserSheetsList();
}
searchUserList(){
  this.pageNo=1
  this.getUserSheetsList();
}
onChangeofPagecount(count:any){

}
getUserSheetsList(){
  const Obj ={
    search:this.sheetName,
    page_no:this.pageNo,
    page_count:this.itemsPerPage
  }
  if(Obj.search == '' || Obj.search == null){
    delete Obj.search;
  }
  if(Obj.page_count == undefined || Obj.page_count == null){
    delete Obj.page_count;
  }
  this.workbechService.getUserSheetListPut(Obj).subscribe(
    {
      next:(data:any) =>{
        this.savedSheetsList=data.sheets
        this.itemsPerPage = data.items_per_page;
        this.totalItems = data.total_items
        console.log('sheetsList',data)


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
viewSheet(serverId:any,fileId:any,querysetId:any,sheetId:any){
  // const encodedServerId = btoa(serverId.toString());
  const encodedQuerySetId = btoa(querysetId.toString());
  const encodedSheetId = btoa(sheetId.toString());


  if (serverId === null ) {
    const encodedFileId = btoa(fileId.toString());
    this.router.navigate(['/workbench/landingpage/fileId/sheets/'+encodedFileId+'/'+encodedQuerySetId+'/'+encodedSheetId])

  }

  if(fileId === null){
    const encodedServerId = btoa(serverId.toString());
    this.router.navigate(['/workbench/landingpage/dbId/sheets/'+encodedServerId+'/'+encodedQuerySetId+'/'+encodedSheetId])

  }

  // this.router.navigate(['/workbench/landingpage/sheets/'+encodedServerId+'/'+encodedQuerySetId+'/'+encodedSheetId])
}
deleteSheet(serverId:any,fileId:any,qurysetId:any,sheetId:any){
  const obj ={
    sheet_id:sheetId,
  }
  this.workbechService.deleteSheetMessage(obj)
  .subscribe(
    {
      next:(data:any) => {
        console.log(data);      
        if(data){
          Swal.fire({
            title: 'Are you sure?',
            text: data.message,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
          }).then((result)=>{
            if(result.isConfirmed){
              const idToPass = fileId == null ? serverId : fileId;

              this.workbechService.deleteSheet(idToPass,qurysetId,sheetId)
              .subscribe(
                {
                  next:(data:any) => {
                    console.log(data);      
                    if(data){
                      Swal.fire({
                        icon: 'success',
                        title: 'Deleted!',
                        text: 'Sheet Deleted Successfully',
                        width: '400px',
                      })
                    }
                    this.getUserSheetsList();
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
}
sheetsRoute(){
  this.router.navigate(['/workbench/sheets'])  
}
}
