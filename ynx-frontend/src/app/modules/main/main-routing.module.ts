import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MainComponent } from './pages/main/main.component';
import { PipelineComponent } from './pages/pipeline/pipeline.component';
import { SearchComponent } from './pages/search/search.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { dashboardGuard } from 'src/app/guards/dashboard.guard';


const routes: Routes = [
  {
    path: "", 
    component: MainComponent, 
    children: [
    {path: "search", component: SearchComponent, title: "Search"},
    {path: "pipeline", component: PipelineComponent, title: "Pipeline"},
    {path: "dashboard", component: DashboardComponent, title: "Dashboard",canActivate:[dashboardGuard]},
    { path: '', redirectTo: '/home/search', pathMatch: 'full' },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MainRouteRoutingModule { }
