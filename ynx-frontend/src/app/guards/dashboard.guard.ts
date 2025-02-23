import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot, UrlTree } from '@angular/router';
import { Injectable } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { NgToastService } from 'ng-angular-popup';

@Injectable({
  providedIn:"root"
})

export class dashboardGuard implements CanActivate{

  currentRole: any;
  currentActive: any;
  constructor(
    private auth: AuthService, 
    private router: Router,
    private toast: NgToastService){}

  canActivate(): boolean  {
    if(this.auth.isLoggedIn()){
      this.currentRole=this.auth.getDataFromLS('role');
      if(this.currentRole=='admin'){
        return true;
      }else{
        this.toast.warning({detail:"Attention", summary:"You are't auth to access this menu!"});
        this.router.navigate(['home']);
        return false;
      }
    } else{
      this.toast.error({detail:"ERROR", summary:"Please login first!"});
      this.router.navigate(['login']);
      return false;
    }
  }
}
