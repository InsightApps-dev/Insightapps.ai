import { Component, ViewChild } from '@angular/core';
import { API, APIDefinition, Columns, Config, DefaultConfig, TableModule } from 'ngx-easy-table';
import { Company, data } from '../../../shared/data/tables_data/easy_table';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgxDatatableModule } from '@swimlane/ngx-datatable';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialModuleModule } from '../../../material-module/material-module.module';

@Component({
  selector: 'app-gridjs-tables',
  standalone: true,
  imports: [SharedModule,NgxDatatableModule,NgbModule,FormsModule,ReactiveFormsModule,MaterialModuleModule,TableModule],
  templateUrl: './gridjs-tables.component.html',
  styleUrl: './gridjs-tables.component.scss'
})
export class GridjsTablesComponent {
  public configuration!: Config;
  public columns!: Columns[];
  public data: Company[] = [];
  @ViewChild('table')
  table!: APIDefinition;

  // data: Company[] = [];
  // public configuration: Config;

  ngOnInit(): void {
    this.columns = [
      { key: 'level', title: 'Level' },
      { key: 'age', title: 'Age' },
      { key: 'company', title: 'Company' },
      { key: 'name', title: 'Name' },
      { key: 'isActive', title: 'STATUS' },
    ];

    this.data = data;
    this.configuration = { ...DefaultConfig };
  }

  private randNumber(min: number, max: number): number {
    return Math.floor(Math.random() * (max - min) + min);
  }

  addRow(): void {
    this.data = [
      ...this.data,
      {
        status: 'ACTIVE',
        amount: this.randNumber(1, 5),
        company: 'food',
        limit: this.randNumber(800, 1200),
        balance: this.randNumber(800, 3000),
      },
    ];
  }

  onChange(event: Event): void {
    this.table.apiEvent({
      type: API.onGlobalSearch,
      value: (event.target as HTMLInputElement).value,
    });
  }

  sortByLastName(asc: boolean): void {}

  sortByLevel(asc: boolean): void {}

  eventEmitted($event: { event: string; value: any }): void {}
}
