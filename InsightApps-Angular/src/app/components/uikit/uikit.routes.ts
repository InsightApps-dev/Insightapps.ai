import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

export const admin: Routes = [
 {path:'uikit',children:[ {
  path: 'accordions',
  loadComponent: () =>
    import('./accordions/accordions.component').then((m) => m.AccordionsComponent),
},
{
  path: 'alerts',
  loadComponent: () =>
    import('./alerts/alerts.component').then((m) => m.AlertsComponent),
},
{
  path: 'avatars',
  loadComponent: () =>
    import('./avatars/avatars.component').then((m) => m.AvatarsComponent),
},
{
  path: 'badges-pills',
  loadComponent: () =>
    import('./badges-pills/badges-pills.component').then((m) => m.BadgesPillsComponent),
},
{
  path: 'breadcrumbs',
  loadComponent: () =>
    import('./breadcrumbs/breadcrumbs.component').then(
      (m) => m.BreadcrumbsComponent
    ),
},
{
  path: 'buttons',
  loadComponent: () =>
    import('./buttons/buttons.component').then(
      (m) => m.ButtonsComponent
    ),
},
{
  path: 'carousels',
  loadComponent: () =>
    import('./carousels/carousels.component').then((m) => m.CarouselsComponent),
},
{
  path: 'colors',
  loadComponent: () =>
    import('./colors/colors.component').then((m) => m.ColorsComponent),
},
{
  path: 'dropdowns',
  loadComponent: () =>
    import('./dropdowns/dropdowns.component').then((m) => m.DropdownsComponent),
},
{
  path: 'listgroup',
  loadComponent: () =>
    import('./listgroup/listgroup.component').then((m) => m.ListgroupComponent),
},
{
  path: 'media-object',
  loadComponent: () =>
    import('./media-object/media-object.component').then((m) => m.MediaObjectComponent),
},
{
  path: 'modal',
  loadComponent: () =>
    import('./modal/modal.component').then((m) => m.ModalComponent),
},
{
  path: 'navigation',
  loadComponent: () =>
    import('./navigation/navigation.component').then((m) => m.NavigationComponent),
},
{
  path: 'offcanvas',
  loadComponent: () =>
    import('./offcanvas/offcanvas.component').then((m) => m.OffcanvasComponent),
},
{
  path: 'pagination',
  loadComponent: () =>
    import('./pagination/pagination.component').then((m) => m.PaginationComponent),
},
{
    path: 'progress',
    loadComponent: () =>
      import('./progress/progress.component').then((m) => m.ProgressComponent),
  },
  {
    path: 'scrollspy',
    loadComponent: () =>
      import('./scrollspy/scrollspy.component').then((m) => m.ScrollspyComponent),
  },
  {
    path: 'tabs',
    loadComponent: () =>
      import('./tabs/tabs.component').then((m) => m.TabsComponent),
  },
  {
    path: 'tags',
    loadComponent: () =>
      import('./tags/tags.component').then((m) => m.TagsComponent),
  },
  {
    path: 'toast',
    loadComponent: () =>
      import('./toast/toast.component').then((m) => m.ToastComponent),
  },
  {
    path: 'tooltip-popover',
    loadComponent: () =>
      import('./tooltip-popover/tooltip-popover.component').then((m) => m.TooltipPopoverComponent),
  },
  {
    path: 'typography',
    loadComponent: () =>
      import('./typography/typography.component').then((m) => m.TypographyComponent),
  },
]}
];
@NgModule({
  imports: [RouterModule.forChild(admin)],
  exports: [RouterModule],
})
export class uikitRoutingModule {
  static routes = admin;
}