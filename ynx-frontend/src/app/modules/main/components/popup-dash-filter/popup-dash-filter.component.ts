import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { NgToastService } from 'ng-angular-popup';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-popup-dash-filter',
  templateUrl: './popup-dash-filter.component.html',
  styleUrls: ['./popup-dash-filter.component.scss']
})
export class PopupDashFilterComponent {

  closemessage:string = 'Closed';
  
  username:string = '';
  email:string = '';
  role:string = '';
  active:boolean = false;
  user_id:number=-9;

  constructor(
    private fb: FormBuilder,
    private ref: MatDialogRef<PopupDashFilterComponent>,
    private service: AuthService,
    private toast: NgToastService) { }


  ngOnInit(): void {}

  closepopup(){this.ref.close(this.closemessage);}

  fetchUserData() {
    if (this.username != '') {
      this.getProfile(this.username, 'username');
    } else if (this.email != '') {
      this.getProfile(this.email, 'email');
    } else {
      this.toast.error({ detail: "ERROR", summary: 'Введите данные!' });
    }
  }

  getProfile(obj: string, by: string) {
    var endpoint: string = (by == 'username') ? 'username' : 'email';
    this.service.handle_get_requests(obj, `user/get-profile-by-${endpoint}`).subscribe({
      next: (res) => {
        this.setpopupdata(res);
        this.toast.success({ detail: 'SUCCESS', summary: res.message });
      },
      error: (err) => {
        console.log(err);
        this.toast.warning({ detail: "Attention", summary: err.error.detail });
      }
    });
  }

  setpopupdata(obj: any) {
      this.role=obj.role,
      this.username=obj.username,
      this.email=obj.email,
      this.active=obj.is_active,
      this.user_id=obj.id
  }

  removeUser() {
    if (confirm('Вы хотите удалить пользователя?')) {
      const req_form = this.fb.group({ user_id: this.user_id }).value;
      this.service.handle_post_requests(req_form,'user/remove').subscribe(res => {
        this.closepopup();
        this.toast.success({ detail: 'success', summary: 'Пользователь удален!' });
      });
    }
  }

  saveUser() {
    this.service.Save_and_Add_User(this.request(),'user/save').subscribe(res=>{
      console.log(res);
      this.closepopup();
      this.toast.success({detail:'SUCCESS', summary: 'Пользователь успешно обновлен!'});
    });
  }  

  request() {
    return this.fb.group({
      username: this.username,
      email: this.email,
      role: this.role,
      active: this.active,
      user_id: this.user_id
    }).value;
  }  

}
