import { CanActivate, Router } from '@angular/router';
import { Injectable } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { NgToastService } from 'ng-angular-popup';

@Injectable({
  providedIn:"root"
})

export class authGuard implements CanActivate{

  constructor(
    private auth: AuthService, 
    private router: Router,
    private toast: NgToastService){}


  canActivate(): boolean {
    if(this.auth.getDataFromLS('token')){
      const active = this.auth.GetDatabyToken(this.auth.getDataFromLS('token')).active;
      const verify = this.auth.GetDatabyToken(this.auth.getDataFromLS('token')).verify;
      console.log(`Verify: ${verify}`);
      console.log(active);
      if(!active){
        this.toast.error({detail:'Error', summary: 'You have been blocked.'});
        return false;
      }
      if(!verify){
        this.router.navigate(['verify']);
        return false;
      }
    return true;  
    }else{
      this.toast.error({detail:"ERROR", summary:"Please login first!"});
      this.router.navigate(['login']);
      return false;
    }
  }
};
