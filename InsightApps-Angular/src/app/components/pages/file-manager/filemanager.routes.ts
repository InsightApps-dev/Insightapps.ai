import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

export const admin: Routes = [
 {path:'pages/file-manager',children:[ {
  path: 'filemanager',
  loadComponent: () =>
    import('./filemanager/filemanager.component').then((m) => m.FilemanagerComponent),
},
{
  path: 'filemanager-list',
  loadComponent: () =>
    import('./filemanager-list/filemanager-list.component').then((m) => m.FilemanagerListComponent),
},

]}
];
@NgModule({
  imports: [RouterModule.forChild(admin)],
  exports: [RouterModule],
})
export class filemanagerRoutingModule {
  static routes = admin;
}