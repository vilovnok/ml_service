import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { NgToastService } from 'ng-angular-popup';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-popup',
  templateUrl: './popup.component.html',
  styleUrls: ['./popup.component.scss']
})
export class PopupComponent implements OnInit {

  inputdata: any;
  editdata:any;
  closemessage = 'Closed';
  role_customer: string = "user";
  choose_fun:boolean=false;
  
  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private ref: MatDialogRef<PopupComponent>,
    private fb: FormBuilder,
    private serivce: AuthService,
    private toast: NgToastService) { }

  ngOnInit(): void {
    this.inputdata = this.data;
    if (this.inputdata.user_id > -1) {
      this.choose_fun=true;
      this.setpopupdata(this.inputdata.user_id);
    }
  }

  closepopup() {this.ref.close(this.closemessage);}

  setpopupdata(user_id:any) {
    const req_form = this.fb.group({user_id: user_id}).value;
    this.serivce.handle_post_requests(req_form,'user/profile').subscribe(res=>{
      this.editdata=res;
      this.myForm.setValue({
        username:this.editdata.username, 
        role:this.editdata.role,
        email:this.editdata.email,
        active:this.editdata.is_active,
        user_id:this.editdata.id
      });

    });
  }

  myForm = this.fb.group({
    username: this.fb.control('', Validators.compose([Validators.required,Validators.minLength(5)])),
    email: this.fb.control('', Validators.compose([Validators.required,Validators.email])),
    role: this.fb.control(''),
    active: this.fb.control(true),
    user_id: this.fb.control(0),
  });
  
  Saveuser() {
    this.serivce.Save_and_Add_User(this.myForm.value,'user/save').subscribe(res=>{
      console.log(res);
      this.closepopup();
      this.toast.success({detail:'SUCCESS', summary: 'Пользователь успешно обновлен!'});
    });
  }

  CreateUser() {
    this.serivce.Save_and_Add_User(this.myForm.value,'user/add').subscribe({
      next: (res) => {
        this.myForm.reset();
        this.closepopup();
        this.toast.success({detail:'SUCCESS', summary: res.message});
      },
      error: (err) => {
        console.log(err);
        this.toast.error({detail:"ERROR",summary:err.error.detail})
      }});
  }

  pickFunction() {
    if(this.choose_fun) {this.Saveuser();}
    else{this.CreateUser();}
  }


}
