import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageTrainingsComponent } from './manage-trainings.component';

describe('ManageTrainingsComponent', () => {
  let component: ManageTrainingsComponent;
  let fixture: ComponentFixture<ManageTrainingsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageTrainingsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageTrainingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
