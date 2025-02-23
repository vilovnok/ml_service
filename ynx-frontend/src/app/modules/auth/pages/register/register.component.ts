import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { NgToastService } from 'ng-angular-popup';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

  registerForm!: FormGroup;

  constructor(
    private fb: FormBuilder, 
    private service: AuthService,
    private router: Router,
    private toast: NgToastService) { }


  ngOnInit(): void {
    this.valid_fun();
  }

  valid_fun(): void {
    this.registerForm = this.fb.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      username: ['', Validators.required],
      email: ['', Validators.required],
      password: ['', Validators.required],
    });
  }

  onReg() {
    if (this.registerForm.valid) {
      this.service.handle_post_requests(this.registerForm.value,'auth/register').subscribe({
        next: (res) => {
          this.registerForm.reset();
          this.service.saveDataToLS('user_id',res.user_id);
          this.toast.success({detail:"SUCCESS",summary:res.message}); 
          this.router.navigate(['verify']);
        },
        error: (err) => {
          this.toast.error({detail:"ERROR",summary:err.error.detail})
        }});
    } else {
      this.toast.error({detail:"ERROR", summary:"Зполните всю форму!", duration: 5000});
    }
  }
}
