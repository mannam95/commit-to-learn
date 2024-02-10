import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OrdersIconComponent } from './orders-icon.component';

describe('OrdersIconComponent', () => {
  let component: OrdersIconComponent;
  let fixture: ComponentFixture<OrdersIconComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OrdersIconComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OrdersIconComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
