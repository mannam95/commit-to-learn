import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EmployeeIconComponent } from './employee-icon.component';

describe('EmployeeIconComponent', () => {
  let component: EmployeeIconComponent;
  let fixture: ComponentFixture<EmployeeIconComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EmployeeIconComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EmployeeIconComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
