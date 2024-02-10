import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Component1Component } from './components/component1/component1.component';
import { Component2Component } from './components/component2/component2.component';
import { InitCapsPipe } from './pipes/init-caps.pipe';



@NgModule({
  declarations: [
    Component1Component,
    Component2Component,
    InitCapsPipe
  ],
  imports: [
    CommonModule
  ]
})
export class SharedModule { }
