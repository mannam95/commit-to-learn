import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ManageEmployeesComponent } from './components/manage-employees/manage-employees.component';
import { ManageTrainingsComponent } from './components/manage-trainings/manage-trainings.component';
import { EmployeeIconComponent } from './shared/employee-icon/employee-icon.component';
import { EmployeeButtonComponent } from './shared/employee-button/employee-button.component';



@NgModule({
  declarations: [
    ManageEmployeesComponent,
    ManageTrainingsComponent,
    EmployeeIconComponent,
    EmployeeButtonComponent
  ],
  imports: [
    CommonModule
  ]
})
export class EmployeesModule { }
