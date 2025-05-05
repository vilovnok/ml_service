import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';
import { FormBuilder } from '@angular/forms';
import { NgToastService } from 'ng-angular-popup';

import { PageEvent } from '@angular/material/paginator';
import { LoadingHandler } from 'src/app/helpers/loading-handler';
import { MatDialog } from '@angular/material/dialog';
import { PopupFilterComponent } from '../../components/popup-filter/popup-filter.component';
import { timeout } from 'rxjs';


@Component({
  selector: 'app-pipeline',
  templateUrl: './pipeline.component.html',
  styleUrls: ['./pipeline.component.scss']
})
export class PipelineComponent {
  input_text: string = '';


  constructor(private service: AuthService, private toast: NgToastService) { }


  async generate(){    
    const reqBody = {message: this.input_text}
    this.input_text = '';
    this.service.handle_post_requests(reqBody, 'generate/top-up-balance').subscribe(
      async response => {
        const token = response['token'];
        const checkInterval = setInterval(() => {
          this.service.handle_get_requests(token, 'generate/check-balance').subscribe(
            res => {
              const balance = res['balance']
              if (res.status === 'completed') {
                clearInterval(checkInterval);
                if (res.message_gen=='убедил'){
                  this.toast.success({
                    detail: "Баланс пополнен",
                    summary: `Убедил! Теперь Ваш текущий баланс составляет: ${balance} YNX`,
                    duration: 4000 
                  },);
                }else{
                  this.toast.error({
                    detail: "Текущий баланс",
                    summary: `Не убедил! Ваш текущий баланс составляет: ${balance} YNX`,
                    duration: 4000 
                  });
                }
              }
            },
            error => {
              if (error.status !== 404) {
                clearInterval(checkInterval);                
              }
            }
          );
        }, 2000);
    });
  }
}