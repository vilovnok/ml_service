import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RegisterComponent } from './modules/auth/pages/register/register.component';
import { LoginComponent } from './modules/auth/pages/login/login.component';
import { ForgotPasswordComponent } from './modules/auth/pages/forgot-password/forgot-password.component';
import { NotFoundComponent } from './modules/auth/pages/not-found/not-found.component';
import { authGuard } from './guards/auth.guard';
import { VerifyComponent } from './modules/auth/pages/verify/verify.component';

const routes: Routes = [
  { 
    path: '', redirectTo: '/reg', pathMatch: 'full' 
  },
  {
    path: "reg", component: RegisterComponent, title: "Sign up"
  },
  {
    path: "login", component: LoginComponent, title: "Login"
  },
  {
    path: "forgot-password", component: ForgotPasswordComponent, title: "Forgot password"
  },
  {
    path: "verify", component: VerifyComponent, title: "Verify"
  },
  {
    path: "home", loadChildren: () => import("./modules/main/main-route.module").then((m)=> m.MainRouteModule),
    canActivate:[authGuard]
  },
  {
    path: "**", component: NotFoundComponent, title: "Not Founded"
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
