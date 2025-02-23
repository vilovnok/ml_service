import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MainRouteRoutingModule } from './main-routing.module';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { PopupComponent } from './components/popup/popup.component';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SearchUserPipe } from './pipes/search-user.pipe';
import { LoadingComponent } from './components/loading/loading.component';

import { PipelineComponent } from './pages/pipeline/pipeline.component';
import { SearchComponent } from './pages/search/search.component';
import { SearchTextComponent } from './components/search-text/search-text.component';
import { PopupFilterComponent } from './components/popup-filter/popup-filter.component';
import { PopupDashFilterComponent } from './components/popup-dash-filter/popup-dash-filter.component';
import { PopupMenuComponent } from './components/popup-menu/popup-menu.component';
import { SelectMenuComponent } from './components/select-menu/select-menu.component';


@NgModule({
  declarations: [
    DashboardComponent,
    PipelineComponent,
    SearchComponent,
    SearchTextComponent,
    PopupFilterComponent,
    PopupComponent,
    LoadingComponent,
    SearchUserPipe,
    PopupDashFilterComponent,
    PopupMenuComponent,
    SelectMenuComponent,
  ],
  imports: [
    CommonModule,
    MainRouteRoutingModule,
    MatCheckboxModule,
    FormsModule,
    ReactiveFormsModule
  ],
  exports:[
    DashboardComponent,
    PipelineComponent,
    SearchComponent,
    SearchTextComponent,
    PopupFilterComponent,
    PopupComponent
  ]
})
export class MainRouteModule { }
