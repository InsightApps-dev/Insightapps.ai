import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

export const admin: Routes = [
 {path:'pages/ecommerce',children:[ {
  path: 'add-product',
  loadComponent: () =>
    import('./add-product/add-product.component').then((m) => m.AddProductComponent),
},
{
  path: 'checkout',
  loadComponent: () =>
    import('./checkout/checkout.component').then((m) => m.CheckoutComponent),
},
{
  path: 'product-details',
  loadComponent: () =>
    import('./product-details/product-details.component').then((m) => m.ProductDetailsComponent),
},
{
    path: 'shop',
    loadComponent: () =>
      import('./shop/shop.component').then((m) => m.ShopComponent),
  },
  {
    path: 'shopping-cart',
    loadComponent: () =>
      import('./shopping-cart/shopping-cart.component').then((m) => m.ShoppingCartComponent),
  },
  {
    path: 'wishlist',
    loadComponent: () =>
      import('./wishlist/wishlist.component').then((m) => m.WishlistComponent),
  },
]}
];
@NgModule({
  imports: [RouterModule.forChild(admin)],
  exports: [RouterModule],
})
export class ecommerceRoutingModule {
  static routes = admin;
}