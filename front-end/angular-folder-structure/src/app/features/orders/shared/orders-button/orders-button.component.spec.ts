import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OrdersButtonComponent } from './orders-button.component';

describe('OrdersButtonComponent', () => {
  let component: OrdersButtonComponent;
  let fixture: ComponentFixture<OrdersButtonComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OrdersButtonComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OrdersButtonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
