import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

export const admin: Routes = [
 {path:'icons',children:[ {
  path: 'bootstrap-icons',
  loadComponent: () =>
    import('./bootstrap-icons/bootstrap-icons.component').then((m) => m.BootstrapIconsComponent),
},
{
  path: 'feather-icons',
  loadComponent: () =>
    import('./feather-icons/feather-icons.component').then((m) => m.FeatherIconsComponent),
},
{
  path: 'flag-icons',
  loadComponent: () =>
    import('./flag-icons/flag-icons.component').then((m) => m.FlagIconsComponent),
},
{
    path: 'font-awesome-icons',
    loadComponent: () =>
      import('./font-awesome-icons/font-awesome-icons.component').then((m) => m.FontAwesomeIconsComponent),
  },
  {
    path: 'ionic-icons',
    loadComponent: () =>
      import('./ionic-icons/ionic-icons.component').then((m) => m.IonicIconsComponent),
  },
  {
    path: 'material-design-icons',
    loadComponent: () =>
      import('./material-design-icons/material-design-icons.component').then((m) => m.MaterialDesignIconsComponent),
  },
  {
    path: 'pe7-icons',
    loadComponent: () =>
      import('./pe7-icons/pe7-icons.component').then((m) => m.Pe7IconsComponent),
  },
  {
    path: 'simple-line-icons',
    loadComponent: () =>
      import('./simple-line-icons/simple-line-icons.component').then((m) => m.SimpleLineIconsComponent),
  },
  {
    path: 'typicon-icons',
    loadComponent: () =>
      import('./typicon-icons/typicon-icons.component').then((m) => m.TypiconIconsComponent),
  },
  {
    path: 'weather-icons',
    loadComponent: () =>
      import('./weather-icons/weather-icons.component').then((m) => m.WeatherIconsComponent),
  },
]}
];
@NgModule({
  imports: [RouterModule.forChild(admin)],
  exports: [RouterModule],
})
export class iconsRoutingModule {
  static routes = admin;
}