import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { authGuard } from '../../auth.guard';

export const admin: Routes = [
 {path:'adminui',children:[ {
  path: 'card-design',
  // canLoad:[authGuard],
  canActivate:[authGuard],
  loadComponent: () =>
    import('./card-design/card-design.component').then((m) => m.CardDesignComponent),
},
{
  path: 'chat',
  loadComponent: () =>
    import('./chat/chat.component').then((m) => m.ChatComponent),
},
{
  path: 'content-scrollbar',
  loadComponent: () =>
    import('./content-scrollbar/content-scrollbar.component').then((m) => m.ContentScrollbarComponent),
},
{
  path: 'full-calendar',
  loadComponent: () =>
    import('./full-calendar/full-calendar.component').then((m) => m.FullCalendarComponent),
},
{
  path: 'loaders',
  loadComponent: () =>
    import('./loaders/loaders.component').then(
      (m) => m.LoadersComponent
    ),
},
{
  path: 'notifications',
  loadComponent: () =>
    import('./notifications/notifications.component').then(
      (m) => m.NotificationsComponent
    ),
},
{
  path: 'range-slider',
  loadComponent: () =>
    import('./range-slider/range-slider.component').then((m) => m.RangeSliderComponent),
},
{
  path: 'rating',
  loadComponent: () =>
    import('./rating/rating.component').then((m) => m.RatingComponent),
},
{
  path: 'ribbons',
  loadComponent: () =>
    import('./ribbons/ribbons.component').then((m) => m.RibbonsComponent),
},
{
  path: 'search',
  loadComponent: () =>
    import('./search/search.component').then((m) => m.SearchComponent),
},
{
  path: 'sweetalerts',
  loadComponent: () =>
    import('./sweetalerts/sweetalerts.component').then((m) => m.SweetalertsComponent),
},
{
  path: 'swiperjs',
  loadComponent: () =>
    import('./swiperjs/swiperjs.component').then((m) => m.SwiperjsComponent),
},
{
  path: 'timeline',
  loadComponent: () =>
    import('./timeline/timeline.component').then((m) => m.TimelineComponent),
},
{
  path: 'treeview',
  loadComponent: () =>
    import('./treeview/treeview.component').then((m) => m.TreeviewComponent),
},
{
  path: 'userlist',
  loadComponent: () =>
    import('./userlist/userlist.component').then((m) => m.UserlistComponent),
},

]}
];
@NgModule({
  imports: [RouterModule.forChild(admin)],
  exports: [RouterModule],
})
export class adminuiRoutingModule {
  static routes = admin;
}