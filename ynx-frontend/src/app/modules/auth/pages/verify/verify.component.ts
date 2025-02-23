import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { NgToastService } from 'ng-angular-popup';
import validateForm from 'src/app/helpers/validateform';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-verify',
  templateUrl: './verify.component.html',
  styleUrls: ['./verify.component.scss']
})
export class VerifyComponent {

  VerifyForm!: FormGroup;
  
  constructor(
    private fb: FormBuilder, 
    private service: AuthService,
    private router: Router,
    private toast: NgToastService) {}

  ngOnInit(): void {
    this.toast.success({detail:"SUCCESS",summary: "Введите code из вашей почты: ******"});
    this.valid_fun();
    this.get_code();
  }

  valid_fun(): void {
    this.VerifyForm = this.fb.group({
      code: ['', Validators.required],
      user_id: [Number(this.service.getDataFromLS('user_id'))]
    });
  }

  get_code():void{
    let user_id = Number(this.service.getDataFromLS('user_id'));
    this.service.handle_get_requests(user_id,'verify/get-code').subscribe({
      next: (res) => {
        console.log("code: ", res);
      },
      error: (err) =>{
        console.log("Error ",err);
      }});
  }

  send_code() {
    if (this.VerifyForm.valid) {
      this.service.handle_post_requests(this.VerifyForm.value,'verify/send-code').subscribe({
        next: (res) => {
          console.log(res);
          this.VerifyForm.reset();
          this.toast.success({detail:"SUCCESS", summary: res.message, duration: 5000});
          this.router.navigate(['login']);
        },
        error: (err) => {
          this.toast.error({detail:"ERROR", summary:err.message, duration: 5000});
        }});
      console.log("Forma отправлена: ", this.VerifyForm.value);
    } else {
      console.log("Forma не отправлена");
      validateForm.validateAllFormFields(this.VerifyForm);
      this.toast.error({detail:"ERROR", summary:"Зполните всю форму", duration: 5000});
    }
  }

}
