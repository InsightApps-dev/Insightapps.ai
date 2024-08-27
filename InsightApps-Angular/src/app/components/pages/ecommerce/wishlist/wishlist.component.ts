import { Component } from '@angular/core';
import { SharedModule } from '../../../../shared/sharedmodule';
import { RouterModule } from '@angular/router';
const DATA = [ 
  {
id:"1",
src:"./assets/images/shop/9.png" ,
name:'A White Table Lamp',
type:'Electronics',
price:'$852',
price1:'$1700',
offer:'50% off today',
status:'SALE!',
bg:'danger'

},
{
  id:"2",
  src:"./assets/images/shop/10.png" ,
  name:'A Green Sleeve Tshirt',
  type:'Clothes',
  price:'$950',
  price1:'$1900',
  offer:'59% off today',
  status:'DEAL!',
  bg:'success'
  
  },
  {
    id:"3",
    src:"./assets/images/shop/11.png" ,
    name:'A Semi Minimal Chair',
    type:'Furnitures',
    price:'$1,150',
    price1:'$2,000',
    offer:'47% off today',
    status:'DEAL!',
    bg:'success'
    
    },
    {
      id:"4",
      src:"./assets/images/shop/13.png" ,
      name:'Casual Leather Shoes',
      type:'Footwear',
      price:'$2,200',
      price1:'$3,500',
      offer:'35% off today',
      status:'DEAL!',
      bg:'success'
      
      },
      {
        id:"5",
        src:"./assets/images/shop/12.png" ,
        name:'Fashion 3D Sun Glasses',
        type:'Electronics',
        price:'$990',
        price1:'$1100',
        offer:'19% off today',
        status:'SALE!',
        bg:'success'
        
        },
        {
          id:"6",
          src:"./assets/images/shop/14.png" ,
          name:'A Brown Mens Hoodie',
          type:'Fashion',
          price:'$1,500',
          price1:'$1,900',
          offer:'35% off today',
          status:'SALE!',
          bg:'danger'
          
          },
          {
            id:"7",
            src:"./assets/images/shop/15.png" ,
            name:'Three Water Bottles',
            type:'Stationary',
            price:'$500',
            price1:'$600',
            offer:'10% off today',
            status:'DEAL!',
            bg:'success'
            
            },
            {
              id:"8",
              src:"./assets/images/shop/16.png" ,
              name:'A Brown Women Bag',
              type:'Stationary',
              price:'$800',
              price1:'$1,700',
              offer:'40% off today',
              status:'SALE!',
              bg:'danger'
              
              },
              {
                id:"9",
                src:"./assets/images/shop/18.png" ,
                name:'Soundtrack Headsets',
                type:'Gadgets',
                price:'$900',
                price1:'$1,800',
                offer:'50% off today',
                status:'DEAL!',
                bg:'success'
                
                },
                {
                  id:"10",
                  src:"./assets/images/shop/19.png" ,
                  name:'Mens Red Tshirt',
                  type:'Fashions',
                  price:'$650',
                  price1:'$1,700',
                  offer:'40% off today',
                  status:'SALE!',
                  bg:'danger'
                  
                  },
]
@Component({
  selector: 'app-wishlist',
  standalone: true,
  imports: [SharedModule,RouterModule],
  templateUrl: './wishlist.component.html',
  styleUrls: ['./wishlist.component.scss']
})
export class WishlistComponent {
  productdata = DATA;

  alphabetpage=3;
  click = (id:string)=>{
    const data = this.productdata.filter(x =>{
      return x.id != id;
    });
    this.productdata = data;
  };
}
