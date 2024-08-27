import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

export const admin: Routes = [
 {path:'form-module',children:[ {
  path: 'form-advanced',
  loadComponent: () =>
    import('./form-advanced/form-advanced.component').then((m) => m.FormAdvancedComponent),
},
{
  path: 'form-editor',
  loadComponent: () =>
    import('./form-editor/form-editor.component').then((m) => m.FormEditorComponent),
},
{
  path: 'form-elements',
  loadComponent: () =>
    import('./form-elements/form-elements.component').then((m) => m.FormElementsComponent),
},
{
  path: 'form-input-spinners',
  loadComponent: () =>
    import('./form-input-spinners/form-input-spinners.component').then((m) => m.FormInputSpinnersComponent),
},
{
  path: 'form-editor',
  loadComponent: () =>
    import('./form-editor/form-editor.component').then((m) => m.FormEditorComponent),
},
{
    path: 'form-layouts',
    loadComponent: () =>
      import('./form-layouts/form-layouts.component').then((m) => m.FormLayoutsComponent),
  },
  {
    path: 'form-validation',
    loadComponent: () =>
      import('./form-validation/form-validation.component').then((m) => m.FormValidationComponent),
  },
  {
    path: 'select2',
    loadComponent: () =>
      import('./select2/select2.component').then((m) => m.Select2Component),
  },
]}
];
@NgModule({
  imports: [RouterModule.forChild(admin)],
  exports: [RouterModule],
})
export class formsmoduleRoutingModule {
  static routes = admin;
}