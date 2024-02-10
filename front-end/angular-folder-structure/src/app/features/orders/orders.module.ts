import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AddOrderComponent } from './components/add-order/add-order.component';
import { ManageOrdersComponent } from './components/manage-orders/manage-orders.component';
import { OrdersIconComponent } from './shared/orders-icon/orders-icon.component';
import { OrdersButtonComponent } from './shared/orders-button/orders-button.component';



@NgModule({
  declarations: [
    AddOrderComponent,
    ManageOrdersComponent,
    OrdersIconComponent,
    OrdersButtonComponent
  ],
  imports: [
    CommonModule
  ]
})
export class OrdersModule { }
