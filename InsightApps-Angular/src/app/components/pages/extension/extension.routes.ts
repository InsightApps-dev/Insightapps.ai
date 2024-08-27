import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

export const admin: Routes = [
 {path:'pages/extension',children:[ {
  path: 'about-company',
  loadComponent: () =>
    import('./about-company/about-company.component').then((m) => m.AboutCompanyComponent),
},
{
  path: 'blog',
  loadComponent: () =>
    import('./blog/blog.component').then((m) => m.BlogComponent),
},
{
  path: 'blog-details',
  loadComponent: () =>
    import('./blog-details/blog-details.component').then((m) => m.BlogDetailsComponent),
},
{
    path: 'blog-details',
    loadComponent: () =>
      import('./blog-details/blog-details.component').then((m) => m.BlogDetailsComponent),
  },
  {
    path: 'blog-post',
    loadComponent: () =>
      import('./blog-post/blog-post.component').then((m) => m.BlogPostComponent),
  },
  {
    path: 'empty-page',
    loadComponent: () =>
      import('./empty-page/empty-page.component').then((m) => m.EmptyPageComponent),
  },
  {
    path: 'faqs',
    loadComponent: () =>
      import('./faqs/faqs.component').then((m) => m.FaqsComponent),
  },
  {
    path: 'invoice',
    loadComponent: () =>
      import('./invoice/invoice.component').then((m) => m.InvoiceComponent),
  },
  {
    path: 'pricing-tables',
    loadComponent: () =>
      import('./pricing-tables/pricing-tables.component').then((m) => m.PricingTablesComponent),
  },
  {
    path: 'settings',
    loadComponent: () =>
      import('./settings/settings.component').then((m) => m.SettingsComponent),
  },
  {
    path: 'terms',
    loadComponent: () =>
      import('./terms/terms.component').then((m) => m.TermsComponent),
  },
]}
];
@NgModule({
  imports: [RouterModule.forChild(admin)],
  exports: [RouterModule],
})
export class extensionRoutingModule {
  static routes = admin;
}