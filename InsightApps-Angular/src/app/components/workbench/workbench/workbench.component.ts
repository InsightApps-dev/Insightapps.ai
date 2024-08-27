import { Component, OnInit, ViewChild } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { NgbModal, NgbModule} from '@ng-bootstrap/ng-bootstrap';
import { SharedModule } from '../../../shared/sharedmodule';
import { FormsModule } from '@angular/forms';
import { WorkbenchService } from '../workbench.service';
import {
  CdkDragDrop,
  CdkDrag,
  CdkDropList,
  CdkDropListGroup,
  moveItemInArray,
  transferArrayItem,
} from '@angular/cdk/drag-drop';
import { of } from 'rxjs';
import { data } from '../../charts/echarts/echarts';
import Swal from 'sweetalert2';
import { GalleryModule } from 'ng-gallery';
import { LightboxModule } from 'ng-gallery/lightbox';
import { ToastrModule, ToastrService } from 'ngx-toastr';
import { CommonModule } from '@angular/common';
import { NgxPaginationModule } from 'ngx-pagination';
import { InsightsButtonComponent } from '../insights-button/insights-button.component';
import { ViewTemplateDrivenService } from '../view-template-driven.service';
@Component({
  selector: 'app-workbench',
  standalone: true,
  imports: [RouterModule,NgbModule,SharedModule,FormsModule,CdkDropListGroup, CdkDropList, CdkDrag,GalleryModule,LightboxModule,ToastrModule,CommonModule,NgxPaginationModule,InsightsButtonComponent],
  templateUrl: './workbench.component.html',
  styleUrl: './workbench.component.scss'
})
export class WorkbenchComponent implements OnInit{
  @ViewChild('fileInput') fileInput:any;
  @ViewChild('fileInput1') fileInput1:any;

  
  tableList = [] as any;
  dragedTableName: any;
  databaseconnectionsList!:boolean;
  draggedtables = [] as any;
  getTableColumns = [] as any;
  getTableRows = [] as any;
  relationOfTables = [] as any;
  databaseId:any;
  fileId:any;
  databaseType:any;
  openPostgreSqlForm= false;
  openMySqlForm = false;
  openOracleForm = false;
  openMicrosoftSqlServerForm = false;
  openSnowflakeServerForm = false;
  openMongoDbForm = false;
  sqlLiteForm = false;
  openTablesUI = false;
  ibmDb2Form = false;
  databaseName:any;
  tableName:any;
  selectedClmnT1:any;
  selectedClmnT2:any;
  selectedCndn:any;
  tableRelationUi = false;
  custmT1Data = [] as any;
  custmT2Data = [] as any;
  connectionList =[] as any;
  searchDbName :any;
  viewNewDbs!:boolean;
  showPassword1 = false;
  toggleClass = "off-line";
  toggleClass1 = "off-line";
  gridView = true;

  itemsPerPage!:any;
  pageNo = 1;
  page: number = 1;
  totalItems:any;
  fileData:any;
  viewDatasourceList = false;
  constructor(private modalService: NgbModal, private workbechService:WorkbenchService,private router:Router,private toasterservice:ToastrService,private viewTemplateService:ViewTemplateDrivenService){ 
    localStorage.setItem('QuerySetId', '0');
    const currentUrl = this.router.url; 
    if(currentUrl.includes('workbench/work-bench/view-connections')){
      this.databaseconnectionsList= true;   
    } 
    if(currentUrl.includes('workbench/work-bench/new-connections')){
      this.viewNewDbs = true;
    }
    this.viewDatasourceList = this.viewTemplateService.viewDtabase();
  }
    postGreServerName = '';
    postGrePortName = '';
    postGreDatabaseName = '';
    postGreUserName = '';
    PostGrePassword = '';
    OracleServiceName = '';
    displayName ='';
    path='';

    openPostgreSql(){
    this.openPostgreSqlForm=true;
    this.databaseconnectionsList= false;
    this.viewNewDbs = false;
    }
    postgreSignIn(){
      const obj={
          "database_type":"postgresql",
          "hostname":this.postGreServerName,
          "port":this.postGrePortName,
          "username":this.postGreUserName,
          "password":this.PostGrePassword,
          "database": this.postGreDatabaseName,
          "display_name":this.displayName
      }
        this.workbechService.postGreSqlConnection(obj).subscribe({next: (responce) => {
              console.log(responce);
              console.log('tablelist',this.tableList)
              this.databaseName = responce.database.database_name
              this.databaseId = responce.database.database_id
              if(responce){
                Swal.fire({
                  icon: 'success',
                  title: 'Connected',
                  width: '400px',
                })
                this.databaseId=responce.database?.database_id
                this.openPostgreSqlForm = false;
                const encodedId = btoa(this.databaseId.toString());
                this.router.navigate(['/workbench/database-connection/tables/'+encodedId]);
              }
            },
            error: (error) => {
              console.log(error);
              this.toasterservice.error(error.error.message,'error',{ positionClass: 'toast-center-center'})
              // Swal.fire({
              //   icon:'error',
              //   title:'error',
              //   text:error.error.message,
              //   width:'600px'
              // })

            }
          }
        )

    }
    DatabaseUpdate(){
      const obj={
          // "database_type":"postgresql",
          "database_type":this.databaseType,
          "hostname":this.postGreServerName,
          "port":this.postGrePortName,
          "username":this.postGreUserName,
          "password":this.PostGrePassword,
          "database": this.postGreDatabaseName,
          "display_name":this.displayName,
          database_id:this.databaseId
      }
        this.workbechService.postGreSqlConnectionput(obj).subscribe({next: (responce) => {
              console.log(responce);
              this.modalService.dismissAll('close');
              if(responce){
                Swal.fire({
                  icon: 'success',
                  title: 'Updated Successfully',
                  width: '400px',
                })
               
              }
              this.getDbConnectionList();
            },
            error: (error) => {
              console.log(error);
              this.toasterservice.error(error.error.message,'error',{ positionClass: 'toast-center-center'})
              // Swal.fire({
              //   icon:'error',
              //   title:'error',
              //   text:error.error.message,
              //   width:'600px'
              // })

            }
          }
        )

    }
    openOracle(){
      this.openOracleForm=true;
      this.databaseconnectionsList= false;
      this.viewNewDbs = false;
    }


    OracleSignIn(){
      const obj={
          "database_type":"oracle",
          "hostname":this.postGreServerName,
          "port":this.postGrePortName,
          "username":this.postGreUserName,
          "password":this.PostGrePassword,
          "display_name":this.displayName,

      }
        this.workbechService.postGreSqlConnection(obj).subscribe({next: (responce) => {
              console.log(responce);
              console.log('tablelist',this.tableList)
              this.databaseName = responce.database.database_name
              this.databaseId = responce.database.database_id
              if(responce){
                Swal.fire({
                  icon: 'success',
                  title: 'Connected',
                  width: '400px',
                })
                this.databaseId=responce.database?.database_id
                this.modalService.dismissAll();
                this.openOracleForm = false;
                const encodedId = btoa(this.databaseId.toString());
                this.router.navigate(['/workbench/database-connection/tables/'+encodedId]);
              }
            },
            error: (error) => {
              console.log(error);
              Swal.fire({
                icon: 'warning',
                text: error.error.message,
                width: '300px',
              })
            }
          }
        )
    }
    openMySql(){
      this.openMySqlForm=true;
      this.databaseconnectionsList= false;
      this.viewNewDbs = false;
    }
    mySqlSignIn(){
      const obj={
          "database_type":"mysql",
          "hostname":this.postGreServerName,
          "port":this.postGrePortName,
          "username":this.postGreUserName,
          "password":this.PostGrePassword,
          "display_name":this.displayName,
          "database": this.postGreDatabaseName,

      }
        this.workbechService.DbConnection(obj).subscribe({next: (responce) => {
          console.log(responce)
              if(responce){
                Swal.fire({
                  icon: 'success',
                  title: 'Connected',
                  width: '400px',
                })
                this.databaseId=responce.database?.database_id
                this.modalService.dismissAll();
                this.openMySqlForm = false;
                const encodedId = btoa(this.databaseId.toString());
                this.router.navigate(['/workbench/database-connection/tables/'+encodedId]);
              }
            },
            error: (error) => {
              console.log(error);
              Swal.fire({
                icon: 'warning',
                text: error.error.message,
                width: '300px',
              })
            }
          }
        )
    }
    openMicrosoftSqlServer(){
      this.openMicrosoftSqlServerForm=true;
      this.databaseconnectionsList= false;
      this.viewNewDbs = false;
    }
    microsoftSqlSignIn(){
      const obj={
          "database_type":"microsoftsqlserver",
          "hostname":this.postGreServerName,
          "port":this.postGrePortName,
          "username":this.postGreUserName,
          "password":this.PostGrePassword,
          "display_name":this.displayName,
          "database": this.postGreDatabaseName,
      }
        this.workbechService.DbConnection(obj).subscribe({next: (responce) => {
          console.log(responce)
              if(responce){
                Swal.fire({
                  icon: 'success',
                  title: 'Connected',
                  width: '400px',
                })
                this.databaseId=responce.database?.database_id
                this.modalService.dismissAll();
                this.openMicrosoftSqlServerForm = false;
                const encodedId = btoa(this.databaseId.toString());
                this.router.navigate(['/workbench/database-connection/tables/'+encodedId]);
              }
            },
            error: (error) => {
              console.log(error);
              Swal.fire({
                icon: 'warning',
                text: error.error.message,
                width: '300px',
              })
            }
          }
        )
    }
    openSnowflakeServer(){
      this.openSnowflakeServerForm=true;
      this.databaseconnectionsList= false;
      this.viewNewDbs = false;
    }
    snowflakeSignIn(){
      const obj={
          "database_type":"snowflake",
          "hostname":this.postGreServerName,
          "port":this.postGrePortName,
          "username":this.postGreUserName,
          "password":this.PostGrePassword,
          "display_name":this.displayName,
          "database": this.postGreDatabaseName,
      }
        this.workbechService.DbConnection(obj).subscribe({next: (responce) => {
          console.log(responce)
              if(responce){
                Swal.fire({
                  icon: 'success',
                  title: 'Connected',
                  width: '400px',
                })
                this.databaseId=responce.database?.database_id
                this.modalService.dismissAll();
                this.openSnowflakeServerForm = false;
                const encodedId = btoa(this.databaseId.toString());
                this.router.navigate(['/workbench/database-connection/tables/'+encodedId]);
              }
            },
            error: (error) => {
              console.log(error);
              Swal.fire({
                icon: 'warning',
                text: error.error.message,
                width: '300px',
              })
            }
          }
        )
    }
    openMOngoDb(){
      this.openMongoDbForm=true;
      this.databaseconnectionsList= false;
      this.viewNewDbs = false;
    }
    mongoDbSignIn(){
      const obj={
          "database_type":"mongodb",
          "hostname":this.postGreServerName,
          "port":this.postGrePortName,
          "username":this.postGreUserName,
          "password":this.PostGrePassword,
          "display_name":this.displayName,
          "database": this.postGreDatabaseName,
      }
        this.workbechService.DbConnection(obj).subscribe({next: (responce) => {
          console.log(responce)
              if(responce){
                Swal.fire({
                  icon: 'success',
                  title: 'Connected',
                  width: '400px',
                })
                this.databaseId=responce.database?.database_id
                this.modalService.dismissAll();
                this.openMongoDbForm = false;
                const encodedId = btoa(this.databaseId.toString());
                this.router.navigate(['/workbench/database-connection/tables/'+encodedId]);
              }
            },
            error: (error) => {
              console.log(error);
              Swal.fire({
                icon: 'warning',
                text: error.error.message,
                width: '300px',
              })
            }
          }
        )
    }
    openIbmDb2(){
      this.ibmDb2Form=true;
      this.databaseconnectionsList= false;
      this.viewNewDbs = false;
    }
    ibmDb2SignIn(){
      const obj={
          "database_type":"ibmdb2",
          "hostname":this.postGreServerName,
          "port":this.postGrePortName,
          "username":this.postGreUserName,
          "password":this.PostGrePassword,
          "display_name":this.displayName,
          "database": this.postGreDatabaseName,
      }
        this.workbechService.DbConnection(obj).subscribe({next: (responce) => {
          console.log(responce)
              if(responce){
                Swal.fire({
                  icon: 'success',
                  title: 'Connected',
                  width: '400px',
                })
                this.databaseId=responce.database?.database_id
                this.modalService.dismissAll();
                this.ibmDb2Form = false;
                const encodedId = btoa(this.databaseId.toString());
                this.router.navigate(['/workbench/database-connection/tables/'+encodedId]);
              }
            },
            error: (error) => {
              console.log(error);
              Swal.fire({
                icon: 'warning',
                text: error.error.message,
                width: '300px',
              })
            }
          }
        )
    }

    opensqlLite(){
      this.sqlLiteForm=true;
      this.databaseconnectionsList= false;
      this.viewNewDbs = false;
    }
    uploadfile(event:any){
      const file:File = event.target.files[0];
      this.fileData = file
    }
    sqLiteSignIn(){
      const formData: FormData = new FormData();
      formData.append('path', this.fileData,this.fileData.name); 
      formData.append('database_type','sqlite');
      formData.append('display_name',this.displayName);

        this.workbechService.DbConnection(formData).subscribe({next: (responce) => {
          console.log(responce)
              if(responce){
                Swal.fire({
                  icon: 'success',
                  title: 'Connected',
                  width: '400px',
                })
                this.databaseId=responce.database?.database_id
                this.modalService.dismissAll();
                this.ibmDb2Form = false;
                const encodedId = btoa(this.databaseId.toString());
                this.router.navigate(['/workbench/database-connection/tables/'+encodedId]);
              }
            },
            error: (error) => {
              console.log(error);
              Swal.fire({
                icon: 'warning',
                text: error.error.message,
                width: '300px',
              })
            }
          }
        )
    }

    triggerFileUpload(value:any) {
      if(value === 'csv'){
      this.fileInput.nativeElement.click();
      }else if(value === 'excel'){
        this.fileInput1.nativeElement.click();
      }
    }

    uploadfileCsv(event:any){
      const file:File = event.target.files[0];
      this.fileData = file;
      if(this.fileData){
        this.csvUpload();
      }

    }
    csvUpload(){
    const formData: FormData = new FormData();
      formData.append('file_path', this.fileData,this.fileData.name); 
      formData.append('file_type','csv');
      this.workbechService.DbConnectionFiles(formData).subscribe({next: (responce) => {
        console.log(responce)
            if(responce){
              Swal.fire({
                icon: 'success',
                title: 'Connected',
                width: '400px',
              })

              this.fileId=responce.file_id
              const encodedId = btoa(this.fileId.toString());
              this.router.navigate(['/workbench/database-connection/files/tables/'+encodedId]);
            }
          },
          error: (error) => {
            console.log(error);
            Swal.fire({
              icon: 'warning',
              text: error.error.message,
              width: '300px',
            })
          }
        }
      )
    }
    uploadfileExcel(event:any){
      const file:File = event.target.files[0];
      this.fileData = file;
      if(this.fileData){
        this.excelUpload();
      }

    }
    excelUpload(){
      const formData: FormData = new FormData();
        formData.append('file_path', this.fileData,this.fileData.name); 
        formData.append('file_type','excel');
        this.workbechService.DbConnectionFiles(formData).subscribe({next: (responce) => {
          console.log(responce)
              if(responce){
                Swal.fire({
                  icon: 'success',
                  title: 'Connected',
                  width: '400px',
                })
                this.fileId=responce.file_id
               
                const encodedId = btoa(this.fileId.toString());
                this.router.navigate(['/workbench/database-connection/files/tables/'+encodedId]);
              }
            },
            error: (error) => {
              console.log(error);
              Swal.fire({
                icon: 'warning',
                text: error.error.message,
                width: '300px',
              })
            }
          }
        )
      }
    deleteDbConnection(dbId:any,fileId:any){
      // const obj ={
      //   database_id:dbId
      // }
      let obj: any = {};

      if (dbId) {
        obj = { database_id: dbId };
      } else if (fileId) {
        obj = { file_id: fileId };
      }
      this.workbechService.deleteDbMsg(obj)
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
                  if(dbId){
                  this.workbechService.deleteDbConnection(dbId)
                  .subscribe(
                    {
                      next:(data:any) => {
                        console.log(data);      
                        if(data){
                          Swal.fire({
                            icon: 'success',
                            title: 'Deleted!',
                            text: 'Databse Deleted Successfully',
                            width: '400px',
                          })
                        }
                        this.getDbConnectionList();
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
                  if(fileId){
                    this.workbechService.deleteFileConnection(fileId)
                    .subscribe(
                      {
                        next:(data:any) => {
                          console.log(data);      
                          if(data){
                            Swal.fire({
                              icon: 'success',
                              title: 'Deleted!',
                              text: 'Databse Deleted Successfully',
                              width: '400px',
                            })
                          }
                          this.getDbConnectionList();
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
    editDbConnectionModal(OpenmdoModal: any) {
      this.modalService.open(OpenmdoModal);
    }
    editDbDetails(id:any){
      const editDataArray  = this.connectionList.filter((item: { database_id: number; }) => item.database_id == id);
      console.log(editDataArray)
      const editData = editDataArray[0] 
    this.postGreServerName =editData.hostname;
    this.postGrePortName = editData.port;
    this.postGreDatabaseName = editData.database;
    this.postGreUserName = editData.username;
    this.PostGrePassword = '';
    this.OracleServiceName = '';
    this.displayName = editData.display_name;
    this.databaseId=editData.database_id;
    this.databaseType = editData.database_type;
    }

    Openmdo(OpenmdoModal: any) {
      this.modalService.open(OpenmdoModal);
    }
    toggleVisibility1() {
      this.showPassword1 = !this.showPassword1;
      if (this.toggleClass1 === "off-line") {
        this.toggleClass1 = "line";
      } else {
        this.toggleClass1 = "off-line";
      }
    }
  ngOnInit(): void {
    {
      document.querySelector('html')?.getAttribute('data-toggled') != null
        ? document.querySelector('html')?.removeAttribute('data-toggled')
        : document
            .querySelector('html')
            ?.setAttribute('data-toggled', 'icon-overlay-close');    
    }
    if(this.viewDatasourceList){
   this.getDbConnectionList();
    }
  }

  pageChangegetconnectionList(page:any){
    this.pageNo=page;
    this.getDbConnectionList();
  }
  getDbConnectionList(){
    const Obj ={
      search : this.searchDbName,
      page_no:this.pageNo,
      page_count:this.itemsPerPage

    }
    if(Obj.search == '' || Obj.search == null){
      delete Obj.search;
    }
    if(Obj.page_count == undefined || Obj.page_count == null){
      delete Obj.page_count
    }
    this.workbechService.getdatabaseConnectionsList(Obj).subscribe({
      next:(data)=>{
        console.log(data);
        this.connectionList = data.sheets;
        this.itemsPerPage = data.items_per_page;
        this.totalItems = data.total_items
        console.log('connectionlist',data)
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
  getTablesFromConnectedDb(dbId:any,fileId:any){
    if(dbId === null){
    const encodedId = btoa(fileId.toString());
    this.router.navigate(['/workbench/database-connection/files/tables/'+encodedId]);
    }
    if(fileId === null){
      const encodedId = btoa(dbId.toString());
      this.router.navigate(['/workbench/database-connection/tables/'+encodedId]);
      }
}

  onDeleteItem(index: number) {
     this.draggedtables.splice(index, 1); // Remove the item from the droppedItems array
     console.log(this.draggedtables)
  }

  gotoNewConnections(){
  this.openPostgreSqlForm=false;
  this.viewNewDbs=true;
  this.openMySqlForm=false;
  this.openOracleForm = false;
  this.openMongoDbForm = false;
  this.openMicrosoftSqlServerForm = false;
  this.openSnowflakeServerForm = false;
  this.ibmDb2Form= false;
  this.sqlLiteForm = false;

  this.postGreServerName = '';
  this.postGrePortName = '';
  this.postGreDatabaseName = '';
  this.postGreUserName = '';
  this.PostGrePassword = '';
  this.OracleServiceName = '';
  this.displayName ='';
  }

  
}
