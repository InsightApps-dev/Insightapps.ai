import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

export const admin: Routes = [
 {path:'pages',children:[ {
  path: 'gallery',
  loadComponent: () =>
    import('./gallery/gallery.component').then((m) => m.GalleryComponent),
},
{
  path: 'mail-inbox',
  loadComponent: () =>
    import('./mail-inbox/mail-inbox.component').then((m) => m.MailInboxComponent),
},
{
  path: 'profile', 
  loadComponent: () =>
    import('./profile/profile.component').then((m) => m.ProfileComponent),
},
{
  path: 'notification-list',
  loadComponent: () =>
    import('./notification-list/notification-list.component').then((m) => m.NotificationListComponent),
},


]}
];
@NgModule({
  imports: [RouterModule.forChild(admin)],
  exports: [RouterModule],
})
export class pagesRoutingModule {
  static routes = admin;
}