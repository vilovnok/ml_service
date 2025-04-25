import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';
import { FormBuilder } from '@angular/forms';
import { NgToastService } from 'ng-angular-popup';

import { PageEvent } from '@angular/material/paginator';
import { LoadingHandler } from 'src/app/helpers/loading-handler';
import { MatDialog } from '@angular/material/dialog';
import { PopupFilterComponent } from '../../components/popup-filter/popup-filter.component';


@Component({
  selector: 'app-pipeline',
  templateUrl: './pipeline.component.html',
  styleUrls: ['./pipeline.component.scss']
})
export class PipelineComponent implements OnInit {
  input_text: string = '';


  constructor(
    private fb: FormBuilder,
    private service: AuthService,
    private toast: NgToastService,
    private dialog: MatDialog) { }



  ngOnInit(): void {
    this.getBalance();
  }



  getBalance() {
    const reqBody = { user_id: localStorage.getItem('user_id'), message: this.input_text }
    this.service.handle_get_requests(reqBody, 'generate/check_balance').subscribe(response => {
      const balance = response['balance']

      if (response['gate'] == "INJECTION") {
        this.toast.success({
          detail: "Баланс пополнен",
          summary: `Ваш текущий баланс составляет: ${balance}YNX`,
        });
      }
    });
  }

  generate(){
    const reqBody = {message: this.input_text}
    this.service.handle_post_requests(reqBody, 'generate/top-up-balance').subscribe(response => {
      
    });
  }
}