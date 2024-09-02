import { Component } from '@angular/core';
import { WorkbenchService } from '../workbench.service';
import { ActivatedRoute, Router } from '@angular/router';
import {
  CdkDragDrop,
  CdkDrag,
  CdkDropList,
  CdkDropListGroup,
  moveItemInArray,
  transferArrayItem,
} from '@angular/cdk/drag-drop';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgbModal, NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { FormsModule } from '@angular/forms';
import Swal from 'sweetalert2';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BrowserModule } from '@angular/platform-browser';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { CommonModule } from '@angular/common';
import { InsightsButtonComponent } from '../insights-button/insights-button.component';
import { tickStep } from 'd3';

@Component({
  selector: 'app-database',
  standalone: true,
  imports: [SharedModule,CdkDropListGroup, CdkDropList, CdkDrag,NgbModule,FormsModule,NgbModule,CommonModule,InsightsButtonComponent],
  templateUrl: './database.component.html',
  styleUrl: './database.component.scss',
  animations:[
    trigger('toggle', [
      state('open', style({
        width: '610px', // Adjust as needed
        // flex: '1 1 610px',
        opacity: 1,
      })),
      state('closed', style({
        width: '0px',
        opacity: 0,
        display: 'none'
      })),
      transition('open <=> closed', [
        animate('0.3s ease-in-out')
      ]),
    ])
  ]
})
export class DatabaseComponent {
  databaseName:any;
  tableName:any;
  selectedClmnT1:any;
  selectedClmnT2:any;
  getSelectedT1:any;
  getSelectedT2:any;
  selectedSchema1:any;
  selectedSchema2:any;
  selectedCndn:any;
  selectedJoin:any;
  selectedAliasT1:any;
  selectedAliasT2:any;
  tableRelationUi = true;
  custmT1Data = [] as any;
  custmT2Data = [] as any;
  connectionList =[] as any;
  tableList = [] as any;
  schematableList = [] as any;
  filteredSchematableList = [] as any;
  hostName:any;
  dragedTableName: any;
  databaseconnectionsList=true;
  draggedtables = [] as any;
  getTableColumns = [] as any;
  getTableRows = [] as any;
  relationOfTables = [] as any;
  displayJoiningCndnsList =[] as any;
  joinTypes = [] as any;
  databaseId:any;  
  fileId:any;
  sqlQuery ='';
  cutmquryTable = [] as any;
  TabledataJoining = [] as any;
  qryTime:any;
  qryRows:any;
  totalRows:any;
  showingRows:any;
  custmQryRows:any;
  custmQryTime:any;
  cutmquryTableError:any;
  showingRowsCustomQuery:any;
  totalRowsCustomQuery:any;
  remainingTables = [] as any;
  qurtySetId:any;
  enableJoinBtn = true;
  customSql = false;
  tableJoiningUI = true;
  isOpen = false;
  searchTables : any;
  columnsInFilters = [] as any;
  tableColumnFilter!:boolean;
  columnRowFilter!:any;
  datasourceFilterId:any;
  rows: any;
  titleMarkDirty: boolean = false;
  datasourceFilterIdArray:any[] =[];
  selectedRows = [];
  datasourceQuerysetId :string | null =null;
  filteredList = [] as any;
  editFilterList = [] as any;
  columnWithTablesData = [] as any;
  isAllSelected: boolean = false;
  saveQueryName = '';
  updateQuery=false;
  dataType:any;
  colName:any;
  fromDatabasId = false;
  fromFileId = false;
  rowLimit:any;
  gotoSheetButtonDisable = true;
  fromSavedQuery = false;
  fromSheetEditDb = false;

  constructor( private workbechService:WorkbenchService,private router:Router,private route:ActivatedRoute,private modalService: NgbModal){
    const currentUrl = this.router.url;
    if(currentUrl.includes('/workbench/database-connection/tables/')){
      this.fromDatabasId=true
      this.databaseId = +atob(route.snapshot.params['id']);
    }
    if(currentUrl.includes('/workbench/database-connection/files/tables/')){
      this.fromFileId=true;
      this.fileId = +atob(route.snapshot.params['id']);
     }
    if(currentUrl.includes('/workbench/database-connection/savedQuery/')){
      if(currentUrl.includes('/workbench/database-connection/savedQuery/fileId') && route.snapshot.params['id1'] && route.snapshot.params['id2'] ){
        this.fileId = +atob(route.snapshot.params['id1']);
        this.fromFileId = true;
        this.qurtySetId = +atob(route.snapshot.params['id2']);
        localStorage.setItem('QuerySetId', JSON.stringify(this.qurtySetId));
        this.getTablesFromFileId();
      }
      if (currentUrl.includes('/workbench/database-connection/savedQuery/dbId') && route.snapshot.params['id1'] && route.snapshot.params['id2'] ) {
        this.databaseId = +atob(route.snapshot.params['id1']);
        this.fromDatabasId = true;
        this.qurtySetId = +atob(route.snapshot.params['id2']);
        localStorage.setItem('QuerySetId', JSON.stringify(this.qurtySetId));
        this.getSchemaTablesFromConnectedDb();
        }
      this.customSql=true;
      this.tableJoiningUI=false;
      this.updateQuery=true;
      this.fromSavedQuery = true;
      this.getSavedQueryData();
     }
     if(currentUrl.includes('/workbench/database-connection/sheets/dbId')){
     if (route.snapshot.params['id1'] && route.snapshot.params['id2'] ) {
      this.databaseId = +atob(route.snapshot.params['id1']);
      this.qurtySetId = +atob(route.snapshot.params['id2']);
      localStorage.setItem('QuerySetId', JSON.stringify(this.qurtySetId));
      this.fromDatabasId = true;
      this.fromSheetEditDb = true;
      this.datasourceQuerysetId = atob(route.snapshot.params['id3'])
      if(this.datasourceQuerysetId==='null'){
        console.log('filterqrysetid',this.datasourceQuerysetId)
        this.datasourceQuerysetId = null
      }
      else{
          parseInt(this.datasourceQuerysetId)
          console.log(this.datasourceQuerysetId)
        }
      }
    }
    if(currentUrl.includes('/workbench/database-connection/sheets/fileId')){
      if (route.snapshot.params['id1'] && route.snapshot.params['id2'] ) {
       this.fileId = +atob(route.snapshot.params['id1']);
       this.qurtySetId = +atob(route.snapshot.params['id2']);
       localStorage.setItem('QuerySetId', JSON.stringify(this.qurtySetId));
       this.fromFileId = true;
       this.fromSheetEditDb = true;
       this.datasourceQuerysetId = atob(route.snapshot.params['id3'])
       if(this.datasourceQuerysetId==='null'){
         console.log('filterqrysetid',this.datasourceQuerysetId)
         this.datasourceQuerysetId = null
       }
       else{
           parseInt(this.datasourceQuerysetId)
           console.log(this.datasourceQuerysetId)
         }
       }
     }

  }
  ngOnInit(){
    // {
    //   document.querySelector('html')?.getAttribute('data-toggled') != null
    //     ? document.querySelector('html')?.removeAttribute('data-toggled')
    //     : document
    //         .querySelector('html')
    //         ?.setAttribute('data-toggled', 'icon-overlay-close');    
    // }

    if(!this.updateQuery && !this.fromSheetEditDb){
      if(this.fromDatabasId){
    // this.getTablesFromConnectedDb();
    this.getSchemaTablesFromConnectedDb();
      }
      if(this.fromFileId){
        this.getTablesFromFileId();
      }
    this.getTablesfromPrevious()
  }
  if(this.fromSheetEditDb){
    this.getTablesfromPrevious();
    if(this.fromFileId){
      this.getTablesFromFileId();
    }else if(this.fromDatabasId){
      this.getSchemaTablesFromConnectedDb();
    }
  }
  }
  toggleCard() {
    this.isOpen = !this.isOpen;
  }
  toggleSubMenu(menu: any) {
    menu.expanded = !menu.expanded;
  }
  getSavedQueryData(){
    const obj ={
      database_id:this.databaseId,
      queryset_id:this.qurtySetId
    }as any
    if(this.fromFileId){
      delete obj.database_id
      obj.file_id = this.fileId
    }
    this.workbechService.getSavedQueryData(obj).subscribe({
      next:(data:any)=>{
        console.log(data);
      this.sqlQuery=data.custom_query
      this.saveQueryName=data.query_name
      this.cutmquryTable = data
        this.custmQryTime = data.query_exection_time;
        this.custmQryRows = data.no_of_rows;
        this.showingRowsCustomQuery=data.no_of_rows
        this.totalRowsCustomQuery=data.total_rows;
        // if(this.fromSavedQuery){
        //   if(data.file_id === null)
        //   this.getSchemaTablesFromConnectedDb();
        // }else if(data.database_id === null){
        //   this.getTablesFromFileId();
        // }
      },
      error:(error:any)=>{
        console.log(error)
      }
    })
  }
  getTablesfromPrevious() {
    const querysetId = localStorage.getItem('QuerySetId') || 0;
    this.qurtySetId = querysetId
    if (querysetId !== 0) {
      const IdToPass = this.fromFileId ? this.fileId : this.databaseId
      this.workbechService.getTablesfromPrevious(IdToPass, querysetId).subscribe({
        next: (data) => {
          console.log(data);
          this.relationOfTables = data.dragged_data.relation_tables
          console.log('tablerelation', this.relationOfTables)
          this.draggedtables = data.dragged_data.json_data
          if (this.draggedtables.length > 0) {
            this.joiningTables();
          }
        },
        error: (error) => {
          console.log(error);
        }
      })
    }
  }
  getTablesFromFileId() {
    this.workbechService.getTablesFromFileId(this.fileId)
      .subscribe({
        next: (data) => {
          this.schematableList = data?.data?.schemas;
          // console.log('filteredscemas',this.filteredSchematableList)
          this.databaseName = data.filename;
          //  this.hostName = data.database.hostname;
          console.log(data)

        },
        error: (error) => {
          console.log(error);
        }
      })

  }
//   getTablesFromConnectedDb(){
//      this.workbechService.getTablesFromConnectedDb(this.databaseId).subscribe({next: (responce) => {
//     if(Array.isArray(responce.data)){
//       this.tableList= responce.data
//     }
//     else{
//     this.tableList = this.combineArrays(responce.data)
//     }
//     console.log('tablelist',this.tableList)
//     // this.databaseName = responce.database.database_name
//     this.databaseId = responce.database.database_id
//   },
//   error:(error)=>{
//     console.log(error);
//   }
// })
// }
getSchemaTablesFromConnectedDb(){
  const obj ={
    search:this.searchTables,
    querySetId:this.qurtySetId
  }
  if(obj.search == '' || obj.search == null){
    delete obj.search;
  }
  if(obj.querySetId === '0' || obj.querySetId === 0){
    delete obj.querySetId
  }
  const IdToPass = this.fromFileId ? this.fileId : this.databaseId
  this.workbechService.getSchemaTablesFromConnectedDb(IdToPass,obj).subscribe({next: (data) => {
   this.schematableList= data?.data?.schemas;
  //  this.filteredSchematableList = this.schematableList?.data?.schemas
   console.log('filteredscemas',this.filteredSchematableList)
       this.databaseName = data.database.database;
        this.hostName = data.database.hostname;
        this.saveQueryName = data.queryset_name;
    console.log(data)

},
error:(error)=>{
 console.log(error);
}
})
}
//filter tables from schemas
filterTables(){
  if (Array.isArray(this.schematableList)) {
    const filteredSchemas = this.schematableList.map((schemaObj: { schema: any; tables: any[] }) => {
      return {
        schema: schemaObj.schema,
        tables: schemaObj.tables.filter(tableObj => tableObj.table.includes(this.searchTables))
      };
    }).filter((schemaObj: { tables: string | any[]; }) => schemaObj.tables.length > 0); // Filter out schemas with no matching tables
  
    if (filteredSchemas.length > 0) {
      console.log('Filtered data:', filteredSchemas);
      this.schematableList = filteredSchemas
    } else {
      console.log('No matching tables found');
    }
  } else {
    console.log('Something went wrong');
  }
}

private combineArrays(arraysOfObjects: { data: any[] }[]): any[]{
  let result: any[] = [];
for (const obj of arraysOfObjects) {
  if (Array.isArray(obj.data)) {
    result = result.concat(obj.data);
  }
}
return result;
}
drop(event: CdkDragDrop<string[]>) {
  if (event.previousContainer === event.container) {
    moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
  } else {
    console.log('Transfering item to new container')
    let item: any = event.previousContainer.data[event.previousIndex];
    // console.log('item' + JSON.stringify(item));
    let copy: any = JSON.parse(JSON.stringify(item));
    // console.log('copy' + JSON.stringify(copy));
    let element: any = {};
    for (let attr in copy) {
      // console.log('attr' + attr);
      if (attr == 'title') {
        element[attr] = copy[attr];
      } else {
        element[attr] = copy[attr];
      }
    }
   // this.draggedtables.splice(event.currentIndex, 0, element);
   //this.draggedtables.push(element);
   console.log('element',element)
    this.pushToDraggedTables(element)
    console.log('darggedtable',this.draggedtables)
   }
   if(parseInt(this.qurtySetId) !== 0){
    this.joiningTables();
   }
   else if(parseInt(this.qurtySetId) === 0){
     this.joiningTablesWithoutQuerySetId()
   }
}

pushToDraggedTables(newTable:any): void {

  const existingTableNames = this.draggedtables.map((table: { table: any; }) => table.table);
  const baseTableName = newTable.table
  const occurrences = existingTableNames.filter((name: string) => name.startsWith(baseTableName)).length;
  let tableName = newTable.table;
  let suffix = occurrences;
    while (existingTableNames.includes(tableName)) {
      tableName = `${newTable.table}_${suffix}`;
      suffix++;
    }
    newTable['alias']=tableName;
    this.draggedtables.push(newTable);
}

getTablerowclms(table:any,schema:any){
  const obj ={
    database_id:this.databaseId,
    tables:[[schema,table]]
  }
  this.workbechService.getTableData(obj).subscribe({
    next:(data:any)=>{
      console.log(data);
      this.getTableColumns = data.column_data;
      this.getTableRows = data.row_data;
      this.tableName = data?.column_data[0]?.table
    },
    error:(error:any)=>{
      console.log(error)
    }
  })
}
// getTableData(){
//   const obj ={
//     database_id:this.databaseId,
//     tables:[[this.draggedtables[0].schema,this.draggedtables[0].table]]
//   }
//   this.workbechService.getTableData(obj).subscribe({
//     next:(data:any)=>{
//       console.log('single table data',data);
//       this.cutmquryTable = data
//       this.qryTime = data.query_exection_time;
//       this.qryRows = data.no_of_rows;
//     },
//     error:(error:any)=>{
//       console.log(error)
//     }
//   })
// }

onDeleteItem(index: number) {
   this.draggedtables.splice(index, 1); // Remove the item from the droppedItems array
   console.log(this.draggedtables);
  //  const schema = this.draggedtables[index].schema
  //  const tablename = this.draggedtables[index].table
  //  const tablealias = this.draggedtables[index].alias


  //  if(this.draggedtables.length !== 0){
    const deleteIndex = index - 1
    this.relationOfTables.splice(deleteIndex,1)
   this.joiningTablesFromDelete();
   this.isOpen = false;
  //  }
}
buildCustomRelation(){
  const parts = this.selectedClmnT1.split('(');
  this.selectedClmnT1 = parts[0].trim()
  const parst = this.selectedClmnT2.split('(');
  this.selectedClmnT2 = parst[0].trim()
  const obj ={
    database_id:this.databaseId,
    tables : [[this.draggedtables[0].schema,this.draggedtables[0].table],[this.draggedtables[1].schema,this.draggedtables[1].table]],
    condition:[[this.draggedtables[0].schema+'.'+this.draggedtables[0].table+'.'+this.selectedClmnT1 +'=' +this.draggedtables[1].schema+'.'+this.draggedtables[1].table+'.'+this.selectedClmnT2]]
  }
  this.workbechService.tableRelation(obj)
    .subscribe(
      {
        next:(data:any) =>{
          console.log(data)
          this.relationOfTables = data[2]?.relation?.condition
          console.log('relation',this.relationOfTables)
        },
        error:(error:any)=>{
        console.log(error)
      }
      })

}
clrQuery(){
  this.sqlQuery = ''
  this.cutmquryTable=[];
  this.custmQryTime='';
  this.custmQryRows='';
}
executeQuery(){
  const obj ={
    database_id: this.databaseId,
    custom_query: this.sqlQuery,
    row_limit:this.rowLimit,
    queryset_id:this.qurtySetId
  }as any
  if(this.fromFileId){
    delete obj.database_id
    obj.file_id = this.fileId
  }
  this.workbechService.executeQuery(obj)
  .subscribe(
    {
      next:(data:any) =>{
        console.log(data)
        // this.relationOfTables = data[2]?.relation?.condition
        // console.log('relation',this.relationOfTables)
        this.cutmquryTable = data
        this.custmQryTime = data.query_exection_time;
        this.custmQryRows = data.no_of_rows;
        this.qurtySetId = data.query_set_id;
        this.showingRowsCustomQuery=data.no_of_rows
        this.totalRowsCustomQuery=data.total_rows
        console.log('dkjshd',this.cutmquryTable)
      },
      error:(error:any)=>{
      console.log(error);
      Swal.fire({
        icon: 'error',
        title: 'oops!',
        text: error.error.message,
        width: '400px',
      })
      this.cutmquryTableError = error;
    }
    })
}

updateRemainingTables() {
  this.remainingTables = this.draggedtables.filter((table: { alias: string; }) => table.alias !== this.selectedAliasT1);
  this.selectedAliasT2 = this.remainingTables.length > 0 ? this.remainingTables[0].alias : '';
}

joiningTablesWithoutQuerySetId(){
  const schemaTablePairs = this.draggedtables.map((item: { schema: any; table: any; alias:any }) => [item.schema, item.table, item.alias]);
  // console.log(schemaTablePairs)
  const obj ={
    query_set_id:null,
    database_id:this.databaseId,
    joining_tables: schemaTablePairs,
    join_type:[],
    joining_conditions:[],
    dragged_array:this.draggedtables,
  } as any
  if(this.fromFileId){
    delete obj.database_id
    obj.file_id = this.fileId
  }
  this.workbechService.joiningTables(obj)
  .subscribe(
    {
      next:(data:any) =>{
        console.log(data)
        this.relationOfTables = data.table_columns_and_rows?.joining_condition;
        this.displayJoiningCndnsList = data.table_columns_and_rows?.joining_condition_list;
        this.qurtySetId = data?.table_columns_and_rows?.query_set_id
        localStorage.setItem('QuerySetId', JSON.stringify(this.qurtySetId));
        this.joinTypes = data?.table_columns_and_rows?.join_types        
        console.log('joining',data)
        console.log('relation',this.relationOfTables);
        this.getJoiningTableData();
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
joiningTables(){
  const schemaTablePairs = this.draggedtables.map((item: { schema: any; table: any; alias:any }) => [item.schema, item.table, item.alias]);
   console.log(schemaTablePairs)
   this.relationOfTables.push([])
  const obj ={
    query_set_id:this.qurtySetId,
    database_id:this.databaseId,
    joining_tables: schemaTablePairs,
    join_type:this.joinTypes,
    joining_conditions:this.relationOfTables,
    dragged_array:this.draggedtables
  }as any;
  if(this.fromFileId){
    delete obj.database_id;
    obj.file_id=this.fileId
  }
  this.workbechService.joiningTables(obj)
  .subscribe(
    {
      next:(data:any) =>{
        console.log(data)
        this.relationOfTables = data.table_columns_and_rows?.joining_condition;
        this.displayJoiningCndnsList = data.table_columns_and_rows?.joining_condition_list;
        this.qurtySetId = data?.table_columns_and_rows?.query_set_id
        this.joinTypes = data?.table_columns_and_rows?.join_types        
        console.log('joining',data)
        console.log('relation',this.relationOfTables);
        this.getJoiningTableData();
        this.gotoSheetButtonDisable = false;
      },
      error:(error:any)=>{
      console.log(error);
      Swal.fire({
        icon: 'error',
        title: 'oops!',
        text: error.error.message,
        width: '400px',
      });
      this.TabledataJoining = [];
      this.qryTime = '';
      this.qryRows ='';
      this.totalRows = '';
      this.showingRows = '';
      this.gotoSheetButtonDisable= true
    }
    })
  
  // else if(schemaTablePairs.length > 2){
  //   const obj ={
  //     query_set_id:this.qurtySetId,
  //     database_id:this.databaseId,
  //     joining_tables: schemaTablePairs,
  //     join_type:[],
  //     joining_conditions:[]
  //   }
  //   this.workbechService.joiningTables(obj)
  //   .subscribe(
  //     {
  //       next:(data:any) =>{
  //         console.log(data)
  //         this.relationOfTables = data.table_columns_and_rows?.joining_condition;
  //         this.displayJoiningCndnsList = data.table_columns_and_rows?.joining_condition_list;
  //         console.log('relation',this.relationOfTables);
  //         this.getJoiningTableData();
  //       },
  //       error:(error:any)=>{
  //       console.log(error)
  //     }
  //     })
  // }
}
joiningTablesFromDelete(){
  const schemaTablePairs = this.draggedtables.map((item: { schema: any; table: any; alias:any }) => [item.schema, item.table, item.alias]);
   console.log(schemaTablePairs)
  const obj ={
    query_set_id:this.qurtySetId,
    database_id:this.databaseId,
    joining_tables: schemaTablePairs,
    join_type:[],
    joining_conditions:this.relationOfTables,
    dragged_array:this.draggedtables
  }as any;
  if(this.fromFileId){
    delete obj.database_id;
    obj.file_id=this.fileId
  }
  this.workbechService.joiningTables(obj)
  .subscribe(
    {
      next:(data:any) =>{
        console.log(data)
        this.relationOfTables = data.table_columns_and_rows?.joining_condition;
        this.displayJoiningCndnsList = data.table_columns_and_rows?.joining_condition_list;
        this.qurtySetId = data?.table_columns_and_rows?.query_set_id
        if(this.qurtySetId === 0){
          localStorage.setItem('QuerySetId','0');
          this.datasourceQuerysetId = null;
        }
        this.joinTypes = data?.table_columns_and_rows?.join_types        
        console.log('joining',data)
        console.log('relation',this.relationOfTables);
        this.getJoiningTableData();
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
customTableJoin(){
  const schemaTablePairs = this.draggedtables.map((item: { schema: any; table: any;alias:any }) => [item.schema, item.table, item.alias]);
  console.log(schemaTablePairs)
  const t1Index = this.draggedtables.findIndex((x: { alias: any; }) => x.alias === this.selectedAliasT1)
  const t2Index = this.draggedtables.findIndex((x: { alias: any; }) => x.alias === this.selectedAliasT2)

  console.log('indexoftable1',t1Index);
   console.log('indexoftable2',t2Index);
  const customJoinCndn = '"'+this.selectedAliasT1+'"."'+this.selectedClmnT1+'" '+this.selectedCndn+' "'+this.selectedAliasT2+'"."'+this.selectedClmnT2+'"'
   const MaxInex = Math.max(t1Index,t2Index);
  console.log('custcon',customJoinCndn, 'maxind',MaxInex)
  if (!this.relationOfTables[MaxInex - 1]) {
    this.relationOfTables[MaxInex - 1] = [];
  }
  this.relationOfTables[MaxInex - 1].push(customJoinCndn)
  console.log('customrelation',this.relationOfTables)
  this.joinTypes[MaxInex - 1] = this.selectedJoin
  console.log(this.joinTypes)
  if(schemaTablePairs.length >= 2){
  const obj ={
    query_set_id:this.qurtySetId,
    database_id:this.databaseId,
    joining_tables: schemaTablePairs,
    join_type:this.joinTypes,
    joining_conditions:this.relationOfTables,
    dragged_array:this.draggedtables

  }as any;
  if(this.fromFileId){
   delete obj.database_id;
   obj.file_id = this.fileId
  }
  this.workbechService.joiningTables(obj)
  .subscribe(
    {
      next:(data:any) =>{
        console.log(data)
        this.relationOfTables = data.table_columns_and_rows?.joining_condition;
        this.displayJoiningCndnsList = data.table_columns_and_rows?.joining_condition_list;
        this.qurtySetId = data?.table_columns_and_rows?.query_set_id;       
        console.log('joining',data)
        console.log('relation',this.relationOfTables);
        this.getJoiningTableData();
        this.clearJoinCondns();
      },
      error:(error:any)=>{
      console.log(error);
      Swal.fire({
        icon: 'error',
        title: 'oops!',
        text: error.error.message,
        width: '400px',
      })
      this.relationOfTables.pop();
    }
    })
  }
}

// populateDropdown() {
//   const dropdownMenu = document.getElementById('dropdownMenu');
//   const selectedTableDiv = document.getElementById('selectedTable');

//   if(dropdownMenu){
//     dropdownMenu.innerHTML = '';
//   this.draggedtables.forEach((tableData: { schema: any; table: any; columns: any[]; }) => {
//     // Add table name as header
//     const tableHeader = document.createElement('li');
//     tableHeader.className = 'dropdown-header';
//     tableHeader.textContent = `${tableData.schema}.${tableData.table}`;
//     dropdownMenu.appendChild(tableHeader);

//     // Add columns
//     tableData.columns.forEach(column => {
//       console.log("Column:", column.columns); //
//       const columnItem = document.createElement('li');
//       columnItem.textContent = `${column.columns} (${column.datatypes})`;
//       columnItem.onclick = function() {
//         // Handle column selection
//         selectedTableDiv!.innerHTML = `${tableData.schema}<br>${tableData.table}`;
//         const dropdownButton = document.getElementById('dropdownMenuButton');
//         dropdownButton!.textContent = `${column.columns}`;
//         console.log("Selected column:", column.columns, "Table:", tableData.table, "Schema:", tableData.schema);
//       };
//       dropdownMenu.appendChild(columnItem);
//     });

//     // Add divider
//     const divider = document.createElement('li');
//     divider.className = 'divider';
//     dropdownMenu.appendChild(divider);
//   });
// }else{
//   console.log('erriieor')
// }
// this.enableJoinButton();
// }
// s

enableJoinButton(){

if( this.selectedJoin && this.selectedCndn)
  {
    this.enableJoinBtn = false;
  }else {
    this.enableJoinBtn = true;
  }
  
}
clearJoinCondns(){
 
  this.selectedJoin ='Condition';
  this.selectedCndn ='Operator';
  this.selectedClmnT1=null
  this.selectedClmnT2=null;
  this.enableJoinButton();
}

getJoiningTableData(){
  const obj ={
    database_id:this.databaseId,
    query_id:this.qurtySetId,
    datasource_queryset_id:this.datasourceQuerysetId,
    row_limit:this.rowLimit
  } as any
  if(this.fromFileId){
    delete obj.database_id
    obj.file_id=this.fileId
  }
  this.workbechService.getTableJoiningData(obj).subscribe(
    {
      next:(data:any) =>{
        console.log('qury_data/tablejoined_data',data)
        this.TabledataJoining = data;
        this.qryTime = data.query_exection_time;
        this.qryRows = data.no_of_rows;
        this.totalRows = data.total_rows;
        this.showingRows = data.no_of_rows;
        this.gotoSheetButtonDisable = false;
        this.saveQueryName = data.queryset_name;
        if(this.TabledataJoining?.column_data?.length === 0){
          this.gotoSheetButtonDisable = true;
        }
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
deleteJoiningRelation(index:number){

  const deleteCondtin = this.displayJoiningCndnsList[index]
  console.log(deleteCondtin)
  this.relationOfTables = this.relationOfTables.map((subArray: any[]) =>
    subArray.filter(item => item !== deleteCondtin)
  ).filter((subArray: string | any[]) => subArray.length > 0);
  console.log('deletedcondfromrelatiion',this.relationOfTables)

  if (index > -1 && index < this.displayJoiningCndnsList.length) {
    this.displayJoiningCndnsList.splice(index, 1);
    //this.relationOfTables.splice(index,1);
  }
  this.deleteRelation(deleteCondtin)
  
  // console.log('removedjoining',this.displayJoiningCndnsList)
}
deleteRelation(deleteCondtin:any){
  const obj ={
    conditions_list:this.relationOfTables,
    delete_condition :deleteCondtin[0],
    
  }
  this.workbechService.deleteRelation(obj).subscribe(
    {
      next:(data:any) =>{
        console.log(data)
       this.relationOfTables= data.data.conditions_list;
       this.joiningTables();
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
openSuperScaled(modal: any) {
  this.modalService.open(modal, {
    centered: true,
    windowClass: 'animate__animated animate__zoomIn',
  });
  this.tableColumnFilter = true;
  this.columnRowFilter = false;
}
openSuperScaledGetColunmns(modal: any){
  this.modalService.open(modal, {
    centered: true,
    windowClass: 'animate__animated animate__zoomIn',
  });
  this.tableColumnFilter = true;
  this.columnRowFilter = false;
  this.callColumnWithTable();

}
openRowsData(modal: any) {
  this.modalService.open(modal, {
    centered: true,
    windowClass: 'animate__animated animate__zoomIn',
  });
}
callColumnWithTable(){
  const obj ={
    database_id:this.databaseId,
    query_set_id :this.qurtySetId,
    type_of_filter:'datasource'
  }as any;
  if(this.fromFileId){
    delete obj.database_id
    obj.file_id = this.fileId
  }
  this.workbechService.callColumnWithTable(obj).subscribe(
    {
      next:(data:any) =>{
        console.log(data)
       this.columnWithTablesData= data
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
selectedColumnGetRows(col:any,datatype:any){
  const obj ={
    database_id:this.databaseId,
    query_set_id:this.qurtySetId,
    datasource_queryset_id:this.datasourceQuerysetId,
    type_of_filter:'datasource',
    col_name:col,
    data_type:datatype,
  }as any;
  if(this.fromFileId){
    delete obj.database_id
    obj.file_id = this.fileId
  }
  this.colName = col;
  this.dataType = datatype;
  this.workbechService.selectedColumnGetRows(obj).subscribe(
    {
      next:(data:any) =>{
        console.log(data)
        this.columnsInFilters= data.col_data.map((item: any) => ({ label: item, selected: false }))
        // this.datasourceFilterId=data.filter_id;
        // this.datasourceFilterIdArray.push(data.filter_id);
        this.tableColumnFilter =false;
        this.columnRowFilter = true;
        console.log('colmnfilterrows',this.columnsInFilters)
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
updateSelectedRows() {
  this.selectedRows = this.columnsInFilters
    .filter((row: { selected: any; }) => row.selected)
    .map((row: { label: any; }) => row.label);
  console.log('selected rows', this.selectedRows);

  this.isAllSelected = this.columnsInFilters.every((row: { selected: any; }) => row.selected);
}

toggleAllRows(event: Event) {
  const isChecked = (event.target as HTMLInputElement).checked;
  this.columnsInFilters.forEach((row: { selected: boolean; }) => row.selected = isChecked);
  this.updateSelectedRows();
}
isAnyRowSelected(): boolean {
  return this.columnsInFilters.some((row: { selected: any; }) => row.selected);
}
getSelectedRows() {
  this.selectedRows = this.columnsInFilters
  .filter((row: { selected: any; }) => row.selected)
  .map((row: { label: any; }) => row.label);
  console.log('selected rows',this.selectedRows);

  const obj = {
    filter_id:null,
    database_id:this.databaseId,
    queryset_id:this.qurtySetId,
    type_of_filter:'datasource',
    datasource_querysetid:null,
    select_values:this.selectedRows,
    range_values:null,
    col_name:this.colName,
    data_type:this.dataType,
  }as any;
  if(this.fromFileId){
    delete obj.database_id
    obj.file_id = this.fileId
  }

  this.workbechService.getSelectedRowsFilter(obj).subscribe(
    {
      next:(data:any) =>{
        console.log(data)
        this.datasourceFilterId = data.filter_id;
         this.datasourceFilterIdArray.push(data.filter_id);
        this.getDsQuerysetId();
        this.modalService.dismissAll('close')
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
getDsQuerysetId(){
  const obj ={
    datasource_queryset_id:this.datasourceQuerysetId,
    queryset_id:this.qurtySetId,
    filter_id:this.datasourceFilterIdArray,
    database_id:this.databaseId
  }as any;
  if(this.fromFileId){
    delete obj.database_id
    obj.file_id = this.fileId
  }
  this.workbechService.getDsQuerysetId(obj).subscribe(
    {
      next:(data:any) =>{
        console.log(data)
        this.datasourceQuerysetId = data.data.datasource_queryset_id;
        if(this.tableJoiningUI){
        this.getJoiningTableData();
        }
        if(this.customSql){
          this.getfilteredCustomSqlData();
        }
        this.getFilteredList();
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
getFilteredList(){
  const obj ={
    query_set_id:this.qurtySetId,
    database_id:this.databaseId,
    type_of_filter:'datasource'
  }as any
  if(this.fromFileId){
    delete obj.database_id
    obj.file_id = this.fileId
  }
  this.workbechService.getFilteredList(obj).subscribe(
    {
      next:(data:any) =>{
        console.log(data)
        this.filteredList = data.filters_data;
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
editFilter(id:any){
  const obj ={
    type_filter:'datasource',
    database_id:this.databaseId,
    filter_id:id
  }as any;
  if(this.fromFileId){
    delete obj.database_id
    obj.file_id = this.fileId
  }
  this.workbechService.editFilter(obj).subscribe(
    {
      next:(data:any) =>{
        console.log(data)
        this.editFilterList = data.result;
        this.colName=data.column_name,
        this.dataType = data.data_type
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
deleteFilter(id:any){
  this.modalService.dismissAll('close')
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
  this.workbechService.deleteFilter(id).subscribe(
    {
      next:(data:any) =>{
        console.log(data)
        if(data){
          Swal.fire({
            icon: 'success',
            title: 'Removed!',
            text: ' Filter Removed Successfully',
            width: '400px',
          })

        }
        console.log('filter ids',this.datasourceFilterIdArray)
        this.datasourceFilterIdArray = this.datasourceFilterIdArray.filter(item => item !== id);
        if(this.datasourceFilterIdArray.length === 0){
          this.datasourceFilterId = null;
        }
        this.getDsQuerysetId()
        this.getFilteredList();
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
  }})


}

updateEditSelectedRows() {
  this.selectedRows = this.editFilterList
    .filter((row: { selected: any; }) => row.selected)
    .map((row: { label: any; }) => row.label);
  console.log('selected rows', this.selectedRows);

  this.isAllSelected = this.editFilterList.every((row: { selected: any; }) => row.selected);
}

toggleEditAllRows(event: Event) {
  const isChecked = (event.target as HTMLInputElement).checked;
  this.editFilterList.forEach((row: { selected: boolean; }) => row.selected = isChecked);
  this.updateEditSelectedRows();
}
isAnyEditRowSelected(): boolean {
  return this.editFilterList.some((row: { selected: any; }) => row.selected);
}
getSelectedRowsFromEdit() {
  this.selectedRows = this.editFilterList
  .filter((row: { selected: any; }) => row.selected)
  .map((row: { label: any; }) => row.label);
  console.log('selected rows',this.selectedRows);

  const obj = {
    filter_id:this.datasourceFilterId,
    database_id:this.databaseId,
    queryset_id:this.qurtySetId,
    type_of_filter:'datasource',
    datasource_querysetid:null,
    select_values:this.selectedRows,
    range_values:null,
    col_name:this.colName,
    data_type:this.dataType
  }as any;
  if(this.fromFileId){
    delete obj.database_id
    obj.file_id = this.fileId
  }
  this.workbechService.getSelectedRowsFilter(obj).subscribe(
    {
      next:(data:any) =>{
        console.log(data)
        this.datasourceFilterId = data.filter_id;
        this.getDsQuerysetId();
         this.modalService.dismissAll('close')
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
getfilteredCustomSqlData(){
    const obj ={
      database_id:this.databaseId,
      query_id:this.qurtySetId,
      datasource_queryset_id:this.datasourceQuerysetId
    }
    this.workbechService.getTableJoiningData(obj).subscribe(
      {
        next:(data:any) =>{
          console.log('qury_data/tablejoined_data',data)
          this.cutmquryTable = data;
          this.custmQryTime = data.query_exection_time;
          this.custmQryRows = data.no_of_rows;
          this.saveQueryName = data.queryset_name;
          this.showingRowsCustomQuery=data.no_of_rows
          this.totalRowsCustomQuery=data.total_rows
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
goToConnections(){
  this.router.navigate(['/workbench/work-bench/view-connections'])
}

markDirty(){
  this.titleMarkDirty = true;
}

  goToSheet() {
    if (this.saveQueryName === '' || this.saveQueryName == null || this.saveQueryName == undefined) {
      Swal.fire({
        icon: 'error',
        title: 'oops!',
        text: 'Please enter title to save',
        width: '400px',
      })
    } else {
      if (this.fromFileId) {
        const encodedFileId = btoa(this.fileId.toString());
        const encodedQuerySetId = btoa(this.qurtySetId.toString());
        if (this.datasourceQuerysetId === null || this.datasourceQuerysetId === undefined) {
          // Encode 'null' to represent a null value
          const encodedDsQuerySetId = btoa('null');
          if (this.titleMarkDirty) {
            let payload = { file_id: this.fileId, query_set_id: this.qurtySetId, query_name: this.saveQueryName }
            this.workbechService.updateQuerySetTitle(payload).subscribe({
              next: (data: any) => {
                this.router.navigate(['/workbench/sheets/fileId' + '/' + encodedFileId + '/' + encodedQuerySetId + '/' + encodedDsQuerySetId])
              },
              error: (error: any) => {
                console.log(error);
                Swal.fire({
                  icon: 'error',
                  title: 'oops!',
                  text: error.error.message,
                  width: '400px',
                })
              }
            });
          } else {
            this.router.navigate(['/workbench/sheets/fileId' + '/' + encodedFileId + '/' + encodedQuerySetId + '/' + encodedDsQuerySetId])
          }
        } else {
          // Convert to string and encode
          const encodedDsQuerySetId = btoa(this.datasourceQuerysetId.toString());
          if (this.titleMarkDirty) {
            let payload = { database_id: this.databaseId, query_set_id: this.qurtySetId, query_name: this.saveQueryName }
            this.workbechService.updateQuerySetTitle(payload).subscribe({
              next: (data: any) => {
                this.router.navigate(['/workbench/sheets/fileId' + '/' + encodedFileId + '/' + encodedQuerySetId + '/' + encodedDsQuerySetId])
              },
              error: (error: any) => {
                console.log(error);
                Swal.fire({
                  icon: 'error',
                  title: 'oops!',
                  text: error.error.message,
                  width: '400px',
                })
              }
            });
          } else {
            this.router.navigate(['/workbench/sheets/fileId' + '/' + encodedFileId + '/' + encodedQuerySetId + '/' + encodedDsQuerySetId])
          }
        }
      } else if (this.fromDatabasId) {
        const encodedDatabaseId = btoa(this.databaseId.toString());
        const encodedQuerySetId = btoa(this.qurtySetId.toString());
        if (this.datasourceQuerysetId === null || this.datasourceQuerysetId === undefined) {
          // Encode 'null' to represent a null value
          const encodedDsQuerySetId = btoa('null');
          if (this.titleMarkDirty) {
            let payload = { database_id: this.databaseId, query_set_id: this.qurtySetId, query_name: this.saveQueryName }
            this.workbechService.updateQuerySetTitle(payload).subscribe({
              next: (data: any) => {
                this.router.navigate(['/workbench/sheets/dbId' + '/' + encodedDatabaseId + '/' + encodedQuerySetId + '/' + encodedDsQuerySetId])
              },
              error: (error: any) => {
                console.log(error);
                Swal.fire({
                  icon: 'error',
                  title: 'oops!',
                  text: error.error.message,
                  width: '400px',
                })
              }
            });
          } else {
            this.router.navigate(['/workbench/sheets/dbId' + '/' + encodedDatabaseId + '/' + encodedQuerySetId + '/' + encodedDsQuerySetId])
          }
        } else {
          // Convert to string and encode
          const encodedDsQuerySetId = btoa(this.datasourceQuerysetId.toString());
          if (this.titleMarkDirty) {
            let payload = { database_id: this.databaseId, query_set_id: this.qurtySetId, query_name: this.saveQueryName }
            this.workbechService.updateQuerySetTitle(payload).subscribe({
              next: (data: any) => {
                this.router.navigate(['/workbench/sheets/dbId' + '/' + encodedDatabaseId + '/' + encodedQuerySetId + '/' + encodedDsQuerySetId])
              },
              error: (error: any) => {
                console.log(error);
                Swal.fire({
                  icon: 'error',
                  title: 'oops!',
                  text: error.error.message,
                  width: '400px',
                })
              }
            });
          } else {
            this.router.navigate(['/workbench/sheets/dbId' + '/' + encodedDatabaseId + '/' + encodedQuerySetId + '/' + encodedDsQuerySetId])
          }
        }
      }
    }
  }

saveQuery(){
  if(this.saveQueryName === ''){
    Swal.fire({
      icon: 'error',
      title: 'oops!',
      text: 'Please enter name to save query',
      width: '400px',
    })
  }else{
  const obj ={
    
    database_id:this.databaseId,
    query_set_id:this.qurtySetId,
    query_name:this.saveQueryName,
    custom_query:this.sqlQuery
  }
  this.workbechService.saveQueryName(obj).subscribe(
    {
      next:(data:any) =>{
        console.log(data)
        if(data){
          Swal.fire({
            icon: 'success',
            title: 'Done!',
            text: 'Query Saved Successfully',
            width: '400px',
          })
        }
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
}
updateCustmQuery(){
  if(this.saveQueryName === ''){
    Swal.fire({
      icon: 'error',
      title: 'oops!',
      text: 'Please enter name to save query',
      width: '400px',
    })
  }else{
  const obj ={
    database_id:this.databaseId,
    queryset_id:this.qurtySetId,
    query_name:this.saveQueryName,
    custom_query:this.sqlQuery
  }as any
  if(this.fromFileId){
    delete obj.database_id
    obj.file_id = this.fileId
  }
  this.workbechService.updateCustmQuery(obj).subscribe({
    next:(data:any)=>{
      console.log(data);
    this.sqlQuery=data.custom_query
    this.saveQueryName=data.query_name
    this.cutmquryTable = data
      this.custmQryTime = data.query_exection_time;
      this.custmQryRows = data.no_of_rows;
      this.showingRowsCustomQuery=data.no_of_rows
      this.totalRowsCustomQuery=data.total_rows
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
}

}
