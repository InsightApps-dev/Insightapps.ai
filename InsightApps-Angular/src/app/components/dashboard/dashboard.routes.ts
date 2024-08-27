import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { authGuard } from '../../auth.guard';

export const admin: Routes = [
 {path:'',children:[ {
  path: 'dashboard',
  canActivate:[authGuard],
  loadComponent: () =>
    import('./dashboard/dashboard.component').then((m) => m.DashboardComponent),
},



]}
];
@NgModule({
  imports: [RouterModule.forChild(admin)],
  exports: [RouterModule],
})
export class dashboardRoutingModule {
  static routes = admin;
}