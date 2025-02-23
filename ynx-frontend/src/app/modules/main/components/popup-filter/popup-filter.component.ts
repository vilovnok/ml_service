import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { NgToastService } from 'ng-angular-popup';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-popup-filter',
  templateUrl: './popup-filter.component.html',
  styleUrls: ['./popup-filter.component.scss']
})
export class PopupFilterComponent implements OnInit {

  inputdata: any;
  closemessage = 'Closed';
  filename: string = '';

  maxDate: string = '';

  date = new Date();
  currentYear = this.date.getUTCFullYear();
  currentMonth = this.date.getUTCMonth() + 1;
  currentDay = this.date.getUTCDate();
  TodayDate: any;

  start_date:string='';
  end_date:string='';

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private fb: FormBuilder,
    private ref: MatDialogRef<PopupFilterComponent>,
    private service: AuthService,
    private toast: NgToastService) { }


  ngOnInit(): void {
    this.inputdata = this.data;
    this.getTodayDate();

  }

  getTodayDate() {
    this.TodayDate=`${this.currentYear}-${(this.currentMonth).toString().padStart(2, '0')}-${this.currentDay.toString().padStart(2, '0')}`;
    this.maxDate=this.TodayDate;
  }
  closepopup() {this.ref.close(this.closemessage);}

  fetchSpecificFile() {
    if (this.filename != '') {
      this.service.handle_get_requests(this.filename, 'pipe/spec-file').subscribe({
        next: (res) => {
          this.closepopup();
          this.toast.success({ detail: 'success', summary: 'The file has been sent to the mail.' });},
        error: (err) => {
          
          this.toast.warning({ detail: "warning", summary: 'The file was not found.' });
        }});
    } else {
      this.toast.warning({ detail: "warning", summary: 'Enter the name of the file.' });}
  }

  fetchSpecificFileByDate() {
    if (this.start_date && this.end_date) {
      const formatted_start_date: Date= new Date(this.start_date);
      const formatted_end_date: Date= new Date(this.end_date);
      let req_form=this.fb.group({start_date:formatted_start_date,end_date:formatted_end_date});      
      if(formatted_start_date<formatted_end_date){
        this.service.handle_post_requests(req_form.value, 'pipe/spec-file-by-date').subscribe({
          next: (res)=>{
            req_form.reset();
            this.closepopup();
            this.toast.success({ detail: 'success', summary: 'The period is being considered.' });
          },error:(err)=>{
            if(err.status===404) {
              this.toast.error({ detail: "Error", summary: err.error.detail });
            }
          }
        });
      }else{this.toast.warning({ detail: 'Attention', summary: 'Check the data! (start_date > end_date)'});}
    }else{this.toast.warning({ detail: "Attention", summary: 'Enter the full period!' })}}




}


