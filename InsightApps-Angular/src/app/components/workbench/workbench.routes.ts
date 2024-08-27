import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { SharedModule } from '../../shared/sharedmodule';
import { PagesService } from '../pages/pages.service';
import { authGuard } from '../../auth.guard';

export const admin: Routes = [

  {path:'workbench',children:[ {
   path: 'work-bench/new-connections',
   canActivate:[authGuard],
   loadComponent: () =>
     import('./workbench/workbench.component').then((m) => m.WorkbenchComponent),
 },
 {
  path: 'work-bench/view-connections',
  loadComponent: () =>
    import('./workbench/workbench.component').then((m) => m.WorkbenchComponent),
},

//  {
//   path: 'database-connection/tables/:id',
//   canActivate:[authGuard],
//   loadComponent: () =>
//     import('./workbench/workbench.component').then((m) => m.WorkbenchComponent),
// },

{
  path: 'database-connection/tables/:id',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./database/database.component').then((m)=> m.DatabaseComponent)
},
{
  path: 'database-connection/files/tables/:id',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./database/database.component').then((m)=> m.DatabaseComponent)
},
{
  path: 'database-connection/sheets/fileId/:id1/:id2/:id3',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./database/database.component').then((m)=> m.DatabaseComponent)
},
{
  path: 'database-connection/sheets/dbId/:id1/:id2/:id3',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./database/database.component').then((m)=> m.DatabaseComponent)
},
{
  path: 'database-connection/savedQuery/fileId/:id1/:id2',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./database/database.component').then((m)=> m.DatabaseComponent)
},
{
  path: 'database-connection/savedQuery/dbId/:id1/:id2',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./database/database.component').then((m)=> m.DatabaseComponent)
},
{
  path: 'sheets/fileId/:id1/:id2/:id3',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./sheets/sheets.component').then((m)=> m.SheetsComponent)
},
{
  path: 'sheets/dbId/:id1/:id2/:id3',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./sheets/sheets.component').then((m)=> m.SheetsComponent)
},
{
  path: 'sheets',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./sheets/sheets.component').then((m)=> m.SheetsComponent)
},
{
  path: 'sheetsdashboard',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./sheetsdashboard/sheetsdashboard.component').then((m)=> m.SheetsdashboardComponent)
},
{
  path: 'sheetscomponent/sheetsdashboard/fileId/:id1/:id2',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./sheetsdashboard/sheetsdashboard.component').then((m)=> m.SheetsdashboardComponent),
   pathMatch: 'full',
},
{
  path: 'sheetscomponent/sheetsdashboard/dbId/:id1/:id2',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./sheetsdashboard/sheetsdashboard.component').then((m)=> m.SheetsdashboardComponent),
   pathMatch: 'full',
},
{
  path: 'landingpage/sheetsdashboard/:id1/:id2/:id3',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./sheetsdashboard/sheetsdashboard.component').then((m)=> m.SheetsdashboardComponent),
  pathMatch: 'full',
},{
  path: 'landingpage/sheetsdashboard/:id1',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./sheetsdashboard/sheetsdashboard.component').then((m)=> m.SheetsdashboardComponent),
  pathMatch: 'full',
},
{
  path: 'landingpage/sheets/:id1/:id2/:id3',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./sheets/sheets.component').then((m)=> m.SheetsComponent)
},

{
  path: 'landingpage/dbId/sheets/:id1/:id2/:id3',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./sheets/sheets.component').then((m)=> m.SheetsComponent)
},
{
  path: 'landingpage/fileId/sheets/:id1/:id2/:id3',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./sheets/sheets.component').then((m)=> m.SheetsComponent)
},

{
  path: 'landingpage',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./landingpage/landingpage.component').then((m)=> m.LandingpageComponent)
},
{
  path: 'dashboard-page',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./dashboard-page/dashboard-page.component').then((m)=> m.DashboardPageComponent)
},
{
  path: 'sheets-dashboard',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./sheets-list-page/sheets-list-page.component').then((m)=>m.SheetsListPageComponent)
},
{
  path: 'saved-queries',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./saved-queries/saved-queries.component').then((m)=>m.SavedQueriesComponent)
},
{
  path: 'list-users/dashboard',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./users-dashboard/users-dashboard.component').then((m)=> m.UsersDashboardComponent)
},
{
  path: 'dashboard/user-add',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./users-dashboard/users-dashboard.component').then((m)=> m.UsersDashboardComponent)
},
{
  path: 'roles-list/dashboard',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./roles-dashboard/roles-dashboard.component').then((m)=> m.RolesDashboardComponent)
},
{
  path: 'dashboard/role-add',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./roles-dashboard/roles-dashboard.component').then((m)=> m.RolesDashboardComponent)
},
{
  path: 'dashboard/role-edit/:id1',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./roles-dashboard/roles-dashboard.component').then((m)=> m.RolesDashboardComponent)
},
{
  path: 'sheetsdashboard/sheets/fileId/:id1/:id2/:id3/:id4',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./sheets/sheets.component').then((m)=> m.SheetsComponent)
},{
  path: 'sheetsdashboard/sheets/dbId/:id1/:id2/:id3/:id4',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./sheets/sheets.component').then((m)=> m.SheetsComponent)
},
{
  path: 'public/dashboard/:id1',
  loadComponent: () =>
    import('./sheetsdashboard/sheetsdashboard.component').then((m) => m.SheetsdashboardComponent),
},
{
  path: 'configure-page/configure',
  loadComponent: () =>
    import('./configure/configure.component').then((m) => m.ConfigureComponent),
},
 ]}
 ];

@NgModule({
  declarations: [],
  imports: [
    CommonModule,RouterModule.forChild(admin),
  ],
  exports:[RouterModule]
})
export class WorkbenchModule { 
  static routes = admin;


}
