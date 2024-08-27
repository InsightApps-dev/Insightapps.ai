import { Component } from '@angular/core';
import { SharedModule } from '../../../../shared/sharedmodule';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

interface cart{
  id: number;
  image: string;
  title: string;
  quantity: number;
  price: string;
  total: string;
  title1:string
}
@Component({
  selector: 'app-shopping-cart',
  standalone: true,
  imports: [SharedModule,FormsModule,ReactiveFormsModule,RouterModule],
  templateUrl: './shopping-cart.component.html',
  styleUrls: ['./shopping-cart.component.scss']
})
export class ShoppingCartComponent {
  
  objectArray: cart[];
  constructor() { 
    this.objectArray = [
      { id: 1, image: "./assets/images/products/9.jpg", title1:"Quantity : 2Kgs", title : "A blue flower bucket", price : "$568", total :'$568', quantity: 1},
      { id: 2, image: "./assets/images/products/10.jpg",title1:"Quantity : 1 piece", title : "A New Magnus airpods", price : "$1,027", total :'$3,082', quantity: 1},
      { id: 3, image: "./assets/images/products/8.jpg",title1:"Quantity : 3pcs", title : "Kids T-shirts", price : "$1,549", total : '$7,945', quantity: 2},
      { id: 4, image: "./assets/images/products/7.jpg",title1:"Quantity : 1pc", title : "Rose Liquid Bottle", price : "$1,027", total : '$3,082', quantity: 1},
      { id: 5, image: "./assets/images/products/5.jpg",title1:"Quantity : 1pc", title : "Hand Picked Camera", price : "$1,589", total : '$7,945', quantity: 1},
      { id: 6, image: "./assets/images/products/11.jpg",title1:"Quantity : 1pc", title : "Green Mike Shoes", price : "$3,589", total : '$3,589', quantity: 1},
      { id: 7, image: "./assets/images/products/12.jpg",title1:"Quantity : 1pc", title : "Black Sunshade Glasses", price : "$609", total : '$1,218', quantity: 1},

   

    ];
  }

  
  RemoveElementFromObjectArray(key: number) {
    this.objectArray.forEach((value,index)=>{
        if(value.id==key) this.objectArray.splice(index,1);
    });
  }
  ngAfterViewInit() {
    const plusButtons = document.querySelectorAll('.product-quantity-plus');
    const minusButtons = document.querySelectorAll('.product-quantity-minus');
  
    function perfectChart() {
      plusButtons.forEach((plusButton: any) => {
        plusButton.addEventListener('click', () => {
          const parentDiv = plusButton.closest('.quantity');
          const quantityInput = parentDiv.querySelector('.qty');
  
          if (quantityInput) {
            quantityInput.value = String(Number(quantityInput.value) + 1);
          }
        });
      });
  
      minusButtons.forEach((minusButton: any) => {
        minusButton.addEventListener('click', () => {
          const parentDiv = minusButton.closest('.quantity');
          const quantityInput = parentDiv.querySelector('.qty');
  
          if (quantityInput && quantityInput.value > 0) {
            quantityInput.value = String(Number(quantityInput.value) - 1);
          }
        });
      });
    }
  
    perfectChart();
  }
  
}
