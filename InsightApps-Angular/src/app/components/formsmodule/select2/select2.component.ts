import { Component } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { NgSelectModule } from '@ng-select/ng-select';
import { SharedModule } from '../../../shared/sharedmodule';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { WorkbenchService } from '../../workbench/workbench.service';
import {
  CdkDragDrop,
  CdkDrag,
  CdkDropList,
  CdkDropListGroup,
  moveItemInArray,
  transferArrayItem,
} from '@angular/cdk/drag-drop';
@Component({
  selector: 'app-select2',
  standalone: true,
  imports: [SharedModule,NgSelectModule,NgbModule,FormsModule,ReactiveFormsModule,CdkDropListGroup, CdkDropList, CdkDrag],
  templateUrl: './select2.component.html',
  styleUrls: ['./select2.component.scss']
})
export class Select2Component {
  tableColumnsData = [] as any;
  draggedtables = [] as any;
  draggedColumns = [] as any;
  draggedRows = [] as any;
  dimentions = [] as any;
  measurments = [] as any;
  columnData = [] as any;
  rowData = [] as any;
  tableName: any;
  schemaName: any;
  draggedColumnsData = [] as any;
  draggedRowsData = [] as any;
  tablePreviewColumn = [] as any;
  tablePreviewRow = [] as any;
  rowdataPreview = [] as any;
 
  constructor(private workbechService:WorkbenchService){   
  }

  ngOnInit(): void {
    this.columnsData();
  }

  columnsData(){
    const obj={
      "db_id":"182",
      "queryset_id":"254",
  }
    this.workbechService.getColumnsData(obj).subscribe({next: (responce:any) => {
          console.log(responce);
          this.tableColumnsData = responce;
        },
        error: (error) => {
          console.log(error);
        }
      }
    )
  }

  dataExtraction(){
    this.tablePreviewColumn = [];
    this.tablePreviewRow = [];
    this.rowdataPreview = [];
      const obj={
          "database_id":182,
          "queryset_id":254,
          "col":this.draggedColumnsData,
          "row":this.draggedRowsData,
          "filter_id": [60]
      }
    this.workbechService.getDataExtraction(obj).subscribe({next: (responce:any) => {
          console.log(responce);
          this.tablePreviewColumn = responce.data[0].col;
          this.tablePreviewRow = responce.data[0].row;
          console.log(this.tablePreviewColumn);
          console.log(this.tablePreviewRow);
          this.tablePreviewRow.forEach((res:any) => {
          this.rowdataPreview.push(res.result_data);
          console.log(this.rowdataPreview)
        });
        },
        error: (error) => {
          console.log(error);
        }
      }
    )
  }
    drop(event: CdkDragDrop<string[]>) {
     // this.draggedtables = [];
     // this.draggedColumns = [];
   // if (event.previousContainer === event.container) {
   //   moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
    //} else {
      console.log('Transfering item to new container')
      // transferArrayItem(event.previousContainer.data,
      //                   event.container.data,
      //                   event.previousIndex,
      //                   event.currentIndex);
      //                   console.log('previouscont:'+event.previousContainer.data,
      //                   'eventcont:'+event.container.data)
      //                  console.log(event.previousContainer.data,'inex:'+event.currentIndex)


      let item: any = event.previousContainer.data[event.previousIndex];
      console.log('item' + JSON.stringify(item));
      let copy: any = JSON.parse(JSON.stringify(item));

      console.log('copy' + JSON.stringify(copy));
      let element: any = {};
      for (let attr in copy) {
        console.log('attr' + attr);
        if (attr == 'title') {
          element[attr] = copy[attr];
        } else {
          element[attr] = copy[attr];
        }
      }
      this.draggedtables.splice(event.currentIndex, 0, element);
      
      console.log(this.draggedtables);
    // }
    // this.columnsData();
    /* if(this.draggedtables.length > 1){
      const obj ={
        database_id : this.databaseId,
        tables : [[this.draggedtables[0].schema,this.draggedtables[0].table],[this.draggedtables[1].schema,this.draggedtables[1].table]]
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
     }*/
  }
  tableNameMethod(schemaname:any,tablename:any){
    this.schemaName = '';
    this.tableName = '';
  this.schemaName = schemaname;
  this.tableName = tablename;

  }
  columndrop(event: CdkDragDrop<string[]>){
    let item: any = event.previousContainer.data[event.previousIndex];
    let copy: any = JSON.parse(JSON.stringify(item));
    let element: any = {};
    for (let attr in copy) {
      if (attr == 'title') {
        element[attr] = copy[attr];
      } else {
        element[attr] = copy[attr];
      }
    }
    this.draggedColumns.splice(event.currentIndex, 0, element);
    this.draggedColumnsData.push([this.schemaName,this.tableName,element.column,element.data_type,""])
    this.dataExtraction();
  }
  rowdrop(event: CdkDragDrop<string[]>){
    let item: any = event.previousContainer.data[event.previousIndex];
    let copy: any = JSON.parse(JSON.stringify(item));
    let element: any = {};
    for (let attr in copy) {
      if (attr == 'title') {
        element[attr] = copy[attr];
      } else {
        element[attr] = copy[attr];
      }
    }
    this.draggedRows.splice(event.currentIndex, 0, element);
    this.draggedRowsData.push([this.schemaName,this.tableName,element.column,element.data_type,""])
    this.dataExtraction();
  }


  genders = [
    {id: 1,name: 'Texas'},
    {id: 2,name: 'Georgia'},
    {id: 3,name: 'California'},
    {id: 4,name: 'Washington D.C'},
    {id: 5,name: 'Virginia'},

  ];
  selectedGender = this.genders[1].name;
  selectedSimpleItem2 = 'Appple';
  cars1 = [
    { id: 1, name: 'Mango' },
    { id: 2, name: 'Orange' },
    { id: 3, name: 'Guava' },
    { id: 4, name: 'Pineapple' },
  ];
  templates = [
    {
      id: 1,
      name: 'Andrew',
      avatar: './assets/images/faces/select2/p-5.jpg',
      value:'p-1'
    },
    {
      id: 2,
      name: 'Maya',
      avatar: './assets/images/faces/select2/p-4.jpg',
      value:'p-2'
    },
    {
      id: 3,
      name: 'Brodus Axel',
      avatar: './assets/images/faces/select2/p-2.jpg',
      value:'p-3'
    },
    {
      id: 4,
      name: 'Goldens',
      avatar: './assets/images/faces/select2/p-1.jpg',
      value:'p-4'
    },
    {
      id: 5,
      name: 'Angelina',
      avatar: './assets/images/faces/select2/p-2.jpg',
      value:'p-5'
    },

  ];
  selectedTemplate = this.templates[1].name;
  simpleItems2: any = [];
  selectedCars2 = ['Andrew'];
  cars2 = [
    { id: 1, name: 'Maya' },
    { id: 2, name: 'Brodus Axel'},
    { id: 3, name: 'Goldhens' },
    { id: 4, name: 'Angelina' },
  ];

  selectedSimpleItem3= 'Selection-4';
  simpleItems3: any = [
    {id:1,name:'Selection-1'},
    {id:2,name:'Selection-2'},
    {id:3,name:'Selection-3'},
    {id:4,name:'Selection-4'}



  ];
  selectedmultiple=['Multiple-1']
  selectedCars3 = ['Selection-1'];
  cars3= [
    { id: 1, name: 'Selection-1' },
    { id: 2, name: 'Selection-2'},
    { id: 3, name: 'Selection-3' },
    { id: 4, name: 'Selection-4' },
  ];
  isCarsDisabled = false;
  enable() {
    this.isCarsDisabled = false;
  }
  disable(){
    this.isCarsDisabled = !this.isCarsDisabled;
  }
}
