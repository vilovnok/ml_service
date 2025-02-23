import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { NgToastService } from 'ng-angular-popup';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.scss']
})
export class ForgotPasswordComponent {
  email:string='';
  password:string='';
  ForgotForm!: FormGroup;

  constructor(
    private fb: FormBuilder, 
    private service: AuthService,
    private router: Router,
    private toast: NgToastService) {}


    go_to_login(){
      this.router.navigate(['/login']);
    }

    update_password(){

      let formData = this.fb.group({
        password: this.password,
        email: this.email,
      });
      
      if (this.password !='' && this.email !=''){
        this.service.handle_post_requests(formData.value, 'auth/reset-password').subscribe({
          next: (res) => {
            this.toast.success({detail:"SUCCESS", summary: res.message}); 
            this.router.navigate(['/login']);
          },
          error: (err) => {
            this.toast.error({detail:"ERROR",summary: err.error.detail})
          }
        });
      }else {
        this.toast.error({detail:"ERROR", summary: "Fill out the form 😅", duration: 5000}); 
      }

    }






}
