import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

export const admin: Routes = [
 {path:'',children:[ {
  path: 'landingpage',
  loadComponent: () =>
    import('./landingpage/landingpage.component').then((m) => m.LandingpageComponent),
},



]}
];
@NgModule({
  imports: [RouterModule.forChild(admin)],
  exports: [RouterModule],
})
export class landingRoutingModule {
  static routes = admin;
}