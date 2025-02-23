import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { NgToastService } from 'ng-angular-popup';
import validateForm from 'src/app/helpers/validateform';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  loginForm!: FormGroup;
  
  constructor(
    private fb: FormBuilder, 
    private service: AuthService,
    private router: Router,
    private toast: NgToastService) {}

  ngOnInit(): void {
    this.valid_fun();
  }

  valid_fun(): void {
    this.loginForm = this.fb.group({
      email: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  onLogin() {
    if (this.loginForm.valid) {
      this.service.handle_post_requests(this.loginForm.value,'auth/login').subscribe({
        next: (res) => {
          console.log("Tokens: ",res);
          this.loginForm.reset();
          this.service.saveTokens(res);    
          this.service.updatemenu.next();
          this.router.navigate(['home']);
        },
        error: (err) => {
          console.log();
          this.toast.error({detail:"ERROR", summary:"Проверьте данные!", duration: 5000});
        }});
      console.log("Forma отправлена: ", this.loginForm.value);
    } else {
      console.log("Forma не отправлена");
      this.toast.error({detail:"ERROR", summary:"Зполните всю форму", duration: 5000});
    }
  }

  go_to_Reg(){
    this.router.navigate(['reg']);
  }
}
